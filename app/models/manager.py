from app import db
import threading
import time
from datetime import datetime
import numpy as np
import pandas as pd
import json
import logging
from sqlalchemy import create_engine, text
from decimal import Decimal
from auditoriabot import AuditoriaBot
from operacionactiva import OperacionActiva
from bots import Bots
from exchanges import Exchanges
from activos import Activos
from estrategias import Estrategias
import ccxt

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class BotTradingContinuo(threading.Thread):
    def __init__(self, bot_id, interval=60):
        super().__init__()
        self.bot_id = bot_id
        self.interval = interval  # Intervalo en segundos
        self.running = False
        self.daemon = True  # El hilo se cerrará cuando el programa principal termine
        
        # Inicializar bot y configuraciones
        self.bot = Bots.query.get(bot_id)
        self.exchange_config = Exchanges.query.get(self.bot.exchange_id)
        self.activo = Activos.query.get(self.bot.activo_id)
        self.estrategia = Estrategias.query.get(self.bot.estrategia_id)
        self.params = json.loads(self.estrategia.parametros)
        
        # Inicializar exchange
        self.exchange = self.inicializar_exchange()
        
        # Control de estado
        self.ultima_operacion = None
        self.operacion_activa = None

    def registrar_auditoria(self, tipo_evento, descripcion, datos=None):
        """Registra eventos de auditoría del bot"""
        try:
            auditoria = AuditoriaBot(
                bot_id=self.bot_id,
                fecha=datetime.utcnow(),
                tipo_evento=tipo_evento,
                descripcion=descripcion,
                datos=json.dumps(datos) if datos else None
            )
            db.session.add(auditoria)
            db.session.commit()
        except Exception as e:
            logging.error(f"Error al registrar auditoría: {str(e)}")
            db.session.rollback()

    def inicializar_exchange(self):
        """Inicializa la conexión con el exchange"""
        try:
            exchange_class = getattr(ccxt, self.exchange_config.nombre.lower())
            exchange = exchange_class({
                'apiKey': self.exchange_config.api_key,
                'secret': self.exchange_config.secret_key,
                'enableRateLimit': True
            })
            return exchange
        except Exception as e:
            self.registrar_auditoria('ERROR', f"Error al inicializar exchange: {str(e)}")
            raise

    def obtener_indicadores_actuales(self):
        """Obtiene los indicadores técnicos actuales"""
        try:
            symbol = f"{self.activo.simbolo}/USDT"
            
            # Obtener el último precio
            ticker = self.exchange.fetch_ticker(symbol)
            precio_actual = ticker['last']
            
            # Obtener datos OHLCV más recientes para los indicadores
            ohlcv = self.exchange.fetch_ohlcv(symbol, '1m', limit=1)[0]
            
            return {
                'precio': precio_actual,
                'volumen': ohlcv[5],
                'timestamp': datetime.fromtimestamp(ohlcv[0]/1000)
            }
        except Exception as e:
            self.registrar_auditoria('ERROR', f"Error al obtener indicadores: {str(e)}")
            raise

    def verificar_estado_bot(self):
        """Verifica si el bot debe seguir ejecutándose"""
        try:
            bot = db.session.query(Bots).filter_by(id=self.bot_id).first()
            if not bot or not bot.activo:
                self.registrar_auditoria('INFO', "Bot desactivado")
                return False
            return True
        except Exception as e:
            self.registrar_auditoria('ERROR', f"Error al verificar estado: {str(e)}")
            return False

    def gestionar_operacion_activa(self, indicadores_actuales):
        """Gestiona una operación activa, verificando take profit y stop loss"""
        if not self.operacion_activa:
            return

        precio_actual = indicadores_actuales['precio']
        operacion = self.operacion_activa

        # Calcular beneficio/pérdida actual
        if operacion.tipo_operacion == 'LONG':
            beneficio = (precio_actual - operacion.precio_entrada) / operacion.precio_entrada * 100
        else:  # SHORT
            beneficio = (operacion.precio_entrada - precio_actual) / operacion.precio_entrada * 100

        # Verificar condiciones de cierre
        if (operacion.take_profit and precio_actual >= operacion.take_profit) or \
           (operacion.stop_loss and precio_actual <= operacion.stop_loss):
            self.cerrar_operacion(precio_actual, f"TP/SL alcanzado. Beneficio: {beneficio}%")

    def abrir_operacion(self, tipo, precio, cantidad):
        """Abre una nueva operación"""
        try:
            # Calcular take profit y stop loss
            take_profit = precio * (1 + self.params.get('take_profit_porcentaje', 0.02))
            stop_loss = precio * (1 - self.params.get('stop_loss_porcentaje', 0.01))

            operacion = OperacionActiva(
                bot_id=self.bot_id,
                precio_entrada=precio,
                cantidad=cantidad,
                fecha_entrada=datetime.utcnow(),
                tipo_operacion=tipo,
                take_profit=take_profit,
                stop_loss=stop_loss,
                estado='ACTIVA'
            )
            
            # Ejecutar la orden en el exchange
            order = self.exchange.create_order(
                symbol=f"{self.activo.simbolo}/USDT",
                type='market',
                side='buy' if tipo == 'LONG' else 'sell',
                amount=cantidad
            )
            
            db.session.add(operacion)
            db.session.commit()
            self.operacion_activa = operacion
            
            self.registrar_auditoria(
                'OPERACION',
                f"Operación abierta: {tipo}",
                {
                    'precio': precio,
                    'cantidad': cantidad,
                    'take_profit': take_profit,
                    'stop_loss': stop_loss,
                    'order_id': order['id']
                }
            )
            
        except Exception as e:
            db.session.rollback()
            self.registrar_auditoria('ERROR', f"Error al abrir operación: {str(e)}")
            raise

    def cerrar_operacion(self, precio_cierre, motivo):
        """Cierra una operación activa"""
        try:
            if not self.operacion_activa:
                return

            # Ejecutar la orden de cierre en el exchange
            order = self.exchange.create_order(
                symbol=f"{self.activo.simbolo}/USDT",
                type='market',
                side='sell' if self.operacion_activa.tipo_operacion == 'LONG' else 'buy',
                amount=self.operacion_activa.cantidad
            )

            # Registrar la operación cerrada
            self.operacion_activa.estado = 'CERRADA'
            db.session.commit()

            # Calcular beneficio/pérdida
            beneficio = ((precio_cierre - self.operacion_activa.precio_entrada) / 
                        self.operacion_activa.precio_entrada * 100)

            self.registrar_auditoria(
                'OPERACION',
                f"Operación cerrada: {motivo}",
                {
                    'precio_entrada': self.operacion_activa.precio_entrada,
                    'precio_salida': precio_cierre,
                    'beneficio_porcentaje': beneficio,
                    'order_id': order['id']
                }
            )

            self.operacion_activa = None

        except Exception as e:
            self.registrar_auditoria('ERROR', f"Error al cerrar operación: {str(e)}")
            raise

    def run(self):
        """Método principal que ejecuta el bot continuamente"""
        self.running = True
        self.registrar_auditoria('INFO', "Bot iniciado")
        
        while self.running:
            try:
                # Verificar si el bot debe seguir ejecutándose
                if not self.verificar_estado_bot():
                    self.running = False
                    break

                # Obtener indicadores actuales
                indicadores = self.obtener_indicadores_actuales()

                # Si hay una operación activa, gestionarla
                if self.operacion_activa:
                    self.gestionar_operacion_activa(indicadores)
                else:
                    # Analizar condiciones para nueva operación
                    señales = self.analizar_mercado(indicadores)
                    
                    if señales['señal_compra'] and not self.operacion_activa:
                        cantidad = self.calcular_cantidad_orden(indicadores['precio'])
                        self.abrir_operacion('LONG', indicadores['precio'], cantidad)
                
                # Esperar hasta el siguiente intervalo
                time.sleep(self.interval)

            except Exception as e:
                self.registrar_auditoria('ERROR', f"Error en ciclo principal: {str(e)}")
                time.sleep(self.interval)  # Esperar antes de reintentar

        self.registrar_auditoria('INFO', "Bot detenido")

    def stop(self):
        """Detiene la ejecución del bot"""
        self.running = False
        self.registrar_auditoria('INFO', "Solicitud de detención recibida")


    def calcular_cantidad_orden(self, precio_actual):
        """Calcula la cantidad a operar basado en el balance y la gestión de riesgo"""
        try:
            balance = float(self.exchange.fetch_balance()['USDT']['free'])
            cantidad_usdt = balance * self.params.get('porcentaje_inversion', 0.1)
            return cantidad_usdt / precio_actual
        except Exception as e:
            self.registrar_auditoria('ERROR', f"Error al calcular cantidad: {str(e)}")
            raise

    def analizar_mercado(self, indicadores):
        """Analiza las condiciones actuales del mercado usando RSI, MACD y Volume
        Retorna señales de compra/venta basadas en la estrategia configurada
        """
        try:
            symbol = f"{self.activo.simbolo}/USDT"
            
            # Obtener datos históricos para el análisis
            timeframe = self.params.get('timeframe', '5m')  # Timeframe por defecto 5 minutos
            limit = 100  # Necesitamos suficientes datos para calcular indicadores
            
            ohlcv = self.exchange.fetch_ohlcv(
                symbol,
                timeframe=timeframe,
                limit=limit
            )
            
            # Convertir a DataFrame
            df = pd.DataFrame(
                ohlcv,
                columns=['timestamp', 'open', 'high', 'low', 'close', 'volume']
            )
            
            # Calcular RSI
            def calcular_rsi(datos, periodos=14):
                delta = datos['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=periodos).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=periodos).mean()
                rs = gain / loss
                return 100 - (100 / (1 + rs))
            
            # Calcular MACD
            def calcular_macd(datos, rapida=12, lenta=26, señal=9):
                exp1 = datos['close'].ewm(span=rapida, adjust=False).mean()
                exp2 = datos['close'].ewm(span=lenta, adjust=False).mean()
                macd = exp1 - exp2
                señal = macd.ewm(span=señal, adjust=False).mean()
                return macd, señal
            
            # Calcular indicadores
            df['rsi'] = calcular_rsi(df, self.params.get('rsi_periodos', 14))
            df['macd'], df['macd_signal'] = calcular_macd(
                df,
                self.params.get('macd_rapida', 12),
                self.params.get('macd_lenta', 26),
                self.params.get('macd_señal', 9)
            )
            
            # Calcular volumen promedio
            df['volumen_promedio'] = df['volume'].rolling(
                window=self.params.get('volumen_periodos', 20)
            ).mean()
            
            # Obtener últimos valores
            ultimo_rsi = df['rsi'].iloc[-1]
            ultimo_macd = df['macd'].iloc[-1]
            ultima_señal = df['macd_signal'].iloc[-1]
            ultimo_volumen = df['volume'].iloc[-1]
            volumen_promedio = df['volumen_promedio'].iloc[-1]
            
            # Condiciones de compra
            señal_compra = (
                # RSI por debajo del nivel de sobreventa
                ultimo_rsi < self.params.get('rsi_sobreventa', 30) and
                # MACD cruza por encima de la línea de señal
                ultimo_macd > ultima_señal and
                df['macd'].iloc[-2] <= df['macd_signal'].iloc[-2] and
                # Volumen superior al promedio
                ultimo_volumen > volumen_promedio * self.params.get('multiplicador_volumen', 1.5)
            )
            
            # Condiciones de venta
            señal_venta = (
                # RSI por encima del nivel de sobrecompra
                ultimo_rsi > self.params.get('rsi_sobrecompra', 70) and
                # MACD cruza por debajo de la línea de señal
                ultimo_macd < ultima_señal and
                df['macd'].iloc[-2] >= df['macd_signal'].iloc[-2]
            )
            
            # Registrar indicadores actuales
            self.registrar_auditoria(
                'ANALISIS',
                'Análisis de mercado completado',
                {
                    'rsi': ultimo_rsi,
                    'macd': ultimo_macd,
                    'macd_signal': ultima_señal,
                    'volumen': ultimo_volumen,
                    'volumen_promedio': volumen_promedio,
                    'señal_compra': señal_compra,
                    'señal_venta': señal_venta
                }
            )
            
            return {
                'señal_compra': señal_compra,
                'señal_venta': señal_venta
            }
            
        except Exception as e:
            self.registrar_auditoria('ERROR', f"Error en análisis de mercado: {str(e)}")
            # En caso de error, no generamos señales
            return {
                'señal_compra': False,
                'señal_venta': False
            }
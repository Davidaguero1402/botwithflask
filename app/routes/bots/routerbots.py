from flask import Blueprint, request, jsonify
from app import db
from models.manager import BotTradingContinuo

bot_routes = Blueprint('bot_routes', __name__)

# Diccionario para mantener las instancias de bots activos
bots_activos = {}

@bot_routes.route('/bot/iniciar', methods=['POST'])
def iniciar_bot():
    try:
        data = request.get_json()
        bot_id = data.get('bot_id')
        
        if not bot_id:
            return jsonify({'error': 'Se requiere el ID del bot'}), 400

        # Verificar si el bot ya está corriendo
        if bot_id in bots_activos and bots_activos[bot_id].is_alive():
            return jsonify({'mensaje': 'El bot ya está en ejecución'}), 400

        # Crear y iniciar el bot
        bot = BotTradingContinuo(bot_id, interval=data.get('interval', 60))
        bot.start()
        bots_activos[bot_id] = bot

        return jsonify({
            'mensaje': 'Bot iniciado correctamente',
            'bot_id': bot_id
        }), 200

    except Exception as e:
        return jsonify({
            'error': f"Error al iniciar el bot: {str(e)}"
        }), 500

@bot_routes.route('/bot/detener', methods=['POST'])
def detener_bot():
    try:
        data = request.get_json()
        bot_id = data.get('bot_id')
        
        if not bot_id:
            return jsonify({'error': 'Se requiere el ID del bot'}), 400

        if bot_id in bots_activos:
            bot = bots_activos[bot_id]
            bot.stop()
            # Esperar a que el bot se detenga
            bot.join(timeout=10)
            del bots_activos[bot_id]
            return jsonify({'mensaje': 'Bot detenido correctamente'}), 200
        else:
            return jsonify({'error': 'Bot no encontrado'}), 404

    except Exception as e:
        return jsonify({
            'error': f"Error al detener el bot: {str(e)}"
        }), 500

@bot_routes.route('/bot/estado', methods=['GET'])
def estado_bot():
    try:
        bot_id = request.args.get('bot_id')
        
        if not bot_id:
            return jsonify({'error': 'Se requiere el ID del bot'}), 400

        if bot_id in bots_activos:
            bot = bots_activos[bot_id]
            return jsonify({
                'estado': 'activo' if bot.is_alive() else 'inactivo',
                'ultima_actualizacion': bot.ultima_actualizacion if hasattr(bot, 'ultima_actualizacion') else None
            }), 200
        else:
            return jsonify({
                'estado': 'inactivo',
                'mensaje': 'Bot no encontrado en la lista de bots activos'
            }), 404

    except Exception as e:
        return jsonify({
            'error': f"Error al obtener el estado del bot: {str(e)}"
        }), 500

@bot_routes.route('/bot/actualizar', methods=['POST'])
def actualizar_bot():
    try:
        data = request.get_json()
        bot_id = data.get('bot_id')
        nuevo_intervalo = data.get('interval')

        if not bot_id or nuevo_intervalo is None:
            return jsonify({'error': 'Se requiere el ID del bot y el nuevo intervalo'}), 400

        if bot_id in bots_activos:
            bot = bots_activos[bot_id]
            bot.update_interval(nuevo_intervalo)  # Suponiendo que el bot tiene un método `update_interval`
            return jsonify({
                'mensaje': 'Configuración del bot actualizada correctamente',
                'bot_id': bot_id,
                'nuevo_intervalo': nuevo_intervalo
            }), 200
        else:
            return jsonify({'error': 'Bot no encontrado'}), 404

    except Exception as e:
        return jsonify({
            'error': f"Error al actualizar la configuración del bot: {str(e)}"
        }), 500
    
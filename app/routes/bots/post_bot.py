from flask import Blueprint, request, jsonify
from app import db
from models.manager import BotTradingContinuo
from models.bots import Bots
from models.exchanges import Exchanges
from models.activos import Activos
from models.estrategias import Estrategias

bot_routes = Blueprint('bot_routes', __name__)

@bot_routes.route('/bot/crear', methods=['POST'])
def crear_bot():
    try:
        data = request.get_json()
        
        # Validar que todos los campos requeridos estén presentes
        required_fields = ['usuario_id', 'exchange_id', 'activo_id', 'estrategia_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'El campo {field} es requerido'
                }), 400

        # Verificar que existan los registros relacionados
        exchange = Exchanges.query.get(data['exchange_id'])
        if not exchange:
            return jsonify({'error': 'Exchange no encontrado'}), 404

        activo = Activos.query.get(data['activo_id'])
        if not activo:
            return jsonify({'error': 'Activo no encontrado'}), 404

        estrategia = Estrategias.query.get(data['estrategia_id'])
        if not estrategia:
            return jsonify({'error': 'Estrategia no encontrada'}), 404

        # Crear nuevo bot
        nuevo_bot = Bots(
            usuario_id=data['usuario_id'],
            exchange_id=data['exchange_id'],
            activo_id=data['activo_id'],
            estrategia_id=data['estrategia_id']
        )

        # Guardar en la base de datos
        db.session.add(nuevo_bot)
        db.session.commit()

        # Retornar respuesta
        return jsonify({
            'mensaje': 'Bot creado exitosamente',
            'bot': {
                'id': nuevo_bot.id,
                'usuario_id': nuevo_bot.usuario_id,
                'exchange_id': nuevo_bot.exchange_id,
                'activo_id': nuevo_bot.activo_id,
                'estrategia_id': nuevo_bot.estrategia_id
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': f"Error al crear el bot: {str(e)}"
        }), 500
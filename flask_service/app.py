from flask import Flask, jsonify, request

app = Flask(__name__)

TIPOS_VALIDOS = ['email', 'sms', 'consola']

# Contador simple en memoria (en producción usaría Redis/DB)
_stats = {"notificaciones_enviadas": 0}


def _validar_payload(data):
    errores = {}
    if not data.get('telefono'):
        errores['telefono'] = 'Este campo es requerido.'
    if not data.get('titulo'):
        errores['titulo'] = 'Este campo es requerido.'
    tipo = data.get('tipo')
    if not tipo:
        errores['tipo'] = 'Este campo es requerido.'
    elif tipo not in TIPOS_VALIDOS:
        errores['tipo'] = f"Tipo inválido. Opciones válidas: {', '.join(TIPOS_VALIDOS)}."
    return errores


def _enviar_notificacion(telefono, titulo, tipo):
    mensajes = {
        'consola': f"[NOTIF-CONSOLA] {telefono} → Publicación creada: {titulo}",
        'sms':     f"[NOTIF-SMS] Enviando SMS a {telefono}: {titulo}",
        'email':   f"[NOTIF-EMAIL] Enviando email a {telefono}: {titulo}",
    }
    print(mensajes[tipo])
    _stats["notificaciones_enviadas"] += 1
    return tipo


# ============================================================================
# Endpoints de Notificaciones
# ============================================================================

@app.route('/notificaciones/', methods=['GET'])
def listar_tipos():
    return jsonify({
        "microservicio": "Notificaciones VecinoMarket",
        "version": "v2",
        "tipos_disponibles": TIPOS_VALIDOS,
        "uso": "POST /notificaciones/ con {telefono, titulo, tipo}",
        "stats": _stats,
    })


@app.route('/notificaciones/', methods=['POST'])
def enviar_notificacion():
    if not request.is_json:
        return jsonify({"error": "Content-Type debe ser application/json"}), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Cuerpo JSON inválido o vacío"}), 400

    errores = _validar_payload(data)
    if errores:
        return jsonify({"error": "Datos inválidos", "detalle": errores}), 400

    try:
        canal = _enviar_notificacion(data['telefono'], data['titulo'], data['tipo'])
        return jsonify({
            "estado": "enviado",
            "canal": canal,
            "destinatario": data['telefono'],
            "titulo": data['titulo'],
        }), 201
    except Exception as e:
        return jsonify({"error": "Error interno del microservicio", "detalle": str(e)}), 500


# ============================================================================
# Endpoint para el equipo aliado (Strangler Pattern — servicio independiente)
# ============================================================================

@app.route('/aliado/catalogo/', methods=['GET'])
def catalogo_aliado():
    """
    Endpoint público del microservicio Flask para el equipo aliado.
    Expone información del sistema de notificaciones.
    """
    return jsonify({
        "sistema": "VecinoMarket - Microservicio Notificaciones",
        "version": "2.0",
        "canales_disponibles": TIPOS_VALIDOS,
        "stats": _stats,
        "estado": "operativo",
    })


# ============================================================================
# Health check
# ============================================================================

@app.route('/health/', methods=['GET'])
def health():
    return jsonify({"status": "ok", "servicio": "flask_notifications"})


@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint no encontrado"}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Método HTTP no permitido"}), 405


if __name__ == '__main__':
    print("--- Microservicio de Notificaciones listo en :5000 ---")
    app.run(host='0.0.0.0', port=5000)

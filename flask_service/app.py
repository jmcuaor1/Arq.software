from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def health_check():
    print("👀 Alguien acaba de revisar si sigo vivo... ¡Todo en orden por aquí!")
    return jsonify({
        "microservicio": "Notificaciones de VecinoMarket",
        "estado": "Activo y escuchando",
        "mensaje": "¡Hola! Estoy listo para gestionar las alertas de la comunidad."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
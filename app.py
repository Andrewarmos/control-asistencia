from flask import Flask, request, jsonify, send_file
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Base de datos temporal
registros = []
entradas = {}  # guarda la última entrada por empleado

# Lista de empleados
empleados = [
    {"codigo": "13434", "nombre": "ANDRIW SOCHA"},
    {"codigo": "22345", "nombre": "JUAN PEREZ"},
    {"codigo": "33456", "nombre": "MARIA LOPEZ"},
    {"codigo": "44567", "nombre": "CARLOS RAMIREZ"}
]

# Página principal
@app.route("/")
def inicio():
    opciones = ""
    for emp in empleados:
        opciones += f"<option value='{emp['codigo']}'>{emp['codigo']} - {emp['nombre']}</option>"

    return f"""
    <html>
    <head>
        <title>ARMOS</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #1c1f26;
                color: white;
                text-align: center;
                padding: 20px;
            }}

            .container {{
                background: #2a2f3a;
                padding: 30px;
                border-radius: 15px;
                max-width: 400px;
                margin: auto;
            }}

            img {{ width: 150px; }}

            select {{
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border-radius: 8px;
                border: none;
            }}

            button {{
                width: 100%;
                padding: 14px;
                margin-top: 10px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }}

            .entrada {{ background-color: #27ae60; }}
            .salida {{ background-color: #e74c3c; }}
        </style>
    </head>

    <body>
        <div class="container">
            <img src="/static/logo.png">
            <h1>Bienvenido a ARMOS</h1>

            <form action="/registrar" method="post">
                <label>Empleado</label>
                <select name="codigo">{opciones}</select>

                <label>Ubicación</label>
                <select name="ubicacion">
                    <option value="Redfern">Redfern</option>
                    <option value="Mascot">Mascot</option>
                    <option value="Otro">Otro</option>
                </select>

                <button class="entrada" type="submit" name="tipo" value="entrada">
                    Marcar Entrada
                </button>

                <button class="salida" type="submit" name="tipo" value="salida">
                    Marcar Salida
                </button>
            </form>
        </div>
    </body>
    </html>
    """

# Registrar
@app.route("/registrar", methods=["POST"])
def registrar():
    codigo = request.form["codigo"]
    ubicacion = request.form["ubicacion"]
    tipo = request.form["tipo"]
    ahora = datetime.now()

    mensaje = ""
    horas_trabajadas = ""

    if tipo == "entrada":
        entradas[codigo] = ahora
        mensaje = "Feliz inicio de turno 👋"
        color = "#27ae60"

        registros.append({
            "codigo": codigo,
            "tipo": "entrada",
            "ubicacion": ubicacion,
            "hora": ahora.strftime("%Y-%m-%d %H:%M:%S"),
            "horas_trabajadas": ""
        })

    else:
        color = "#e74c3c"

        if codigo in entradas:
            inicio = entradas[codigo]
            diferencia = ahora - inicio
            horas = round(diferencia.total_seconds() / 3600, 2)
            horas_trabajadas = f"{horas} horas"
            mensaje = f"Gracias por tu ayuda 🙌<br>Trabajaste: {horas} horas"

            del entradas[codigo]
        else:
            mensaje = "No hay entrada registrada ⚠️"

        registros.append({
            "codigo": codigo,
            "tipo": "salida",
            "ubicacion": ubicacion,
            "hora": ahora.strftime("%Y-%m-%d %H:%M:%S"),
            "horas_trabajadas": horas_trabajadas
        })

    return f"""
    <html>
    <body style="font-family: Arial; background:#1c1f26; color:white; text-align:center; padding:50px;">
        
        <h1 style="color:{color};">{mensaje}</h1>

        <script>
            if (navigator.vibrate) {{
                navigator.vibrate(200);
            }}
        </script>

        <br>
        <a href="/" style="color:#3498db; font-size:18px;">Volver</a>

    </body>
    </html>
    """

# Ver registros
@app.route("/registros")
def ver_registros():
    return jsonify(registros)

# Exportar
@app.route("/exportar")
def exportar():
    df = pd.DataFrame(registros)
    archivo = "registros.xlsx"
    df.to_excel(archivo, index=False)
    return send_file(archivo, as_attachment=True)

# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
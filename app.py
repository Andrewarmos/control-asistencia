from flask import Flask, request
from datetime import datetime
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ===============================
# CONEXIÓN GOOGLE SHEETS
# ===============================
sheet = None

try:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credenciales_json = os.getenv("GOOGLE_CREDENTIALS")

    if credenciales_json:
        credenciales_dict = json.loads(credenciales_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credenciales_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Control Asistencia ARMOS").sheet1

except Exception as e:
    print("Error Google Sheets:", e)
    sheet = None

# ===============================
# DATOS
# ===============================
registros = []
entradas = {}

empleados = [
    {"codigo": "13434", "nombre": "ANDRIW SOCHA"},
    {"codigo": "22345", "nombre": "JUAN PEREZ"},
    {"codigo": "33456", "nombre": "MARIA LOPEZ"},
    {"codigo": "44567", "nombre": "CARLOS RAMIREZ"}
]

# ===============================
# HOME
# ===============================
@app.route("/")
def inicio():
    opciones = ""
    for emp in empleados:
        opciones += f"<option value='{emp['codigo']}'>{emp['codigo']} - {emp['nombre']}</option>"

    return f"""
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                font-family: Arial;
                background: linear-gradient(135deg, #1c1f26, #2c3e50);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .container {{
                background: #2b2f38;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
                text-align: center;
                width: 320px;
            }}

            img {{
                width: 120px;
            }}

            select, input {{
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                border-radius: 8px;
                border: none;
            }}

            .buttons {{
                display: flex;
                gap: 10px;
                margin-top: 10px;
            }}

            button {{
                flex: 1;
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-weight: bold;
                cursor: pointer;
            }}

            .entrada {{ background: #2ecc71; }}
            .salida {{ background: #e74c3c; }}
        </style>
    </head>

    <body>
        <div class="container">
            <img src="/static/logo.png">
            <h2>Bienvenido a ARMOS</h2>

            <form action="/registrar" method="post" enctype="multipart/form-data">

                <select name="codigo">{opciones}</select>

                <select name="ubicacion">
                    <option value="Redfern">Redfern</option>
                    <option value="Mascot">Mascot</option>
                    <option value="Otro">Otro</option>
                </select>

                <!-- FOTO -->
                <input type="file" name="foto" accept="image/*" capture="environment">

                <div class="buttons">
                    <button class="entrada" name="tipo" value="entrada">Entrada</button>
                    <button class="salida" name="tipo" value="salida">Salida</button>
                </div>

            </form>
        </div>
    </body>
    </html>
    """

# ===============================
# REGISTRAR
# ===============================
@app.route("/registrar", methods=["POST"])
def registrar():
    codigo = request.form["codigo"]
    ubicacion = request.form["ubicacion"]
    tipo = request.form["tipo"]
    ahora = datetime.now()

    # 📸 FOTO
    foto = request.files.get("foto")
    nombre_foto = ""

    if foto:
        nombre_foto = f"foto_{codigo}_{ahora.strftime('%Y%m%d%H%M%S')}.jpg"
        ruta = os.path.join("static", nombre_foto)
        foto.save(ruta)

    horas_trabajadas = ""

    if tipo == "entrada":

        if codigo in entradas:
            mensaje = "⚠️ Ya marcaste entrada"
            color = "orange"

        else:
            entradas[codigo] = ahora
            mensaje = "Feliz inicio de turno 👋"
            color = "green"

            if sheet:
                try:
                    sheet.append_row([
                        codigo,
                        tipo,
                        ubicacion,
                        ahora.strftime("%Y-%m-%d %H:%M:%S"),
                        "",
                        f"https://control-armos.onrender.com/static/{nombre_foto}"
                    ])
                except Exception as e:
                    print("Error Sheets:", e)

    else:

        if codigo not in entradas:
            mensaje = "⚠️ Primero debes marcar entrada"
            color = "orange"

        else:
            inicio = entradas[codigo]
            diferencia = ahora - inicio
            horas = round(diferencia.total_seconds() / 3600, 2)
            horas_trabajadas = f"{horas} horas"

            mensaje = f"Gracias por tu ayuda 🙌<br>Trabajaste: {horas} horas"
            color = "red"

            del entradas[codigo]

            if sheet:
                try:
                    sheet.append_row([
                        codigo,
                        tipo,
                        ubicacion,
                        ahora.strftime("%Y-%m-%d %H:%M:%S"),
                        horas_trabajadas,
                        f"https://control-armos.onrender.com/static/{nombre_foto}"
                    ])
                except Exception as e:
                    print("Error Sheets:", e)

    return f"""
    <html>
    <body style="background:#1c1f26; color:white; text-align:center; padding:50px;">
        
        <h1 style="color:{color};">{mensaje}</h1>

        <script>
            if (navigator.vibrate) {{
                navigator.vibrate(200);
            }}
        </script>

        <br><br>
        <a href="/" style="color:lightblue;">Volver</a>

    </body>
    </html>
    """

# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
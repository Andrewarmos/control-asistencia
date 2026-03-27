from flask import Flask, request, jsonify, send_file
from datetime import datetime
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets conexión (solo funcionará local por ahora)
try:
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Control Asistencia ARMOS").sheet1
except:
    sheet = None  # evita que falle en Render

# Datos en memoria
registros = []
entradas = {}

empleados = [
    {"codigo": "13434", "nombre": "ANDRIW SOCHA"},
    {"codigo": "22345", "nombre": "JUAN PEREZ"},
    {"codigo": "33456", "nombre": "MARIA LOPEZ"},
    {"codigo": "44567", "nombre": "CARLOS RAMIREZ"}
]

@app.route("/")
def inicio():
    opciones = ""
    for emp in empleados:
        opciones += f"<option value='{emp['codigo']}'>{emp['codigo']} - {emp['nombre']}</option>"

    return f"""
    <html>
    <body style="font-family: Arial; background:#1c1f26; color:white; text-align:center; padding:20px;">
        <img src="/static/logo.png" width="150">
        <h1>Bienvenido a ARMOS</h1>

        <form action="/registrar" method="post">
            <select name="codigo">{opciones}</select>

            <select name="ubicacion">
                <option value="Redfern">Redfern</option>
                <option value="Mascot">Mascot</option>
                <option value="Otro">Otro</option>
            </select>

            <button name="tipo" value="entrada">Entrada</button>
            <button name="tipo" value="salida">Salida</button>
        </form>
    </body>
    </html>
    """

@app.route("/registrar", methods=["POST"])
def registrar():
    codigo = request.form["codigo"]
    ubicacion = request.form["ubicacion"]
    tipo = request.form["tipo"]
    ahora = datetime.now()

    horas_trabajadas = ""

    if tipo == "entrada":
        entradas[codigo] = ahora
        mensaje = "Feliz inicio de turno 👋"
        color = "green"

    else:
        if codigo in entradas:
            inicio = entradas[codigo]
            diferencia = ahora - inicio
            horas = round(diferencia.total_seconds() / 3600, 2)
            horas_trabajadas = f"{horas} horas"
            mensaje = f"Gracias por tu ayuda 🙌<br>Trabajaste: {horas} horas"
            del entradas[codigo]
        else:
            mensaje = "No hay entrada registrada ⚠️"
        color = "red"

    # Guardar local
    registros.append({
        "codigo": codigo,
        "tipo": tipo,
        "ubicacion": ubicacion,
        "hora": ahora.strftime("%Y-%m-%d %H:%M:%S"),
        "horas_trabajadas": horas_trabajadas
    })

    # Guardar en Google Sheets (si está disponible)
    if sheet:
        try:
            sheet.append_row([
                codigo,
                tipo,
                ubicacion,
                ahora.strftime("%Y-%m-%d %H:%M:%S"),
                horas_trabajadas
            ])
        except:
            pass

    return f"""
    <html>
    <body style="font-family: Arial; background:#1c1f26; color:white; text-align:center; padding:50px;">
        
        <h1 style="color:{color};">{mensaje}</h1>

        <script>
            if (navigator.vibrate) {{
                navigator.vibrate(200);
            }}
        </script>

        <a href="/">Volver</a>

    </body>
    </html>
    """

@app.route("/registros")
def ver_registros():
    return jsonify(registros)

@app.route("/exportar")
def exportar():
    df = pd.DataFrame(registros)
    archivo = "registros.xlsx"
    df.to_excel(archivo, index=False)
    return send_file(archivo, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
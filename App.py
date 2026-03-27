from flask import Flask, request, jsonify
from datetime import datetime
import pandas as pd
from flask import send_file

app = Flask(__name__)

# 👇 empleados con código
empleados = {
    "EMP001": "Juan Perez",
    "EMP002": "Carlos Lopez",
    "EMP003": "Maria Gomez"
}

# 👇 ubicaciones
ubicaciones = ["Iglu Redfern", "Iglu Mascot", "Iglu Chatswood", "Domestico Carro gris","Domestico Carro blanco","Domestico Van"]

registros = []

@app.route("/")
def inicio():
    return """
    <h2>Control de Asistencia</h2>

    <label>Empleado:</label>
    <select id="empleado">
        <option value="EMP001">EMP001 - Juan Perez</option>
        <option value="EMP002">EMP002 - Carlos Lopez</option>
        <option value="EMP003">EMP003 - Maria Gomez</option>
    </select>

    <br><br>

    <label>Ubicación:</label>
    <select id="ubicacion">
        <option value="Iglu Redfern">Iglu Redfern</option>
        <option value="Iglu Mascot">Iglu Mascot</option>
        <option value="Iglu Chatswood">Iglu Chatswood</option>
        <option value="Domestico Carro Gris">Domestico Carro Gris</option>
        <option value="Domestico Carro Blanco">Domestico Carro Blanco</option>
        <option value="Domestico Van">Domestico Van</option>

    </select>

    <br><br>

    <button onclick="registrar('entrada')">Entrada</button>
    <button onclick="registrar('salida')">Salida</button>

    <script>
    function registrar(tipo){
        let empleado = document.getElementById("empleado").value;
        let ubicacion = document.getElementById("ubicacion").value;

        fetch("/registro", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                empleado: empleado,
                tipo: tipo,
                ubicacion: ubicacion
            })
        })
        .then(res => res.json())
        .then(data => {
            alert("Registrado: " + data.nombre + " en " + data.ubicacion);
        });
    }
    </script>
    """

@app.route("/registro", methods=["POST"])
def registro():
    data = request.json

    codigo = data["empleado"]

    nuevo = {
        "codigo": codigo,
        "nombre": empleados[codigo],
        "tipo": data["tipo"],
        "ubicacion": data["ubicacion"],
        "hora": datetime.now().strftime("%H:%M:%S"),
        "fecha": datetime.now().strftime("%Y-%m-%d")
    }

    registros.append(nuevo)

    return jsonify(nuevo)

@app.route("/registros")
def ver_registros():
    return jsonify(registros)


@app.route("/exportar")
def exportar():
    import pandas as pd
    from flask import send_file

    df = pd.DataFrame(registros)

    archivo = "registros.xlsx"
    df.to_excel(archivo, index=False)

    return send_file(archivo, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
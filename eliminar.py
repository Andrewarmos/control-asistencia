from flask import Flask

app = Flask(__name__)

@app.route("/")
def inicio():
    return "Servidor funcionando en Render 🚀"

if __name__ == "__main__":
    app.run()
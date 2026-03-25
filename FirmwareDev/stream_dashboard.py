from flask import Flask
from .ControlHardware import AccessStream

app = Flask(__name__)
controls = ControlHardware()

@app.route('/')
def home():
    stream = controls.ControlHardware()
    return str(stream)

if __name__ == '__main__':
    app.run(debug=True)
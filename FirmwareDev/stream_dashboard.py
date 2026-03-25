from flask import Flask
from .AccessStream import AccessStream

app = Flask(__name__)
controls = AccessStream()

@app.route('/')
def home():
    stream = controls.get_data_stream(content=["GPS", "IMU"], continous=False)
    
    return str()

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Ollama container is running", 200

if __name__ == '__main__':
    app.run()
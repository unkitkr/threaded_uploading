from flask import Flask

app = Flask(__name__)
app.secret_key = "17BTRIS002"

@app.route('/', methods= ['GET'])
def home():
    return "I'm up."


if __name__ == "__main__":
    app.run( debug=True)
from flask import Flask, jsonify, request

app = Flask(__name__)

#Secret key if I decide to use sessions anytime.
app.secret_key = "17BTRIS002"


#Home route, to verify app status.
@app.route('/', methods= ['GET'])
def home():
    return jsonify({
        "Success" : "App is running."
    })


#Generic ETL route for testing.
@app.route('/upload',methods=['POST', 'PUT'])
def upload():
    file = request.files['upload_file']
    print(file.filename)
    return jsonify({
        "Success": "Read the file"
        })




if __name__ == "__main__":
    app.run( debug=True)
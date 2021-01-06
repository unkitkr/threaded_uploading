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
    return jsonify({
        "Success": "Read the file"
    })
    

#Generic route for pausing the upload
@app.route('/pause', methods= ['GET'])
def pause_upload():
    return jsonify({
        "Success": "Paused the operation"
    }), 201


#Generic route for resuming the upload
@app.route('/resume', methods= ['GET'])
def resume_upload():
    return jsonify({
        "Success": "resumed the operation"
    }), 201

#Generic route for stopping the upload
@app.route('/stop', methods= ['GET'])
def stop_upload():
    return jsonify({
        "Success": "Stopped the operation"
    }), 201

if __name__ == "__main__":
    app.run( debug=True)
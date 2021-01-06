from flask import Flask, jsonify, request
import threading

app = Flask(__name__)

#Secret key if I decide to use sessions anytime.
app.secret_key = "17BTRIS002"

# Need to start threading.
# Using only events since we need to control thread within this particular process based on certain events.
thread = threading.Event()

# All possible thread states. At any given point of time system would be in one single state.
# Also not to be confused with OS process states.
STATES = ("READY", "PAUSED", "UPLOADING", "STOPPED", "DONE")

# By default when application starts it must be on a ready state
CURRENT_STATE = STATES[0]

# Helper functions
def is_ready():
    if CURRENT_STATE == "READY":
        return 1
    return 0
def is_paused():
    if CURRENT_STATE == "PAUSED":
        return 1
    return 0
def is_uploading():
    if CURRENT_STATE == "UPLOADING":
        return 1
    return 0
def is_stopped():
    if CURRENT_STATE == "STOPPED":
        return 1
    return 0



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
@app.route('/terminate', methods= ['GET'])
def stop_upload():
    return jsonify({
        "Success": "Terminated the operation"
    }), 201


#Get status
@app.route('/getstate', methods=["GET"])
def get_state():
    return jsonify({
        "Current State": CURRENT_STATE
    })

if __name__ == "__main__":
    app.run( debug=True)
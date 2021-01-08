from flask import Flask, jsonify, request
import threading
from sqlalchemy import create_engine, engine, MetaData
import csv
import pandas as pd

app = Flask(__name__)

#Secret key if I decide to use sessions anytime.
app.secret_key = "17BTRIS002"

# Need to start threading.
# Using only events since we need to control thread within this particular process based on certain events.
thread = threading.Event()

# All possible thread states. At any given point of time system would be in one single state.
# Also not to be confused with OS process states.
STATES = ("READY", "PAUSED", "UPLOADING", "TERMINATED", "DONE")

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
def check_if_csv(file):
    if file.split(".")[1] == "csv":
        return 1
    return 0
def change_state(state):
    global CURRENT_STATE
    CURRENT_STATE = state


#Home route, to verify app status.
@app.route('/', methods= ['GET'])
def home():
    return jsonify({
        "Success" : "App is running."
    })


#Generic ETL route for testing.
@app.route('/upload',methods=['POST', 'PUT'])
def start_etl():
    # Accessing global CURRENT_STATE
    global CURRENT_STATE

    #check if some file is already under ETL
    if is_uploading():
        return jsonify({
            "Error": "A file is under ETL"
        }), 400

    #check whether the file was sent along with form-data request
    if not "upload_file" in request.files:
        return jsonify({
            "Error": "File not recieved"
        }), 400

    if not "table_name" in request.form:
        return jsonify({
            "Error": "Table name parameter not recieved"
        }), 400
    
    file = request.files['upload_file']
    #check whether the file sent was a csv file
    if not check_if_csv(file.filename):
        return jsonify({
        "Error": "Please upload a CSV file"
        }), 400
    
    table_name = request.form["table_name"]

    #since we dont know the size of the file, better to use a buffered stream, available in the pandas library
    csv_database = create_engine('sqlite:///csv_database.db')

    metadata = MetaData(csv_database)

    #check if a table already exists with a similar name
    if csv_database.dialect.has_table(csv_database, table_name):
        return jsonify({
                "Error": "A table with similar name exists. Please try some other name."
            })

    # it is safe to spawn thread to start uploading procedure
    # this sets the internal flag to be true (Thread starts)
    thread.set()

    # Variable to keep check of any interupts (pause/terminate requests)
    initialize_thread = 1

    # At this point we may safely consider switching the state to uploading
    change_state( STATES[2] )
    #CURRENT_STATE = STATES[2]

    for frame in pd.read_csv(file, chunksize= 1000, iterator=True):
        # checkpoint, will check at any point a terminate request 
        thread.wait()
        print(frame)
        # Check if anytime the status was changed to TERMINATED
        if CURRENT_STATE == STATES[3]:
            initialize_thread = 0
            break
        try:
            frame.to_sql(table_name, csv_database, if_exists='append')
        except Exception as e:
            return jsonify({
                "Error": str(e)
            })
            break
    if initialize_thread == 0:
        CURRENT_STATE = STATES[3]
        # Drop the database table since the operation was cancled
        csv_database.execute("DROP TABLE {}".format(table_name))
        return jsonify({
        "Success": "Operation Stopped"
        }), 201
    
    change_state( STATES[4] )
    return jsonify({
        "Success": "ETL successful"
    }), 201
        

# #Generic route for pausing the upload
@app.route('/pause', methods= ['GET'])
def pause_etl():
    if CURRENT_STATE != STATES[2]:
        return jsonify({
        "Error": "No file under upload."
        }), 400
    
    # Blocking the set() called in uploading route
    thread.clear()
    # Changing the CURRENT_STATE to PAUSED
    change_state( STATES[1] )
    return jsonify({
        "Success": "Paused the operation"
    }), 201


# Generic route for resuming the upload
@app.route('/resume', methods= ['GET'])
def resume_etl():
    if not is_paused():
        return jsonify({
        "Error": "No upload process is paused."
        }), 400
    # Releasing the blocked thread
    thread.set()

    #changing CURRENT_STATUS to Uploading
    change_state( STATES[2] )
    return jsonify({
        "Success": "resumed the operation"
    }), 201

#Generic route for stopping the upload
@app.route('/terminate', methods= ['GET'])
def stop_upload():
    # check if any upload is progressing or paused
    if not is_paused() and not is_uploading():
        return jsonify({
        "Error": "No operation under progress"
        }), 400

    # Reset the internal flag and set the state to TERMINATED to triger the logic on line 114
    thread.set()
    change_state( STATES[3] )
    print (CURRENT_STATE)
    return jsonify({
        "Success": "Terminated the operation"
    }), 201


#Get status
@app.route('/getstate', methods=["GET"])
def get_state():
    global CURRENT_STATE
    return jsonify({
        "Current State": CURRENT_STATE
    })

if __name__ == "__main__":
    app.run(threaded = True)
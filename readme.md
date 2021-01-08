# Simple threaded ETL
#### This is a simple API having a threaded architecture for concurrent API calls.

#### Features:

 1. Stop/pause/resume ETL operation when required.
 2. Uses SQLite database for storing data (can be customized).


#### Dependencies
1. Flask (  `pip install flask`)
2. SQLAlchemy ( `pip install SQLAlchemy` )
3. Pandas ( `pip install pandas` )

### Starting the development server
    python app.py  
    python3 app.py (linux)

### API Structure

#### 🔼 Uploading Files

    /upload

##### `POST`: Payload (form data):

|Parameter| Type |Required|Sample Value|
|--|--|--|--|
|upload_file| file| Yes| csv file |
|table_name| String | Yes| SampleTable |

###### Note:  Do not start table name with a digit.

#### 🔪 Terminate ongoing process

    /terminate

##### `GET`: Payload :
##### None

#### ⏸ Pause ongoing process

    /pause

##### `GET`: Payload :
##### None

#### ▶ Resume paused process

    /resume

##### `GET`: Payload :
##### None


#### 🔢  Get current state of API

    /getstate

##### `GET`: Payload :
##### None

#### 🏠  Home

    /home

##### `GET`: Payload :
##### None


#### 🔗  Links 
##### `Docker image`:  https://hub.docker.com/repository/docker/unkitkr/threaded_etl
##### `Github`:  https://github.com/unkitkr/threaded_uploading
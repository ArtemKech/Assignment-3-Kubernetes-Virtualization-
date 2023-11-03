from flask import Flask, jsonify
import time
import socket
from redis import Redis
import os

redis_host = os.environ.get('REDIS_HOST')
redis_port = int(os.environ.get('REDIS_PORT'))
redis = Redis(host=redis_host, port=redis_port)
app = Flask(__name__)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello! I have been seen {0} times'.format(redis.get('hits'))

@app.route("/status", methods=['GET', 'POST'])
def status():
    current_time = time.ctime()
    return jsonify({"status": "Server is up and running", "Time of Call": current_time})


# Function to fetch hostname and ip
def fetchostdetails():
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    return str(hostname), str(host_ip)


@app.route("/host")
def details():
    hostname,ip = fetchostdetails()
    response = {"Response from host": f"{hostname} with IP Address {ip}"}
    return jsonify(response)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)


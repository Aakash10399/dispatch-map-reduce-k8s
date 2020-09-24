import os
from flask import Flask, request
from werkzeug.utils import secure_filename
import requests
from kubernetes import client, config
import string
import random
import threading

UPLOAD_FOLDER = '/datafiles/'
ALLOWED_EXTENSIONS = {'in'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class executeTask(threading.Thread):
    def __init__(self, ip, inputfile):
        threading.Thread.__init__(self)
        self.ip = ip
        self.inputfile = inputfile
        self.response = "- 0"
    def run(self):
        try:
            self.response = requests.post( "http://" + self.ip + ":5001/", data = { "inputfile": self.inputfile } ).text
        except Exception as e:
            print(e)
            self.response = "- 0"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "File not uploaded as part of request."
        file = request.files['file']
        if file.filename == '':
            return "File not uploaded as part of request."
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            config.load_incluster_config()
            v1 = client.CoreV1Api()
            pods_response = v1.list_pod_for_all_namespaces(watch=False)
            pods = []
            for pod in pods_response.items:
                if pod.metadata.namespace == "default" and ("app" in pod.metadata.labels) and pod.metadata.labels["app"] == "wordcount":
                    pods.append( pod.status.pod_ip )

            CHUNK_SIZE = os.stat(UPLOAD_FOLDER + filename).st_size // (len(pods) - 1)
            file_number = 0
            job_id = ''.join(random.choices(string.ascii_lowercase, k = 6))
            jobs = []
            with open(UPLOAD_FOLDER + filename) as f:
                chunk = f.read(CHUNK_SIZE)
                while chunk:
                    with open(UPLOAD_FOLDER + job_id + '_' + str(file_number) + '.in', 'w') as chunk_file:
                        if file_number < len(pods):
                            jobs.append( executeTask( pods[file_number], job_id + '_' + str(file_number) + '.in' ) )
                            jobs[-1].start()
                        chunk_file.write(chunk)
                    file_number += 1
                    chunk = f.read(CHUNK_SIZE)

            words = dict()

            for job in jobs:
                job.join()
                for item in job.response.split("\n"):
                    word, count = item.split(" ")
                    count = int(count)
                    if word in words:
                        words[word] += count
                    else:
                        words[word] = count

            output = ""
            for key, value in words.items():
                output = output + key + " " + str(value) + "<br>"

            return output
        return "File extension not allowed."

    return '''
    <!doctype html>
    <title>Upload Data</title>
    <h1>Upload Data</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
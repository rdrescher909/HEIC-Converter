import os
import tempfile
import shutil
import zipfile

from gevent.pywsgi import WSGIServer
import requests
from flask import Flask, request, render_template, send_file, after_this_request
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener() # Give PIL access to HEIF

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['heic', 'heif'])

app = Flask(__name__)

def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_all_files(working_dir):
    for item in os.listdir(working_dir):
        filename, ext = os.path.splitext(item)
        image = Image.open(os.path.join(working_dir, item))
        image.save(os.path.join(working_dir, filename + ".png"))

def zip_all_files(work_dir):
    with zipfile.ZipFile(os.path.join(work_dir, "output.zip"), "w") as zip:
        for file in os.listdir(work_dir):
            print(os.listdir(work_dir))
            _, ext = os.path.splitext(file)
            if ext.lower() == ".png":
                zip.write(os.path.join(work_dir, file), file)


@app.route("/", methods=["GET", "POST"])
def home():
    work_dir = tempfile.TemporaryDirectory()
    output_file_path = os.path.join(work_dir.name, "output.zip")

    if request.method == "POST":
        if 'file' not in request.files:
            return "No image provided"
        files = request.files.getlist('file') # Get all of the files
        if files[0].filename == "": # Check if the first one is empty
            return "No image provided"
        for file in files:
            if file and is_allowed_file(file.filename):
                output_name = os.path.join(work_dir.name, file.filename)
                file.save(output_name)
    
    if request.method == "GET":
        url = request.args.get("url", type=str)
        if not url:
            return render_template('index.html')
        # Download file from given url
        response = requests.get(url, stream=True)
        with open(os.path.join(work_dir.name ,"item.heic"), "wb") as fp:
            shutil.copyfileobj(response.raw, file)
        del response
    
    convert_all_files(work_dir.name)
    zip_all_files(work_dir.name)

    @after_this_request
    def cleanup(response):
        work_dir.cleanup()
        return response

    return send_file(output_file_path, mimetype="application/zip")

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), app)
    http_server.serve_forever()
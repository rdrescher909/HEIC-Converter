import os
import tempfile
from gevent.pywsgi import WSGIServer
import requests
import shutil

from flask import Flask, request, render_template, send_file, after_this_request
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener() # Give PIL access to HEIF

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['heic', 'heif'])

app = Flask(__name__)

def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_file(output_dir, input_file):
    image = Image.open(input_file)
    image.save(f"{output_dir}/converted.png")

@app.route("/", methods=["GET", "POST"])
def home():
    work_dir = tempfile.TemporaryDirectory()
    file_name = "converted"
    input_file_path = os.path.join(work_dir.name, file_name)
    output_file_path = os.path.join(work_dir.name, file_name + ".png")

    if request.method == "POST":
        if 'file' not in request.files:
            return "No image provided"
        file = request.files['file']
        if file.filename == "":
            return "No image provided"
        if file and is_allowed_file(file.filename):
            file.save(input_file_path)
    
    if request.method == "GET":
        url = request.args.get("url", type=str)
        if not url:
            return render_template('index.html')
        # Download file from given url
        response = requests.get(url, stream=True)
        with open(input_file_path, "wb") as fp:
            shutil.copyfileobj(response.raw, file)
        del response
    
    convert_file(work_dir.name, input_file_path)

    @after_this_request
    def cleanup(response):
        work_dir.cleanup()
        return response

    return send_file(output_file_path, mimetype="image/png")

if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), app)
    http_server.serve_forever()
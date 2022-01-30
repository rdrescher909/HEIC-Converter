import os
import tempfile
import zipfile

from gevent.pywsgi import WSGIServer
from flask import Flask, request, render_template, send_file, after_this_request
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener() # Give PIL access to HEIF

ALLOWED_EXTENSIONS = set(['heic', 'heif'])

app = Flask(__name__)

def is_allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_all_files(working_dir):
    """Converts all files in working_dir to pngs, assumes all files are of the proper type
    Args:
        working_dir (str, path): The working directory
    """
    for file in os.listdir(working_dir):
        original_name, _ = os.path.splitext(file)
        image = Image.open(os.path.join(working_dir, file))
        image.save(os.path.join(working_dir, original_name + ".png"))
        del image

def zip_all_files(work_dir):
    """Zips all png files in work_dir into an archive called output.zip
    Args:
        work_dir (str, path): The working directory
    """
    with zipfile.ZipFile(os.path.join(work_dir, "output.zip"), "w") as zip:
        for file in os.listdir(work_dir):
            _, ext = os.path.splitext(file)
            if ext.lower() == ".png":
                file_path = os.path.join(work_dir, file)
                zip.write(file_path, file)


@app.route("/", methods=["GET", "POST"])
def home():
    work_dir = tempfile.TemporaryDirectory()
    output_file_path = os.path.join(work_dir.name, "output.zip")

    if request.method == "POST":
        if 'file' not in request.files: # No files given in the POST at all
            return "No image provided"
        files = request.files.getlist('file') # Get all of the files, contains one entry with no filename if no files were given
        if files[0].filename == "": # Check if the first one is empty
            return "No image provided"
        for file in files:
            if file and is_allowed_file(file.filename):
                output_name = os.path.join(work_dir.name, file.filename) 
                file.save(output_name) # Save the file to the temp dir
    
    if request.method == "GET":
        return render_template("index.html")
    
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
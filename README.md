# About

A simple web interface that allows you to upload an heic image and it will return you a converted png of that image.

## Setup and Install

If you'd like to run this on your own machine, you'll need to clone the repository install the dependencies.

### macOS/Linux

`python3 -m pip install -r requirements.txt`

### Windows

`py -m pip install -r requirements.txt`

Note that [pillow-heif](https://pypi.org/project/pillow-heif/) may need to build from source on your machine.

## Notes

This project was made with Google Cloud Run in mind, therefore the limits stated on the `index.html` page are specific to cloud run, if run on your own server, you can submit and receive back as much data as you like.

## Contributing

If you'd like to contribute, feel free to submit a pull request.





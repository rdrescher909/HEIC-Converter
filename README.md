# About

A simple web interface that allows you to upload heic images and it will return you a zip file of converted png images.

## Setup and Install

If you'd like to run this on your own machine, you'll need to clone the repository install the dependencies.

### macOS/Linux

`python3 -m pip install -r requirements.txt`

### Windows

`py -m pip install -r requirements.txt`

Note that [pillow-heif](https://pypi.org/project/pillow-heif/) may need to build from source on your machine.

## Notes

This project was made with Google Cloud Run in mind, therefore the limits stated on the `index.html` page are specific to Cloud Run ([Source](https://cloud.google.com/run/quotas)), if run on a virtual machine instead, it can handle as much data as you'd like to throw at it.

## Contributing

If you'd like to contribute, feel free to submit a pull request.


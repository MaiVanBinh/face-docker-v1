# FACE RECOGNITION PROJECT

* [Requirements](#requirements)
* [Install (Linux)](#install-linux)
* [Install (Windows)](#install-windows)
* [Test project running](#test-project-running)

## Requirements
- Python 3.7
- Virtualenv
- Python-pip
- macOS, Linux or Windows 10

## Install (Linux)

Download source code project from git and change dir to project folder
```shell
git clone https://github.com/gemisolocnv/face_recognition.git

cd face_recognition
```

Most of the necessary libraries were installed and stored in `venv` folder, so what we need is installing virtualenv to use this enviroment. Install virtualenv:
```shell
python -m venv venv
```

Run source in venv
```shell
source venv/bin/activate

# for deactivate use command `deactivate`
```

Update pip and install packages
```shell
python -m pip install --upgrade pip

pip install -r requirements.txt
```

Install package mongo_uri parse srv
```shell
python -m pip install "pymongo[srv]"
```

Copy file environment
```shell
cp .env.example .env
```

Change infomation in enviroment file
```dotenv
APP_NAME="Face Recognition" # change your name app
APP_URL=http://127.0.0.1:5000/ # change to your api url

FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000 # change port
FLASK_APP=main.py

# "production" or "development" enviroment
FLASK_ENV=development

# 1 (debug) or empty (not debug)
FLASK_DEBUG=1
#FLASK_DEBUG=

# only choose 1 in 2 options: MONGO_URI or MONGO_HOST (host, port,...) info
MONGO_URI=

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USERNAME=
MONGO_PASSWORD=
MONGO_DATABASE=face_recognition

MAX_FACE_REGISTER=20
```

Run project
```shell
python -m flask run
# or
flask run

# if has error run: `python main.py` for debug
# if run with production, please setup and run with `gunicorn`
```

## Install (Windows)

Install python 3.7 on `https://www.python.org/downloads/`

Download source code project from git and change dir to project folder
```shell
git clone https://github.com/gemisolocnv/face_recognition.git
```

Update pip and install packages
```shell
python -m pip install --upgrade pip

pip install -r requirements.txt
```

*NOTE: IF ANY ERROR OCCURS during install package in requirements file, 
remove "mxnet~=1.8.0.post0 in requirements file and re-run: `pip install -r requirements.txt`, 
and after install mxnet: `pip install mxnet==1.8.0 -f https://dist.mxnet.io/python`

Install package mongo_uri parse srv
```shell
pip install "pymongo[srv]"
```

Copy file environment with command below or use File Manager
```shell
cp .env.example .env
```

Change infomation in enviroment file
```dotenv
APP_NAME="Face Recognition" # change your name app
APP_URL=http://127.0.0.1:5000/ # change to your api url

FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5000 # change port
FLASK_APP=main.py

# "production" or "development" enviroment
FLASK_ENV=development

# 1 (debug) or empty (not debug)
FLASK_DEBUG=1
#FLASK_DEBUG=

# only choose 1 in 2 options: MONGO_URI or MONGO_HOST (host, port,...) info
MONGO_URI=

MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_USERNAME=
MONGO_PASSWORD=
MONGO_DATABASE=face_recognition

MAX_FACE_REGISTER=20
```

Run project
```shell
python -m flask run
# or
flask run

# if has error run: `python main.py` for debug

# if run with production, please setup and run with `gunicorn`
```

## Test project running

Open api url on your favorite browser

[http://127.0.0.1:5000](http://127.0.0.1:5000) example api url run in local

The website will show:
```json
{
  "author": "S3Lab", 
  "description": "Face recognition", 
  "project": "S-Face", 
  "version": "1.0.0"
}
```

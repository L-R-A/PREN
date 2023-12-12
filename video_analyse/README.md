# Video-Analyse

## Setup

Clone the project:

```bash
git clone git@github.com:SirLRA/PREN.git
```

Activate python enviroment

```bash
source ./video_analyse/bin/activate
```

## Run script

```bash
python3 ./video_analyse/src/app.py
```

## Run video stream server
```bash
export FLASK_APP=video_stream_server.py
export FLASK_ENV=development
flask run

sudo lsof -PiTCP -sTCP:LISTEN
``````




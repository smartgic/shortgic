[![Build Status](https://travis-ci.com/smartgic/shortgic.svg?branch=main)](https://travis-ci.com/github/smartgic/shortgic) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/shortgic/pulls)[![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.gg/Vu7Wmd9j)

# Shortgic

A minimalist, and lightweight URL shortener using FastAPI and SQLAlchemy and SQLite3.

## Installation

Shortgic requires few Python libraries such as FastAPI, SQLAlchemy for the database integration and Uvicorn for serving the application.

```bash
$ python3 -m venv ~/venvs/shortgic
$ source ~/venvs/shortgic/bin/activate
$ git clone https://github.com/smartgic/shortgic.git
$ cd shortgic
$ pip install -r requirements.txt
$ uvicorn app.main:app
```

A Docker image is availble on Docker Hub *(cf. https://hub.docker.com/repository/docker/smartgic/shortgic)*

```bash
$ docker run -d -n shortgic -p 8000:8000 smartgic/shortgic:latest
```

## Usage

As any FastAPI project, a Swagger documention is available at http://127.0.0.1:8000/docs

Create a basic URL shortened.
```bash
$ curl -s -X POST http://127.0.0.1:8000 -d '{"target": "https://smartgic.io"}'
{
  "link": "BEN9S"
}
```

Create an URL shortened with extras information, `extras` must be a JSON dictionary. 
```bash
$ curl -s -X POST http://127.0.0.1:8000 -d '{"target": "https://smartgic.io", "extras": {"version": "0.2b-1", "validated": true}}'
{
  "link": "UY9JN"
}
```

Redirection to the target URL, the `-L` option should be used with `curl` to follow the `302` redirection.
```bash
$ curl -s -X GET http://127.0.0.1:8000/UY9JN -L
```

Get link information, this will output the `target` and the `extras` information.
```bash
$ curl -s -X GET http://127.0.0.1:8000/UY9JN/info
{
  "target": "https://smartgic.io",
  "extras": {
    "version": "0.2b-1",
    "validated": true
  }
}
```

Remove permanently an URL shortened from the database.
```bash
$ curl -s -X DELETE http://127.0.0.1:8000/UY9JN
```
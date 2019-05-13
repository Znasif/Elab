# Elab
====================

A Python Flask RESTapi that's ready to run on Heroku.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Development Setup

* `pipenv install`

* `pipenv shell`

* `python app.py`

## Screenshot

[comment]: <> (https://i.imgur.com/IkkvQX0.png)
![screenshot](https://imgflip.com/gif/30sqso)

## Deploy

* `heroku create`

* `heroku addons:create heroku-postgresql:hobby-dev`

* `git push heroku master`

* Note: make sure you run `db.create_all()` to create the tables.

## Contributors

* [Znasif](https://linkedin.com/in/nasif-zaman-9683309a/)

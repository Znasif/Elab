docker build -t znasif/elab .
heroku container:push web --app elab-ai
heroku container:release web --app elab-ai


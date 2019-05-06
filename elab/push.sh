docker build -t znasif/elab .
heroku container:push web --app elab-ai
heroku container:release web --app elab-ai

# conda install -c conda-forge -y \
#     conda-build \
#     flask \
#     flask-cors \
#     flask-restful \
#     flask-sqlalchemy \
#     google-cloud-bigquery \
#     google-cloud-storage \
#     passlib \
#     pandas \
#     keras \
#     tensorflow \
#   && conda clean --yes --tarballs --packages \
#   && conda build purge-all

# pip install --no-cache-dir firebase-admin

# gcloud builds submit --tag gcr.io/elab-237906/elab
# gcloud beta run deploy --image gcr.io/elab-237906/elab

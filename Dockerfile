FROM frolvlad/alpine-miniconda3:python3.6

RUN conda install -c conda-forge -y \
    conda-build \
    flask \
    flask-cors \
    flask-restful \
    flask-sqlalchemy \
    google-cloud-bigquery \
    google-cloud-storage \
    passlib \
    pandas \
    keras \
    tensorflow \
  && conda clean --yes --tarballs --packages \
  && conda build purge-all

RUN pip install --no-cache-dir firebase-admin
RUN pip install Flask gunicorn

WORKDIR /tmp
COPY app/ .
EXPOSE 8080

CMD exec gunicorn -b 0.0.0.0:8080 --workers 1 --threads 8 app:app
# CMD exec python app.py
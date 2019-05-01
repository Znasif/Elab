FROM frolvlad/alpine-miniconda3

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

WORKDIR /tmp
COPY app/ .
COPY Logs/ Logs/
EXPOSE 33507

CMD ["python", "modules.py"]
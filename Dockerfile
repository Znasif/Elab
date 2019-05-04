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
EXPOSE 33507

CMD ["python", "__init__.py"]
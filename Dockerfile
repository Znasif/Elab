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

WORKDIR /tmp
ADD . /Elab
WORKDIR /Elab/app

EXPOSE 33507

CMD ["python", "__init__.py"]
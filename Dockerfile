FROM frolvlad/alpine-miniconda3

RUN conda install -c conda-forge -y \
    flask \
    flask-restful \
    flask-sqlalchemy \
    passlib \
    pandas \
    keras \
    tensorflow \
  && conda clean --yes --tarballs --packages --source-cache

WORKDIR /tmp
ADD . /Elab
WORKDIR /Elab/app

EXPOSE 33507

CMD ["python", "__init__.py"]
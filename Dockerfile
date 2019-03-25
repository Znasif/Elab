FROM frolvlad/alpine-miniconda3

RUN conda install -y \
    flask \
    h5py \
    pandas \
    keras \
    tensorflow \
    tqdm \
  && conda clean --yes --tarballs --packages --source-cache

RUN pip install Flask-RESTful
RUN pip install Flask-HTTPAuth
RUN pip install Flask-SQLAlchemy
RUN pip install passlib

WORKDIR /tmp
ADD . /Elab
WORKDIR /Elab/app

EXPOSE 5000

CMD ["python", "__init__.py"]
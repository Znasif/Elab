FROM ubuntu

RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
  && rm -rf /var/lib/apt/lists/*

RUN curl -qsSLkO \
    https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-`uname -p`.sh \
  && bash Miniconda3-latest-Linux-`uname -p`.sh -b \
  && rm Miniconda3-latest-Linux-`uname -p`.sh

ENV PATH=/root/miniconda3/bin:$PATH

RUN conda install -y \
    flask \
    h5py \
    pandas \
    keras \
    tensorflow \
    tqdm \
  && conda clean --yes --tarballs --packages --source-cache

RUN pip install Flask-OAuthlib
RUN pip install Flask-RESTful

WORKDIR /tmp
ADD . /Elab
WORKDIR /Elab

CMD ["python", "test.py"]
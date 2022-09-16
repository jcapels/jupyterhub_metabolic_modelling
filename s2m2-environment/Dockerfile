# Based on the JupyterHub docker image that is
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
# Ubuntu 16.04 (xenial) from 2017-07-23
# https://github.com/docker-library/official-images/commit/0ea9b38b835ffb656c497783321632ec7f87b60c

# This has been extensively modified by C.Woods, so blame him
# for any errors or problems

# Start from ubuntu :-)
FROM ubuntu@sha256:84c334414e2bfdcae99509a6add166bbb4fa4041dc3fa6af08046a66fed3005f

LABEL maintainer="João Capela <joao.capela@ceb.uminho.pt>"

# <----- credits to Christopher Woods <Christopher.Woods@bristol.ac.uk> from here ------>

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get -yq dist-upgrade \
 && apt-get install -yq --no-install-recommends \
    git \
    sudo \
    locales \
    ca-certificates \
    fonts-liberation \
    wget \
    bzip2 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Install Tini - this is a tiny init system that is useful
# for containers that need to start many processes
RUN wget --quiet https://github.com/krallin/tini/releases/download/v0.10.0/tini && \
    echo "1361527f39190a7338a0b434bd8c88ff7233ce7b9a4876f3315c22fce7eca1b0 *tini" | sha256sum -c - && \
    mv tini /usr/local/bin/tini && \
    chmod +x /usr/local/bin/tini

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=s2m2 \
    NB_UID=1000 \
    NB_GID=100 \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

ENV PATH=$CONDA_DIR/bin:$PATH \
    HOME=/home/$NB_USER

ADD fix-permissions /usr/local/bin/fix-permissions

# Create jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN useradd -m -s $SHELL -N -u $NB_UID $NB_USER

RUN $SHELL fix-permissions $HOME

# Install a mini anaconda for Python 3. This is needed as
# JupyterHub is best installed from conda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-py37_4.12.0-Linux-x86_64.sh -O miniconda.sh && \
    chmod a+x miniconda.sh && \
    ./miniconda.sh -b -p /opt/conda && \
    chown -R $NB_USER:$NB_GID /opt/conda && \
    rm miniconda.sh

RUN $SHELL fix-permissions /opt/conda

# Configure container startup. This starts the tini init system
# telling it to run the start_notebook.sh as the primary process.
# This is a script provided by JupyterHub that will start different
# processes depending on whether this is the hub or a notebook
ENTRYPOINT ["tini", "--"]
CMD ["start-notebook.sh"]

# Make sure that the jupyter notebook port is accessible from
# outside the container
EXPOSE 8888

# Now copy in all of the files that are needed to run JupyterHub
# This includes jupyter-notebook_config.py that is used to
# configure the jupyterhub server
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/
RUN $SHELL fix-permissions /etc/jupyter/

# Do all conda work as $NB_USER
USER $NB_USER
WORKDIR $HOME

# Install Jupyter Notebook and Hub and other useful packages
RUN conda config --system --prepend channels conda-forge && \
    conda config --system --set auto_update_conda false && \
    conda config --system --set show_channel_urls true && \
    conda install --quiet --yes notebook jupyterhub jupyterlab


# Now installed tmpauthenticator. This is a module that allows anybody
# to log into this jupyterhub using a hidden URL
RUN pip install jupyterhub-tmpauthenticator

# <---------- to here ------------>

COPY ./requirements.txt /home/requirements.txt
RUN pip install -r /home/requirements.txt
RUN pip install tornado

USER root

COPY ./cplex/ /home/cplex/
COPY ./etfl /home/etfl/
RUN python /home/cplex/python/setup.py install
RUN cd /home/etfl/ && python setup.py install
RUN cd ../../
USER $NB_USER
# Reinstall an older version of tornado as tornado 5 doesn't work
# with the current version of jupyterhub
# Also clean up after conda, including clearing the cache
RUN conda clean -tipsy && \
    rm -rf $CONDA_DIR/share/jupyter/lab/staging && \
    rm -rf $HOME/.cache $HOME/.jupyter $HOME/.local/share/jupyter

USER root
RUN $SHELL fix-permissions $CONDA_DIR
USER $NB_USER

# End as the User to make sure that we don't
# accidentally run the container as root
USER $NB_USER

ARG BASE_IMAGE=jupyterhub/jupyterhub

FROM ${BASE_IMAGE}

RUN pip3 install --no-cache jupyterhub-nativeauthenticator
RUN pip3 install --no-cache --upgrade jupyter
RUN pip3 install --no-cache dockerspawner
RUN pip3 install --no-cache oauthenticator

RUN mkdir /home/configs

ENV DOCKER_NETWORK_NAME="jupyterhub_network"

EXPOSE 8000

CMD ["jupyterhub", "-f", "/home/configs/jupyterhub_config.py"]

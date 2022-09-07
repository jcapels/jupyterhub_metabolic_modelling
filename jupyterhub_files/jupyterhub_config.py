import os, nativeauthenticator
# Configuration file for Jupyter Hub
from jupyter_client.localinterfaces import public_ips

# https://blog.umd.edu/crstl/useful-links/how-to-setup-and-use-your-own-conda-environment-in-jupyterhub/

ip = public_ips()[0]

c.JupyterHub.hub_ip = ip
c = get_config()

# # spawn with Docker
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

network_name = os.environ['DOCKER_NETWORK_NAME']

c.DockerSpawner.cmd = "jupyterhub-singleuser"
c.DockerSpawner.image = "cplex_mewpy"
c.DockerSpawner.network_name = network_name
c.DockerSpawner.extra_host_config = {'network_mode': network_name}
c.DockerSpawner.extra_create_kwargs = {'user': 's2m2'}

c.DockerSpawner.http_timeout = 60
c.DockerSpawner.start_timeout = 60

c.JupyterHub.authenticator_class = 'nativeauthenticator.NativeAuthenticator'

c.JupyterHub.template_paths = [f"{os.path.dirname(nativeauthenticator.__file__)}/templates/"]

c.Authenticator.admin_users = {"admin"}




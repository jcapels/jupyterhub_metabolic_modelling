
HOME_DIR=/home/joao/Desktop/jupyterhub_metabolic_modelling
PORT=8000:8000

cd s2m2-environment
docker build . -t cplex_mewpy

cd ../jupyterhub_files

docker network create --driver bridge jupyterhub_network

mkdir -pv ./configs
chmod -R 777 ./configs

cp jupyterhub_config.py ./configs/jupyterhub_config.py

docker build -t qw/jupyterhub .

docker run -d --name jupyterhub -p $PORT --network jupyterhub_network -v /var/run/docker.sock:/var/run/docker.sock \
-v $HOME_DIR/jupyterhub_files/configs:/home/configs/ -v $HOME_DIR/s2m2_workdir/:/home/s2m2/ qw/jupyterhub

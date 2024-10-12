# Docker app to create a jupyterhub instance for multiple users - metabolic modelling
A jupyter hub instance for metabolic modelling using mewpy, troppo, cobra, etfl and cplex. 

# Requirements
- Docker
- etfl and cplex folders should be pasted here in the root folder (the one with this project)

# Docker image for the cplex_mewpy environment 

You can find the Dockerfile for this image in the s2m2-environment folder

The ETFL repository should be downloaded from https://github.com/EPFL-LCSB/etfl.git .
CPLEX should be downloaded and added to the this project directly. Not to any other folder. It is mandatory that the cplex folder should be called "cplex".

# RUN

Just change the HOME_DIR in the **run_jupyter_hub.sh** for the complete path of this directory and you're all set.

```bash
sh run_jupyter_hub.sh
```

# Create an admin account
Create an admin account by signing up with the username **admin** and a password of your choice. Log in and start coding
and managing the jupyterhub in your server.

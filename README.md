# Exploratory and Predictive Data Analysis of the COVID-19 pandemic

### Using Docker to set up a local development environment (recommended)

This method is recommended as you do not need anything installed on your system, except Docker. You don't even need Python installed.

**Step 1** - Install and set up Docker on your system. You can follow the installation instructions from [here](https://docs.docker.com/get-docker/)

**Step 2** - Clone this Github repository on your system and change the working directory to the covid-19 repo with the following set of commands

```
git clone https://github.com/anandrajaram21/covid-19.git
cd covid-19
```

**Step 3** - Use the following command to build a docker image with the provided Dockerfile. 

```
docker build -t covid . # Do not forget the '.' at the end
```

If this is your first time running this command, it might take some time to run as it has to fetch a base image from docker hub. Do not get scared if you see some red text appear on the screen. Pay no attention to it

You can use this command instead if you don't want to build the image manually. This command pulls a Docker image from Docker Hub, that contains all the dependencies required to run the Python files and Jupyter Notebooks.

```
docker pull anandrajaram21/covid-19:dev
```

**Step 4** - Run the docker container with the following command

```
docker run -it --name <use any name> -p 8888:8888 -v "$PWD":/home/jovyan/work covid bash
# Replace "covid" in the command with "anandrajaram21/covid" if you pulled the image from Docker Hub
```

This command will start a terminal session in the Docker container. From here, you can now run `jupyter lab` or `jupyter notebook` depending on which one you prefer.

**Step 5** - Once you are in the Jupyter Lab/Notebook interface, navigate to the "work" folder. You should see all the project files present. The main project files are present in src/python_files and src/jupyter_notebooks. The other files are stuff you don't have to worry about. The changes made to the files are reflected on the host system, so you can just edit the files you need and exit.

**Step 6** - Once you are done making changes to the files, run `exit` in the Docker container's terminal, to come out of the Docker container. Then run the following command to stop the container.

```
docker stop <name provided in Step 4>
```

**Step 7** - If you want to resume editing your files at some point in the future, all you have to do is run the following commands.

```
docker start <name provided in Step 4>
docker exec -it <name provided in Step 4> bash
```

Executing these commands gives you a terminal session in the Docker container. You can now repeat steps from Step 5 onwards.

### Alternative (Using python venv)

Replace python3 with python in the following commands depending on which OS you are using.

**Step 1** - Run the following command to create a python3 venv

```
python3 -m venv covid_env
```

**Step 2** - Activate the venv, install all dependencies with the following commands.

```
# The activation command differs with the OS you are using. Check the Python documentation for more information.
source covid_env/bin/activate
pip install -r requirements.txt
```

**Step 3** - Run the command `jupyter lab` in the terminal to fire up a jupyter lab server.

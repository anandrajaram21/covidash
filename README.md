# Exploratory and Predictive Data Analysis of the COVID-19 pandemic

## How to reproduce the project on a local environment

- There are 2 methods that you can use to setup a local development environment on your computer
  1. Using Docker (recommended)
  2. Using python venv

### Using Docker to set up a local development environment (recommended)

- This method is recommended as you do not need anything installed on your system, except Docker. You don't even need Python installed.

**Step 1** - Install and set up Docker on your system. You can follow the installation instructions from [here](https://docs.docker.com/get-docker/)

**Step 2** - Clone this Github repository on your system and change the working directory to the covid-19 repo with the following set of commands

```
git clone https://github.com/anandrajaram21/covid-19.git
cd covid-19
```

**Step 3** - Use the following command to build a docker image with the provided Dockerfile. 

```
docker build -t covid:latest . # Do not forget the '.' at the end
```

If this is your first time running this command, it might take some time to run as it has to fetch a base image from docker hub. Do not get scared if you see some red text appear on the screen. Pay no attention to it

You can use this command instead if you dont want to build the image manually. This command pulls a Docker image from Docker Hub, that contains all the dependencies for the application

```
docker pull anandrajaram21/covid-19:latest
```

**Step 4** - Run the docker container with the following command

```
docker run --rm -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v "$PWD":/home/jovyan/work covid
# Replace "covid" in the command with "anandrajaram21/covid" if you pulled the image from Docker Hub
```

This command fires up a docker container that contains a jupyter lab server. The terminal will show you 2 links that you can use to navigate to the jupyter lab server. Click on the second link, and jupyter lab should open up in your browser. 

**Step 5** - Once you are in the Jupyter Lab interface, navigate to the "work" folder. You should see all the project files present. The main project files are present in src/python_files and src/jupyter_notebooks. The other files are stuff you dont have to worry about.

**Step 6** - If you want to run the streamlit web app, its very easy.

  **Step 6(a)** - Open the "Launcher" in Jupyter Lab, and fire up a terminal from there. This terminal allows you to execute commands in the docker container

  **Step 6(b)** - Run the following command in the terminal window that shows up

  ```
  streamlit run src/python_files/app.py
  ```

  You will see some output logged to the terminal. Click on the first link and a new browser tab will be opened, where you can see the streamlit.

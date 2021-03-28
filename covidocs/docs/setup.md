---
title: Basic Setup
---

#### 1. On Linux/macOS

##### a. If you have Docker installed

- Run the following commands on a UNIX based system.

```
chmod +x deploy.sh
./deploy.sh
```

- Open a browser and navigate to localhost:8050, and you will see the dashboard.

##### b. If you have only Python installed

- Run the following commands on a UNIX based system to get the python environment ready. We are using venv here, as its very simple to get started with.

```
python3 -m venv env # Use python instead of python3 if the command throws an error
source env/bin/activate
pip install -r requirements.txt
```

- Now start the app with the following commands.

```
cd src/
gunicorn --bind :8050 --workers 2 --threads 8 app:server # Change the number of workers and threads to your liking
```

- Open a browser and navigate to localhost:8050, and you will see the dashboard.

#### 2. On Windows

##### a. If you have Anaconda installed (recommended for easy installation)

- Run the following commands in Anaconda Prompt to create the environment.

```
cd covidash
conda env create -f environment_windows.yml
conda activate covid
```

- Now start the app with the following commands

```
cd src
python app.py
```

- Open a browser and navigate to localhost:8050, and you will see the dashboard.

##### b. If you have only Python installed

- Follow the steps in the Linux/macOS section.

##### b. If you have Docker installed

- Follow the steps in the Linux/macOS section.

### Documentation

- Run the following commands to start the docusaurus project and navigate to localhost:3000 on your browser.

```
cd covidocs
npm start
```

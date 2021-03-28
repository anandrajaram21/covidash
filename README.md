# Covidash

Covidash is an open source, community driven, COVID-19 dashboard that not only shows the daily statistics of the growing pandemic, but also forecasts the growth of the pandemic.

## Getting Started

### Prerequisites

- The program will run without any issues on any computer, but for a smooth performance, it is recommended to use a system with atleast 4 GB memory, and atleast 2 CPU cores.
- Either Python or Docker must be installed.
- Both npm and Node JS have to be installed to view the documentation.
- You can use git to clone the repository, or you can download the zip file.

### Basic Setup

#### 1. On Linux/macOS

##### a. If you have Docker installed

- Run the following commands on a UNIX based system

```
chmod +x deploy.sh
./deploy.sh
```

- Open a browser and navigate to 0.0.0.0:8050, and you will see the dashboard

##### b. If you have only Python installed

- Run the following commands on a UNIX based system to get the python environment ready. We are using venv here, as its very simple to get started with

```
python3 -m venv env # Use python instead of python3 if the command throws an error
source env/bin/activate
pip install -r requirements.txt
```

- Navigate to the web_app directory, and start the app with the following commands

```
cd src/web_app/
gunicorn --bind :8050 --workers 2 --threads 8 app:server # Change the number of workers and threads to your liking
```

- Open a browser and navigate to localhost:8050, and you will see the dashboard

#### 2. On Windows

##### a. If you have Anaconda installed (recommended for easy installation)

- Run the following commands in Anaconda Prompt

```
cd <path of the cloned folder>
conda env create -f environment_windows.yml
conda activate covid
python .\src\web_app\app.py # or change directory to web_app and run `python app.py`
```

- Open a browser and navigate to 0.0.0.0:8050, and you will see the dashboard

### Documentation

- Run the following commands to start the docusaurus project and navigate to localhost:3000 on your browser.

```
cd covidocs
npm start
```

### Presentation
<a href = "https://colab.research.google.com/drive/12SBxJ_N1TLJgc6pZVy9G-vgZY3k2w_Aa?usp=sharing">
<img src='https://img.shields.io/static/v1?label=view%20on&message=google%20colab&color=ffa31a&style=for-the-badge' />
</a> 

### Technologies Used

- All the visuals and the dashboard were built solely using **Python**. 
- **Plotly** and **Plotly Dash** were the frameworks used to create the visualizations and make the web app.
- **Keras** is the framework used to make the predictive model (CNN) that forecasts the cases for the next seven days. We chose Keras as it offered the most flexibility along with ease of learning and experimentation.


Web Application/Dashboard [(link here)](https://github.com/anandrajaram21/covidash) 

### Main Contributors
 - [Anand Rajaram](https://github.com/anandrajaram21/)
 - [Anirudh Lakhotia](https://github.com/anirudhlakhotia/)




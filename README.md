# Covidash

Covidash is an open source, community driven, COVID-19 dashboard that not only shows the daily statistics of the growing pandemic, but also forecasts the growth of the pandemic.

## Getting Started

### Prerequisites

- The program will run without any issues on any computer, but for a smooth performance, it is recommended to use a system with atleast 4 GB memory, and atleast 2 CPU cores.
- Either Python or Docker must be installed.
- Both npm and Node JS have to be installed to view the documentation.
- You can use git to clone the repository, or you can download the zip file.

### Basic Setup
##### a. Using Docker

- Run the following commands on a UNIX based system

```
chmod +x deploy.sh
./deploy.sh
```

- Open a browser and navigate to 0.0.0.0:8050, and you will see the dashboard

##### b. Using Python (venv)

- Run the following commands on a UNIX based system to get the python environment ready.

```
python3 -m venv env # Use python instead of python3 if the command throws an error
source env/bin/activate # If you are using a non POSIX compliant shell (for example, the fish shell, run this command instead: source env/bin/activate.fish)
pip install -r requirements.txt
```

- Navigate to the web_app directory, and start the app with the following commands

```
cd src/web_app/
gunicorn --bind :8050 --workers 2 --threads 8 app:server # Change the number of workers and threads to your liking
```

- Open a browser and navigate to 0.0.0.0:8050, and you will see the dashboard

### Documentation

- Run the following commands and navigate to localhost:3000 on your browser.

```
cd docs
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

<br>

Web Application/Dashboard [(link here)](https://github.com/anandrajaram21/covidash/tree/web_app) 

### Main Contributors
 - [Anand Rajaram](https://github.com/anandrajaram21/)
 - [Anirudh Lakhotia](https://github.com/anirudhlakhotia/)





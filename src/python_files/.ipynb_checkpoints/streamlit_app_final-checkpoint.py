# Imports

import sys
import os
from datetime import datetime
from datetime import date
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# Custom file imports

import vars_for_streamlit as vfs
import map 
import ARIMA
import animations
import main

@st.cache
def main_app():
    
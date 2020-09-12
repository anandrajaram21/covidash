# Imports
import copy
import sys
import os
from datetime import datetime
from datetime import date
import pandas as pd
import numpy as np
import plotly
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

confirmed_global, deaths_global, recovered_global, country_cases = None, None, None, None
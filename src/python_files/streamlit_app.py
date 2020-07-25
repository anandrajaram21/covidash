# Imports
import sys
import os
from datetime import datetime
from datetime import date
import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

# To import the main.py file
sys.path.append('../')
from python_files import main

# Getting all the data
confirmed_global, deaths_global, recovered_global, country_cases = main.collect_data()

# Streamlit trials
st.title("COVID-19 Pandemic Analysis")

option = st.sidebar.selectbox('Choose your option', ('What is COVID-19', 'Global Pandemic Situation', 'Individual Country Analysis', 'Safety Measures', 'About Us'))

if option == 'What is COVID-19':

    covid_19 =\
    """
    ## COVID-19
    Coronavirus disease 2019 (COVID-19) is an infectious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). It was first identified in December 2019 in Wuhan, Hubei, China, and has resulted in an ongoing pandemic.
    ## Symptoms of COVID-19
    Common symptoms include fever, cough, fatigue, shortness of breath, and loss of smell and taste. While the majority of cases result in mild symptoms, some progress to acute respiratory distress syndrome (ARDS) possibly precipitated by cytokine storm, multi-organ failure, septic shock, and blood clots. The time from exposure to onset of symptoms is typically around five days, but may range from two to fourteen days
    ## Treatment
    There are no vaccines nor specific antiviral treatments for COVID-19. Management involves the treatment of symptoms, supportive care, isolation, and experimental measures. The World Health Organization (WHO) declared the COVID‑19 outbreak a public health emergency of international concern (PHEIC) on 30 January 2020 and a pandemic on 11 March 2020. Local transmission of the disease has occurred in most countries across all six WHO regions.
    """
    st.markdown(covid_19)
    
elif option == 'Global Pandemic Situation':
    # Chloropleth Setup
    chloropleths = main.chloropleths

    # Plotting the confirmed cases chloropleth
    graph = 'confirmed'
    graph1 = main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

    # Plotting the deaths chloropleth
    graph = 'deaths'
    graph2 = main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

    # Plotting the recovered cases chloropleth
    graph = 'recovered'
    graph3 = main.chloropleth(graph,chloropleths[graph][0],chloropleths[graph][1],chloropleths[graph][2])

    st.write(graph1)
    st.write(graph2)
    st.write(graph3)

elif option == 'Individual Country Analysis':
    country_name = st.text_input('Enter Country Name', 'India')

    st.write('Country name chosen is', country_name)

    country_confirmed = main.get_new_cases(country_name)
    country_deaths = main.get_new_deaths(country_name)
    country_recoveries = main.get_new_recoveries(country_name)

    st.write(main.get_plot(country_confirmed))
    st.write(main.get_plot(country_deaths))
    st.write(main.get_plot(country_recoveries))

elif option == 'Safety Measures':

    safety =\
    """
    ## **Safety Measures**
    ## 1. Wash Your Hands Often
    - Wash your hands often with soap and water for at least 20 seconds especially after you have been in a public place, or after blowing your nose, coughing, or sneezing.
    - If soap and water are not readily available, **use a hand sanitizer that contains at least 60% alcohol**. Cover all surfaces of your hands and rub them together until they feel dry.
    - **Avoid touching your eyes, nose, and mouth** with unwashed hands.
    ## 2. Avoid Close Contact
    - Inside your home: Avoid close contact with people who are sick.
        - If possible, maintain 6 feet between the person who is sick and other household members.
    - Outside your home: Put 6 feet of distance between yourself and people who don’t live in your household.
    ## 3. Cover your mouth and nose with a cloth face cover when around others
    - You could spread COVID-19 to others even if you do not feel sick.
    - The cloth face cover is meant to protect other people in case you are infected.
    - Everyone should wear a cloth face cover in public settings and when around people who don’t live in your household, especially when other social distancing measures are difficult to maintain.
        - Cloth face coverings should not be placed on young children under age 2, anyone who has trouble breathing, or is unconscious, incapacitated or otherwise unable to remove the mask without assistance.
    - Do NOT use a facemask meant for a healthcare worker. Currently, surgical masks and N95 respirators are critical supplies that should be reserved for healthcare workers and other first responders.
    - Continue to keep about 6 feet between yourself and others. The cloth face cover is not a substitute for social distancing.
    ## 4. Cover coughs and sneezes
    - **Always cover your mouth and nose** with a tissue when you cough or sneeze or use the inside of your elbow and do not spit.
    - **Throw used tissues** in the trash.
    - Immediately **wash your hands** with soap and water for at least 20 seconds. If soap and water are not readily available, clean your hands with a hand sanitizer that contains at least 60% alcohol.
    ## 5. Clean and disinfect
    - **Clean AND disinfect frequently touched surfaces daily**. This includes tables, doorknobs, light switches, countertops, handles, desks, phones, keyboards, toilets, faucets, and sinks.
    - **If surfaces are dirty, clean them**. Use detergent or soap and water prior to disinfection.
    - **Then, use a household disinfectant**. Most common EPA-registered household disinfectants will work.
    ## 6. Monitor Your Health Daily
    - **Be alert for symptoms**. Watch for fever, cough, shortness of breath, or other symptoms of COVID-19.
        - Especially important if you are running essential errands, going into the office or workplace, and in settings where it may be difficult to keep a physical distance of 6 feet.
    - **Take your temperature** if symptoms develop.
        - Don’t take your temperature within 30 minutes of exercising or after taking medications that could lower your temperature, like acetaminophen.
    """
    
    st.markdown(safety)

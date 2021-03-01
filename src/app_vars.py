confirmed_global, deaths_global, recovered_global, country_cases, country_cases_sorted = (
    None,
    None,
    None,
    None,
    None
)
main_url='https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/'
img1="https://fourremovalsolutions.sg/wp-content/uploads/2020/04/Four-Solutions-Disinfecting-Spraying-01.png"
img2="https://image.freepik.com/free-vector/coronavirus-symptoms-concept_23-2148496136.jpg"
covid_19 = """
    Coronavirus disease 2019 (COVID-19) is an infectious disease caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). It was first identified in December 2019 in Wuhan, Hubei, China, and has resulted in an ongoing pandemic.
    """
symptoms="Common symptoms include fever, cough, fatigue, shortness of breath, and loss of smell and taste. While the majority of cases result in mild symptoms, some progress to acute respiratory distress syndrome (ARDS) possibly precipitated by cytokine storm, multi-organ failure, septic shock, and blood clots. The time from exposure to onset of symptoms is typically around five days, but may range from two to fourteen days."
img3="https://image.freepik.com/free-vector/scientists-working-creating-covid-19-vaccine_23-2148551283.jpg"
treatment="    There are no vaccines nor specific antiviral treatments for COVID-19. Management involves the treatment of symptoms, supportive care, isolation, and experimental measures. The World Health Organization (WHO) declared the COVID‑19 outbreak a public health emergency of international concern (PHEIC) on 30 January 2020 and a pandemic on 11 March 2020. Local transmission of the disease has occurred in most countries across all six WHO regions."
safety = """
    ## **Safety Measures**
    ## 1. Wash Your Hands Often 👏
    - Wash your hands often with soap and water for at least 20 seconds especially after you have been in a public place, or after blowing your nose, coughing, or sneezing.
    - If soap and water are not readily available, **use a hand sanitizer that contains at least 60% alcohol**. Cover all surfaces of your hands and rub them together until they feel dry.
    - **Avoid touching your eyes, nose, and mouth** with unwashed hands.
    ## 2. Avoid Close Contact 😷 <------ 6 Feet ------> 😷
    - Inside your home: Avoid close contact with people who are sick.
        - If possible, maintain 6 feet between the person who is sick and other household members.
    - Outside your home: Put 6 feet of distance between yourself and people who don’t live in your household.
    ## 3. Cover your mouth and nose with a cloth face cover when around others 🤐 😷
    - You could spread COVID-19 to others even if you do not feel sick.
    - The cloth face cover is meant to protect other people in case you are infected.
    - Everyone should wear a cloth face cover in public settings and when around people who don’t live in your household, especially when other social distancing measures are difficult to maintain.
        - Cloth face coverings should not be placed on young children under age 2, anyone who has trouble breathing, or is unconscious, incapacitated or otherwise unable to remove the mask without assistance.
    - Do NOT use a facemask meant for a healthcare worker. Currently, surgical masks and N95 respirators are critical supplies that should be reserved for healthcare workers and other first responders.
    - Continue to keep about 6 feet between yourself and others. The cloth face cover is not a substitute for social distancing.
    ## 4. Cover coughs and sneezes 🤧
    - **Always cover your mouth and nose** with a tissue when you cough or sneeze or use the inside of your elbow and do not spit.
    - **Throw used tissues** in the trash.
    - Immediately **wash your hands** with soap and water for at least 20 seconds. If soap and water are not readily available, clean your hands with a hand sanitizer that contains at least 60% alcohol.
    ## 5. Clean and disinfect
    - **Clean AND disinfect frequently touched surfaces daily**. This includes tables, doorknobs, light switches, countertops, handles, desks, phones, keyboards, toilets, faucets, and sinks.
    - **If surfaces are dirty, clean them**. Use detergent or soap and water prior to disinfection.
    - **Then, use a household disinfectant**. Most common EPA-registered household disinfectants will work.
    ## 6. Monitor Your Health Daily 👨‍⚕️
    - **Be alert for symptoms**. Watch for fever, cough, shortness of breath, or other symptoms of COVID-19.
        - Especially important if you are running essential errands, going into the office or workplace, and in settings where it may be difficult to keep a physical distance of 6 feet.
    - **Take your temperature** if symptoms develop.
        - Don’t take your temperature within 30 minutes of exercising or after taking medications that could lower your temperature, like acetaminophen.
    """
pcloud1="https://api.pcloud.com/getpubthumb?code=XZuvpQXZsR3nbzh8S9j61OE1DfDCHbAVIOdk&linkpassword=undefined&size=413x460&crop=0&type=auto"    
pcloud2="https://api.pcloud.com/getpubthumb?code=XZ7ipQXZ5KUuyw3hghJcuqkGaMUU1VQJqyOk&linkpassword=undefined&size=430x365&crop=0&type=auto"
pcloud3="https://api.pcloud.com/getpubthumb?code=XZY9HQXZEKg6hUK7fay5q06RYI65GJ5OXVay&linkpassword=undefined&size=499x499&crop=0&type=auto"
pcloud4="https://api.pcloud.com/getpubthumb?code=XZlEpQXZpJuyvwybNSmg8RVr1VPyxYcWDHCX&linkpassword=undefined&size=279x382&crop=0&type=auto"
pcloud5="https://api.pcloud.com/getpubthumb?code=XZScpQXZAAbOx5c5QeRUQzz7ji6jqFkeEJKk&linkpassword=undefined&size=387x99&crop=0&type=auto"
pcloud6="https://api.pcloud.com/getpubthumb?code=XZfOpQXZdAvDtsdvjX0Rg6RWhabgDk11fMTy&linkpassword=undefined&size=218x433&crop=0&type=auto"
clean="""Clean and disinfect frequently touched surfaces daily. This includes tables, doorknobs, light switches, countertops, handles, desks, phones, keyboards, toilets, faucets, and sinks.
    - If surfaces are dirty, clean them. Use detergent or soap and water prior to disinfection.
    - Then, use a household disinfectant. Most common EPA-registered household disinfectants will work. """
wash="""Wash your hands often with soap and water for at least 20 seconds especially after you have been in a public place, or after blowing your nose, coughing, or sneezing.
    Cover all surfaces of your hands and rub them together until they feel dry.
    Avoid touching your eyes, nose, and mouth with unwashed hands."""
mask='''You could spread COVID-19 to others even if you do not feel sick.
    The cloth face cover is meant to protect other people in case you are infected.
    Everyone should wear a cloth face cover in public settings and when around people who don’t live in your household, especially when other social distancing measures are difficult to maintain.
    The cloth face cover is not a substitute for social distancing'''
about = """
    ### This project was made by 3 High school students
    - Arunachala Amuda Murugan - [GitHub Profile](https://github.com/Majimearun)
    - Anirudh Lakhotia - [GitHub Profile](https://github.com/anirudhlakhotia)
    - Anand Rajaram - [GitHub Profile](https://github.com/anandrajaram21)
    ### You can find the source code for this project [here](https://github.com/anandrajaram21/covid-19)
    """

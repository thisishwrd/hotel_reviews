%%writefile app.py
import streamlit as st
import numpy as np
import pandas as pd
from pyngrok import ngrok
import random
import torch
import warnings
warnings.filterwarnings("ignore")

@st.cache(allow_output_mutation=True)
def get_data():
    url = 'https://drive.google.com/file/d/1beARL54xgLWxkD76WJ2SEKV2G37CgnTp/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    dataframe = pd.read_csv(path)
    
    return dataframe

df = get_data()

st.title("Hotel Data Visualisation")
st.subheader("Using Python")
st.markdown("""
Op deze website zijn hotel reviews en bijbehorende data (zoals hotel naam, review datum en de 
nationaliteit van de reviewer). Op de map zie je de reviews aan de hand van de gegevens die 
je zelf invult.

Dat kan in het linker zij-menu waar je drie input velden vindt.
\n1. In het eerste veld selecteer je de nationaliteiten van de mensen die een review hebben achtergelaten.
\n2. In het tweede veld selecteer je het minimum aantal reviews dat de reviewer gegeven moet hebben.
\n3. In het derde veld selecteer je de gemiddelde score van het hotel
\n
Nadat je op de "plot map" knop klikt zul je de geselecteerde hotels op een kaart zien en de bijbehorende data.
            """)

st.sidebar.title('Filter options')

# Reviewer nationality selector
nationalities = df['Reviewer_Nationality'].unique().tolist()
nationalities_selected = st.sidebar.multiselect(label='Nationalities reviewers', options=nationalities, \
                                                default = None)
nationalities_val_count = df['Reviewer_Nationality'].value_counts().tolist()

# Number of reviews selector
number_of_reviews = st.sidebar.number_input(label='Select totel number of reviews', \
                              min_value = 1,max_value = 100)
numb_of_reviews_val_count = df['Total_Number_of_Reviews_Reviewer_Has_Given'].value_counts().tolist()

# Average score selector
avg_score = st.sidebar.slider(label='Select minimum average review score', \
                              min_value=round(1.,1),max_value=round(10.,1), step=round(0.1, 1))


# Plot map
if st.button('Plot map'):
    df.rename(columns = {'lng':'lon'}, inplace = True)

    df_filtered_on_nat = df.loc[df['Reviewer_Nationality'].isin(nationalities_selected)]
    df_filtered_on_score = df_filtered_on_nat.loc[df_filtered_on_nat['Average_Score'] >= avg_score]
    df_filtered_on_reviews = df_filtered_on_score.loc[df_filtered_on_score['Total_Number_of_Reviews_Reviewer_Has_Given'] >= min(numb_of_reviews_val_count)]
    
    # print map
    st.map(df_filtered_on_reviews[["lat", "lon"]].dropna(how = "any"))
    
    st.write(df_filtered_on_score)

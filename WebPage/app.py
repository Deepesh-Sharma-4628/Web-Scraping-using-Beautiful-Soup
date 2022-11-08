import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
import json
from streamlit_lottie import st_lottie

def load_lottiefile(filepath:str):
    with open(filepath,"r") as f:
        return json.load(f)


def Compare(selected_company_name_1,selected_company_name_2,df):
    col1,col2=st.columns(2)
    with col1:
        f=df.loc[df['name']==selected_company_name_1]
        star_rating=":star:" * int(round(float(f['rating'].item())))
        st.header(selected_company_name_1)
        st.subheader('Ratings : ')
        st.subheader(f"{f['rating'].item()} {star_rating}")

    with col2:
        d=df.loc[df['name']==selected_company_name_2]
        star_rating=":star:" * int(round(float(d['rating'].item())))
        st.header(selected_company_name_2)
        st.subheader('Ratings : ')
        st.subheader(f"{d['rating'].item()} {star_rating}")
    col1,col2=st.columns(2)
    with col1:
        x={'':0,selected_company_name_1:f['rating'].item(),selected_company_name_2:d['rating'].item()}
        w=list(x.keys())
        y=list(x.values())
        fig = plt.figure(figsize =(9, 8))
        plt.title("Ratings",{"size":20})
        plt.xlabel("Company")
        plt.ylabel("Ratings")
        plt.bar(w,y,color=['red', 'cyan'],width=0.3)
        st.pyplot(fig)
    with col2:
        x={selected_company_name_1:f['Average Salary'].item(),selected_company_name_2:d['Average Salary'].item()}
        w=list(x.keys())
        y=list(x.values())
        fig = plt.figure(figsize =(9, 8))
        plt.title("Average Salary per anum",{"size":20})
        plt.xlabel("Company")
        plt.ylabel("Average Salary")
        plt.bar(w,y,color=['green', 'orange'],width=0.2)
        st.pyplot(fig)

    col1,col2=st.columns(2)
    with col1:
        st.write(selected_company_name_1+" Office")
        map=folium.Map(location=[f['Latitude'].item(),f['Longitude'].item()])
        map.add_child(folium.Marker(location=[f['Latitude'].item(),f['Longitude'].item()],popup=selected_company_name_1+' HQ',icon=folium.Icon(color='red')))
        folium_static(map,width=430)
    with col2:
        st.write(selected_company_name_2+" Office")
        map=folium.Map(location=[d['Latitude'].item(),d['Longitude'].item()])
        map.add_child(folium.Marker(location=[d['Latitude'].item(),d['Longitude'].item()],popup=selected_company_name_2+' HQ',icon=folium.Icon(color='black')))
        folium_static(map,width=450)

st. set_page_config(page_title="Compare Companies",layout="wide")       
df=pd.read_csv('file1.csv')
st.sidebar.title('Compare Companies')
selected_company_name_1 = st.sidebar.selectbox(
    'Select By Company Name',
   df['name'])

st.sidebar.write('You selected:', selected_company_name_1)
selected_company_name_2 = st.sidebar.selectbox(
    'Select By Comapany Name',
    df['name'],key=1)
st.sidebar.write('You selected:', selected_company_name_2)
if st.sidebar.button('Compare'):
    Compare(selected_company_name_1,selected_company_name_2,df)
else:
    lotti=load_lottiefile("lotti.json")
    lotti2=load_lottiefile("lotti2.json")
    st_lottie(
       lotti, 
        height=550
    )
    
#st.dataframe(df)
import pandas as pd
import requests
from bs4 import BeautifulSoup
from geopy.geocoders import ArcGIS
import numpy as np

final=pd.DataFrame()
for j in range(1,20):
    url='https://www.ambitionbox.com/list-of-companies?page={}'.format(j)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    webpage=requests.get(url,headers=headers).text

    soup=BeautifulSoup(webpage)
    company=soup.find_all('div',class_='ab-company-result-card')

    name=[]
    rating=[]
    reviews=[]
    ctype=[]
    hq=[]
    salary=[]

    for i in company:
        name.append(i.find('h2').text.strip())
        rating.append(i.find('p',class_='rating').text.strip())
        reviews.append(i.find('a',class_='review-count').text.strip())
        ctype.append(i.find_all('p',class_='infoEntity')[0].text.strip())
        try:
            hq.append(i.find_all('p',class_='infoEntity')[1].text.strip())
        except:
            hq.append(np.nan)
        salary.append(i.find_all('span',class_='caption-subdued-large')[1].text.strip())

    HQ=[]
    latitude=[]
    longitude=[]
    Average=[]
    for i in hq:
        try:
            HQ.append(i.split("+",1)[0])
        except:
            HQ.append(np.nan)

    Average=[]
    for i in salary:
        j=i.replace("k",".")
        Average.append(j.split(".",1)[0]+'000')


    nom=ArcGIS()
    for i in HQ:
        s=nom.geocode(i)
        try:
            latitude.append(s.latitude)
            longitude.append(s.longitude)
        except:
            latitude.append(np.nan)
            longitude.append(np.nan)

    d={'name':name, 'rating':rating, 'reviews':reviews, 'type':ctype, 'hq':HQ,'Average Salary':Average, 'Latitude':latitude, 'Longitude':longitude}
    df=pd.DataFrame(d)
    final=final.append(df,ignore_index=True)
final.to_csv('file1.csv')
import numpy as np
import pandas as pd
from datetime import date

# for getting world map
import folium

# read_html() method returns all the tables in the webpage (Internally beautifulSoup is executed)

# Latitude and Longitude coordinates
ori_coordinate = {"District":['Barat Daya','Timur Laut','Seberang Perai Tengah', 'Seberang Perai Selatan','Seberang Perai Utara'], "Latitude":[5.3519, 5.4142, 5.3535, 5.1958, 5.5148], "Longitude":[100.2359, 100.3285, 100.4518, 100.4921, 100.4355]}
coordinates = pd.DataFrame(ori_coordinate)

# Retrieving the LIVE COVID19 Stats from Wikipedia
coronastats = pd.read_html('http://covid-19.livephotos123.com/state/view?id=P.Pinang')

# Convert to DataFrame
covid19 = pd.DataFrame(coronastats[0])
covid19 = covid19.drop(columns=covid19.columns[0])
covid19 = covid19.drop(covid19.index[5])
covid19["NewCase"] = covid19["Total"].apply(lambda st: st[st.find("(")+1:st.find(")")])
covid19.head()

final_data = pd.merge(coordinates, covid19, how ='inner', on ='District')
final_data.head()

penang = folium.Map(location = [5.4164,100.3327],zoom_start=11.5)


# adding to map
for district,lat,long,total_cases,Active, NewCase in zip(list(final_data['District']),list(final_data['Latitude']),list(final_data['Longitude']),list(final_data['Total']),list(final_data['Active']),list(final_data['NewCase'])):
    # for creating circle marker
    folium.CircleMarker(location = [lat,long],
                       radius = 5,
                       color='red',
                       fill = True,
                       fill_color="red").add_to(penang)
    # for creating marker
    icon = folium.features.CustomIcon('https://static.wikia.nocookie.net/fategrandorder/images/9/98/Nobu_tank.png', icon_size=(100,100))
    folium.Marker(location = [lat,long],
                  icon=icon,
                  # adding information that need to be displayed on popup
                  popup=folium.Popup(('<strong><b>Date  : '+str(date.today())+'</strong> <br>' +
                    '<strong><b>District  : '+district+'</strong> <br>' +
                    '<strong><b><font color=red>New Cases : '+str(NewCase)+'</font></striong><br>' +
                    '<strong><b><font color=yellow>Active Cases : '+str(Active)+'</font></striong><br>' +
                    #'<strong><font color= red>Deaths : </font>'+Death+'</striong><br>' +
                    #'<strong><font color=green>Recoveries : </font>'+Recov+'</striong><br>' +
                    '<strong><b>Total Cases : '+total_cases+'</striong>' ),max_width=200)).add_to(penang)

penang.save('penang_map.html')
import geopy
from geopy.geocoders import Nominatim
from geopy import distance

import folium
from folium.plugins import MarkerCluster

import json

import random

import sys

import urllib


def get_bounds(deger):
    json_location = json.dumps(deger.raw)

    json_location = json.loads(json_location)
    locations_limit = json_location["boundingbox"]

    return locations_limit

# Users Input Locations
address = str(input("Enter Location: "))
if (address == "" or address == " "):
    address == 'Maslak, İstanbul, Turkey'

# GeoCode Üzerinden Lokasyon Verileri 
Location = Nominatim(user_agent="find_location")
inputLocation= Location.geocode(address)
print(inputLocation)

# Lokasyon Sınırları
bounds = get_bounds(inputLocation)


# kullanılacak listeler
colist = [] # Random Lokasyonlar
locations_list = [] # Sınırlandırılmış Lokasyonlar
list_of_buckets = [] # Sepetlere Bölünmüş Lokasyonlar


# Random Oluşturulan Noktalar
for i in range(random.randint(500, 600)): # 500 ile 600 arasında rastgele oluşturulan noktalar


    ranLat = (random.uniform(float(bounds[0]), float(bounds[1])))
    ranLot = (random.uniform(float(bounds[2]), float(bounds[3])))
    colist.append([ranLat, ranLot])

# Random Oluşturulan Konumların Sıralanması
colist.sort()
print("Lokasyon Sayısı =",len(colist))
control_num = len(colist)


# Map de Konumun Orta Kısmını İşaretle
middle_y = ((float(bounds[0]) + float(bounds[1])) / 2)
middle_x = ((float(bounds[2]) + float(bounds[3])) / 2)

# Haritada Lokasyonun orta kısmı bulunuyor.
m = folium.Map(location=[middle_y,middle_x], tiles='OpenStreetMap', zoom_start=15)


# Konumları Sınırlama Algoritması 
start_num = 0
while True:
    gecici_lokasyon = []
    gecici_lokasyon.clear()
    start_loc = colist[start_num]

    
    for i in range(start_num,len(colist)):
        
        mesafe = distance.distance(start_loc,colist[i]).km
        
        if mesafe < 1.10: # iki nokta arasındaki max uzaklık 
            gecici_lokasyon.append(colist[i])
            start_num += 1   
        else:
            continue
    locations_list.append(gecici_lokasyon)
    if (start_num == control_num):
        break


#Text Dosyası Oluştur
# sys.stdout = open('Locations.txt', 'w' , encoding='utf-8') # Terminal Yerine Txt Dosyasına Yazmak İstenirse Aktifleştirilsin bu ve en sondaki sys.stdout.close() kodu.

# Elde Edilen Lokasyon Sınıflandırmasına göre Yazdırma işlemi 
print("Sepet Sayısı =",len(locations_list))
for i in range(len(locations_list)):
    print("Sepet No#{}".format(i+1))
    div = 0
    bucket_circle_y = 0
    bucket_circle_x = 0
    for j in range(len(locations_list[i])):
        s = urllib.parse.quote("www.google.com.tr/maps/@{},{},17z".format(locations_list[i][j][0],locations_list[i][j][1]))
        map_link ='https://' + s

        bucket_circle_y +=  locations_list[i][j][0]
        bucket_circle_x +=  locations_list[i][j][1]
        div += 1
        location_address = Location.reverse(locations_list[i][j])
        folium.Marker(location=locations_list[i][j], popup=locations_list[i][j], icon=folium.Icon(color="blue",icon="glyphicon glyphicon-phone")).add_to(m)
        print("  item #{} -> GeoCode# {}, Address# {}, Link# {}".format(j+1, locations_list[i][j],location_address,map_link))
    bucket_circle_y = bucket_circle_y / div
    bucket_circle_x = bucket_circle_x / div
    folium.Marker(location=[bucket_circle_y,bucket_circle_x],popup="SepetNo#{}".format(i+1) , icon=folium.Icon(color="green",icon="glyphicon glyphicon-shopping-cart")).add_to(m)
    folium.Circle([bucket_circle_y,bucket_circle_x],radius=1000,fill=True,color="green").add_to(m)
m.save('index.html')

# sys.stdout.close() # Terminal Yerine Txt Dosyasına Yazmak İstenirse Aktifleştirilsin
# print("Text File Ready")
#!/usr/bin/env python

from lxml import etree
import requests
from jinja2 import Template
import webbrowser

#funcion que devuelve la orientacion del viento norte N,nordeste NE,este E, ......
def direccion_vi(cadena):
    if cadena>=337.5 and cadena<=360.0 or cadena>=0 and cadena<22.5:
       	return "N"
    if cadena>=22.5 and cadena<=67.5:
       	return "NE"
    if cadena>=67.5 and cadena<112.5:
       	return "E"
    if cadena>=112.5 and cadena<157.5:
        return "SE"
    if cadena>=157.5 and cadena<202.5:
        return "S"
    if cadena>=202.5 and cadena<247.5:
        return "SE" 
    if cadena>=247.5 and cadena <292.5:
        return "O"
    if cadena>=292.5 and cadena<337.5:
        return "NO"

f=open('plantilla1.html','r')
f_weather=open('weather.html','w')
html=''
temp_min =[]
temp_max = []
velocidad_viento = []
direccion = []
provincia_salida=[]

dicc_ciudad={'1':'Almeria','2':'Cadiz','3':'Cordoba','4':'Granada','5':'Huelva','6':'Jaen','7':'Malaga','8':'Sevilla'}
provincias=dicc_ciudad.values()
url="http://api.openweathermap.org/data/2.5/weather?"
for provincia in provincias:
    dicc_params={"q":provincia,"mode":"xml","units":"metric","lang":"es"}
    respuesta=requests.get(url,params=dicc_params)
    codificacion=respuesta.text.encode('utf-8')
    arbol=etree.fromstring(codificacion)
    viento=arbol.find("wind/speed")
    dir=arbol.find("wind/direction")
    temperatura=arbol.find("temperature")
    provincia_salida.append(provincia)
    temp_min.append(temperatura.attrib["min"])
    temp_max.append(temperatura.attrib["max"])
    velocidad_viento.append(viento.attrib["value"])
    direccion_sal=float(dir.attrib["value"])
    direccion.append(direccion_vi(direccion_sal))
for linea in f:
    html += linea
mi_template=Template(html)
salida=mi_template.render(ciudades=provincia_salida, temp_minima=temp_min, temp_maxima=temp_max, viento=velocidad_viento, direccion_viento=direccion)
f_weather.write(salida)
webbrowser.open("weather.html")	


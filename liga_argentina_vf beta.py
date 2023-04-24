#instalar las librerias requests, bs4, pandas
#instalar el interprete de python
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
url='https://www.tycsports.com/agenda-deportiva-hoy.html'
page=requests.get(url)
soup=BeautifulSoup(page.content,'html.parser')
#equipos locales
#necesito extraer los equipos que se encuentran dentro de <div class="agenda_eventoWrap" data-rango-horario="noche" data-competencia="primeraa" data-deporte="futbol" data-dia="hoy"> seguido de <span class="team teamDesktop">Colón</span> siendo Colón el equipo de ejemplo
eq=soup.find_all('div',class_='agenda_eventoWrap')
equipos=list()
#quiero filtrar por data-competencia="primeraa" y data-dia="hoy"
for i in eq:
    if i['data-competencia']=='primeraa' and i['data-dia']=='hoy':
        equipos.append(i.find('span',class_='team teamDesktop').text)
print(equipos)
#equipos visitantes
#los equipos visitante se encuentran en el mismo div pero en <span class="agenda__match-team visita"> y <span class="team teamDesktop">Vélez</span>
eq2=soup.find_all('div',class_='agenda_eventoWrap')
equipos2=list()
for i in eq2:
    if i['data-competencia']=='primeraa' and i['data-dia']=='hoy':
        equipos2.append(i.find('span',class_='agenda__match-team visita').find('span',class_='team teamDesktop').text)
print(equipos2)
#partidos
#juntar los elementos de la lista equipos y equipos2 en una lista llamada partidos con la cadena ' vs '
partidos=list()
for i in range(len(equipos)):
    partidos.append(equipos[i]+' vs '+equipos2[i])
print(partidos)
#hora
#los horarios se encuentran en el mismo div y en <div class="agenda__time"> y <span>21:00</span> quiero filtrar por data-competencia="primeraa" y data-dia="hoy"
hora=soup.find_all('div',class_='agenda_eventoWrap')
horas=list()
for i in hora:
    if i['data-competencia']=='primeraa' and i['data-dia']=='hoy':
        horas.append(i.find('div',class_='agenda__time').find('span').text)
print(horas)
#canal de tv
#los canales de tv se encuentran en el mismo div y en <div class="agenda_article">despues en <div class="agenda__cta"<div/> y <span class="transmitions"<span/> quiero filtrar por data-competencia="primeraa" y data-dia="hoy"
canales=soup.find_all('div',class_='agenda_eventoWrap')
canal=list()
for i in canales:
    if i['data-competencia']=='primeraa' and i['data-dia']=='hoy':
        canal.append(i.find('div',class_='agenda_article').find('div',class_='agenda__cta').find('span',class_='transmitions').text)
print(canal)
partidoshoy=list()
#el formato de los partidos es el siguiente 'Colón vs Vélez 21:00 TyC Sports' cambiar la palabra TRANSMITE POR LA PALABRA EN
for i in range(len(partidos)):
    partidoshoy.append(partidos[i]+' '+horas[i]+' '+canal[i].replace('TRANSMITE :','EN'))
print(partidoshoy)
#GENERAR UN CSV llamado liga argentina con los partidos de hoy
df=pd.DataFrame(partidoshoy,columns=['Partidos de hoy'])
df.to_csv('liga argentina.csv',index=False)






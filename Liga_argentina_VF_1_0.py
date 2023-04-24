import pandas as pd
import requests
from bs4 import BeautifulSoup

def webscraping():
    url = 'https://www.tycsports.com/agenda-deportiva-hoy.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Equipos locales
    eq = soup.find_all('div', class_='agenda_eventoWrap')
    equipos = []
    for i in eq:
        if i['data-competencia'] == 'primeraa' and i['data-dia'] == 'hoy':
            equipos.append(i.find('span', class_='team teamDesktop').text)

    # Equipos visitantes
    eq2 = soup.find_all('div', class_='agenda_eventoWrap')
    equipos2 = []
    for i in eq2:
        if i['data-competencia'] == 'primeraa' and i['data-dia'] == 'hoy':
            equipos2.append(i.find('span', class_='agenda__match-team visita').find('span', class_='team teamDesktop').text)

    # Partidos
    partidos = [f'{local} vs {visitante}' for local, visitante in zip(equipos, equipos2)]

    # Hora
    hora = soup.find_all('div', class_='agenda_eventoWrap')
    horas = []
    for i in hora:
        if i['data-competencia'] == 'primeraa' and i['data-dia'] == 'hoy':
            horas.append(i.find('div', class_='agenda__time').find('span').text)

    # Canal de TV
    canales = soup.find_all('div', class_='agenda_eventoWrap')
    canal = []
    for i in canales:
        if i['data-competencia'] == 'primeraa' and i['data-dia'] == 'hoy':
            canal.append(i.find('div', class_='agenda_article').find('div', class_='agenda__cta').find('span', class_='transmitions').text.replace('TRANSMITE :', 'EN'))

    # Partidos de hoy
    partidoshoy = [f'{partido} {hora} {tv}' for partido, hora, tv in zip(partidos, horas, canal)]

    # Escribir archivo de texto
    with open('partidos.txt', 'w', encoding='utf-8') as archivo:
        archivo.write('PARTIDOS DE HOY liga argentina\n\n')
        for partido in partidoshoy:
            archivo.write(partido + '\n\n')
#ejecutar funcion
webscraping()
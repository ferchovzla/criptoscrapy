import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

import requests
from bs4 import BeautifulSoup
#import csv
from datetime import datetime

#Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
    ]
file_name = 'client_key.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name,scope)
client = gspread.authorize(creds)


#Fetch the sheet
sheet = client.open('Monedas 2020').sheet1
python_sheet = sheet.get_all_records()
pp = pprint.PrettyPrinter()
pp.pprint(python_sheet)


# indicar la ruta
url_page = ['https://monitordolarvenezuela.com/', 'https://exchangemonitor.net/criptos', 'https://coinmarketcap.com/']

page = requests.get(url_page[0]).text 
soup = BeautifulSoup(page, "html.parser")

dateAndTime = soup.find_all('h4', attrs={'class': 'text-center'})

print("Cotizaciones al "+dateAndTime[0].getText())

print('=========== $$$ Dolar $$$ ===========')
dolar_monitor = soup.find_all("h6", {'class':['back-white-tabla', 'text-center']})

print("Monitor Dolar "+dolar_monitor[1].getText())

criptos = soup.find_all('div', attrs={'class': 'col-12 col-lg-5'})
monto = soup.find_all('div', attrs={'class': 'col-6 col-lg-4'})

kriptos = {}

for c, m in zip(criptos, monto):
    print(c.getText(), m.getText())
    kriptos[c.getText()] = ["VES/USD", m.getText().replace(".","*").replace(",",".").replace("*",",")]


print("=========== @@@ Criptomonedas @@@ ===========")

page = requests.get(url_page[1]).text 
soup = BeautifulSoup(page, "html.parser")

criptos = soup.find_all('div', attrs={'class': 'col c-nombre'})
names = soup.find_all('h6', attrs={'class': 'nombre'})
unities = soup.find_all('p', attrs={'class': 'unidad'})
prices = soup.find_all('p', attrs={'class': 'precio'})


for c, n, u, p in zip(criptos, names, unities, prices):
    print("Cripto: "+n.getText())
    print("Unidad: "+u.getText())
    print("Precio: "+p.getText().replace(".","*").replace(",",".").replace("*",","))#. * , . * ,
    print("-------------------------")
    kriptos[n.getText()] = [u.getText(), p.getText().replace(".","*").replace(",",".").replace("*",",")]


print("=========== ### Criptocurrency @@@ ===========")

page = requests.get(url_page[2]).text 
soup = BeautifulSoup(page, "html.parser")

#criptos = soup.find_all('div', attrs={'class': 'cmc-table__column-name cmc-table__column-name--narrow-layout'})
names = soup.find_all('a', attrs={'class': 'cmc-link'})
#unities = soup.find_all('p', attrs={'class': 'unidad'})
#prices = soup.find_all('p', attrs={'class': 'precio'})

can_read = False
Kriptos = {}

it=0
for n in names:
    if n.getText() == "Bitcoin":
       can_read = True
    if can_read:
       it=it+1

       if it ==1:
       	  if it == "Next 100 →":
       	  	can_read = False
       	  	break
          kripto_name = n.getText()
       elif it ==2:
          Kriptos[kripto_name] = n.getText().replace(".","*").replace(",",".").replace("*",",")
          print("Name: "+n.getText().replace(".","*").replace(",",".").replace("*",","))
       elif it==4:
          it=0  

    #  print("Cripto: "+n.getText())
    #print("Name: "+n.getText())
    ##print("Precio: "+p.getText().replace(".","*").replace(",",".").replace("*",","))#. * , . * ,
       print("-------------------------")
    #kriptos[n.getText()] = [u.getText(), p.getText().replace(".","*").replace(",",".").replace("*",",")]


#Update LocalBitcoin (BTC) 
cell = sheet.cell(3,2)
sheet.update_cell(3,2,kriptos['LocalBitcoin (BTC)'][1])

#Update AIRTM
cell = sheet.cell(9,2)
sheet.update_cell(9,2,kriptos['AIRTM'][1])
#sheet.update_cell(9,2,Kriptos['AIRTM'][1])

#Update Bitcoin Cell 
cell = sheet.cell(12,2)
#sheet.update_cell(12,2,kriptos['Bitcoin'][1])
sheet.update_cell(12,2,Kriptos['Bitcoin'])

#Update Pax Cell 
cell = sheet.cell(6,2)
sheet.update_cell(6,2,Kriptos['Paxos Standard'])

#Update Pax Cell 
cell = sheet.cell(15,2)
sheet.update_cell(15,2,Kriptos['Nano'])

#Update Ethereum Cell 
cell = sheet.cell(18,2)
#sheet.update_cell(18,2,kriptos['Ethereum'][1])
sheet.update_cell(18,2,Kriptos['Ethereum'])

#Update Litecoin Cell 
cell = sheet.cell(21,2)
#sheet.update_cell(12,2,kriptos['Bitcoin'][1])
sheet.update_cell(21,2,Kriptos['Litecoin'])





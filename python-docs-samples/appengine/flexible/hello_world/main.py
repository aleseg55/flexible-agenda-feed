#INSTALACION SQLALCHEMY
#sudo apt-get install mysql-server
#sudo apt-get install mysql-client
#sudo apt-get install libmysqlclient-dev
#sudo apt-get install python-mysqldb
#sudo wget http://peak.telecommunity.com/dist/ez_setup.py
#sudo python ez_setup.py
#sudo easy_install MySQL-Python
#sudo easy_install SQLAlchemy

#ARMAR UN CRUD CON SQLALCHEMY
#https://www.codementor.io/garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2

import sys
sys.path.insert(0,'libs')
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, make_response, request, Response
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, time
import re
import locale
from dateparser import parse
#from operator import itemgetter

#locale.setlocale(locale.LC_ALL,'en_US.utf8')

titulos=[]
filas=[]
hora_actual=''
valor='SoyElValor'
app= Flask(__name__)

@app.route("/")
def home():
	#titulo=sopa.title
	return render_template("home.html",valor=valor)

@app.route("/news")
def news():
	return render_with_context("get_news.html",eventos=filas,hora_actual=hora_actual)

def cambiar_valor():
	global valor
	valor="Soy el Nuevo Valor!!!"
	print("el nuevo valor es"+valor)

def get_mes(str):
	if "enero" in str:
		return 1
	elif "febrero" in str:
		return 2
	elif "marzo" in str:
		return 3
	elif "abril" in str:
		return 4
	elif "mayo" in str:
		return 5
	elif "junio" in str:
		return 6
	elif "julio" in str:
		return 7
	elif "agosto" in str:
		return 8
	elif "septiembre" in str:
		return 9
	elif "octubre" in str:
		return 10
	elif "noviembre" in str:
		return 11
	elif "diciembre" in str:
		return 12

def get_news():
	#global titulos
	#html=''
	#html=requests.get('http://www.randomtextgenerator.com/')
	#sopa=BeautifulSoup(html.content,'html.parser')
	#titulos.append(sopa.find('textarea',{'id':'generatedtext'}).string)
	#print(titulos)
	global filas
	global hora_actual
	hora_actual=datetime.now()
	filas=[]
	html=requests.get('https://www.meetup.com/es/find/tech/?allMeetups=false&radius=31&userFreeform=buenos+aires&mcId=c1000296&change=yes&sort=default')
	sopa=BeautifulSoup(html.content,'html.parser')
	grupos=[]
	
	#filas.append({'lunes':'sopa','martes':'pescado'})
	#filas.append({'lunes':'milanesa','martes':'empanadas'})

	for li_item in sopa.find_all('li',{'class':'noRatings'}):
	    grupos.append(li_item.findChild('a',{'class':'groupCard--photo'}).get('href'))
	    
	i=0
	    
	for grupo in grupos:

		#if i>10:
		#	break

		url_eventos=grupo+'events/'
		html=requests.get(url_eventos)
		sopa=BeautifulSoup(html.content,'html.parser')    

		for evento in sopa.find_all('li',{'class':'list-item'}):  
			evento_fila={}

			#entrar al detalle del evento
			html_detalle_evento=requests.get('https://www.meetup.com'+evento.findChild('a').get('href'))
			sopa_detalle_evento=BeautifulSoup(html_detalle_evento.content,'html.parser')

			try:

				fecha_string=sopa_detalle_evento.find('span',{'class':'eventTimeDisplay-startDate'}).findChild('span').text
				anio=re.findall("\d{4}",fecha_string)[0]
				mes=get_mes(fecha_string)
				dia=re.findall("\d{1,2}",fecha_string.replace(anio,''))[0]
				print(fecha_string)
				print(anio)
				print(mes)
				print(dia)
				fecha_formato_fecha=date(int(anio),int(mes),int(dia))
				print(fecha_formato_fecha)



				evento_fila = {"nombre_grupo":sopa.find('a',{'class':'groupHomeHeader-groupNameLink'}).text,
							"link_grupo":grupo,
							"nombre_evento":evento.findChild('a').text,
							"link_evento":'https://www.meetup.com'+evento.findChild('a').get('href'),
							"fecha_string":fecha_string,
							"fecha_formato_fecha":fecha_formato_fecha.strftime("%x"),
							"hora_inicio":sopa_detalle_evento.find('span',{'class':'eventTimeDisplay-startDate-time'}).findChild('span').text,
							"hora_fin":sopa_detalle_evento.find('span',{'class':'eventTimeDisplay-endDate-partialTime'}).findChild('span').text,
							"ubicacion":sopa_detalle_evento.find(lambda tag: tag.name == 'p' and 'wrap--singleLine--truncate' in tag.get('class','') and 'text--secondary' not in tag.get('class', '')).text,
							"direccion":sopa_detalle_evento.find('p',{'class':'venueDisplay-venue-address'}).text.replace(' ·',',')}
				
				if False:
					#link del grupo
					evento_fila.append({'link_grupo':grupo})
					#nombre del evento
					evento_fila.append({'nombre_evento':evento.findChild('a').text})
					#link del evento
					evento_fila.append({'link_evento':'https://www.meetup.com'+evento.findChild('a').get('href')})

					#entrar al detalle del evento
					html_detalle_evento=requests.get('https://www.meetup.com'+evento.findChild('a').get('href'))
					sopa_detalle_evento=BeautifulSoup(html_detalle_evento.content,'html.parser')

					#dia del evento
					evento_fila.append({'dia':sopa_detalle_evento.find('span',{'class':'eventTimeDisplay-startDate'}).findChild('span').text})
					#hora de inicio del evento
					evento_fila.append({'hora_inicio':sopa_detalle_evento.find('span',{'class':'eventTimeDisplay-startDate-time'}).findChild('span').text})
					#hora de fin del evento
					evento_fila.append({'hora_fin':sopa_detalle_evento.find('span',{'class':'eventTimeDisplay-endDate-partialTime'}).findChild('span').text})
					#ubicacion del evento
					evento_fila.append({'ubicacion':sopa_detalle_evento.find(lambda tag: tag.name == 'p' and 'wrap--singleLine--truncate' in tag.get('class','') and 'text--secondary' not in tag.get('class', '')).text})
					#direccion del evento
					evento_fila.append({'direccion':sopa_detalle_evento.find('p',{'class':'venueDisplay-venue-address'}).text.replace(' ·',',')})
				filas.append(evento_fila)
				print(evento_fila)
			except:
				continue
		i=i+1
	#print(filas)
	filas.sort(key=lambda x:parse(x["fecha_formato_fecha"]))
	for item in filas:
		print("indice: "+str(filas.index(item)))
		print(item.get("fecha_formato_fecha"))


	

def render_with_context(template, _url="/news", **kw):
	with app.test_request_context(""):
		return render_template(template, **kw)

sched=BackgroundScheduler(daemon=True)
sched.add_job(get_news,'interval', hours=4)
sched.start()

if __name__ == "__main__":
	app.run(debug=True)
	
	

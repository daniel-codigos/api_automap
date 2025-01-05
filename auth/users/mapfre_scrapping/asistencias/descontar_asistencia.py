from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
import time

class ingresar_porcentaje():
    def __init__(self,driver,porcentaje):
        self.driver = driver
        self.porcentaje = porcentaje
        self.ingresar()

    def ingresar(self):
        self.driver.find_element(By.XPATH,'//input[@id="idPreguntaNO"]').click()
        self.driver.find_element(By.XPATH,'//input[@id="mcaIntervencionTSRNO"]').click()
        self.driver.find_element(By.XPATH,'//input[@id="mcaIntervencionPeriNO"]').click()
        time.sleep(.5)
        self.driver.find_element(By.XPATH,'//td[@id="presupuestoTab"]').click()
        time.sleep(.5)
        for cadaOpcion in self.driver.find_elements(By.XPATH,'//option[@onclick="return func_1(this, event);"]'):
            if cadaOpcion.get_attribute('value') == self.porcentaje.replace("%",''):
                cadaOpcion.click()
            #if cadaOpcion.get_attribute('value') ==

class ingresar_importe():
    def __init__(self,driver,precio):
        self.driver = driver
        self.precio = precio
        if precio == '0':
            self.presu = True
        else:
            self.presu = False
        print(self.precio)
        self.ingresar()

    def ingresar(self):
        #print(self.driver.page_source)
        if self.presu:
            #presupuestoTab
            self.driver.find_element(By.XPATH,'//td[@id="presupuestoTab"]').click()
            time.sleep(3)
            #idPregEmitirFacN
            #idPreguntaSI
            try:
                self.driver.find_element(By.XPATH, '//input[@id="idPreguntaSI"]').click()
            except ElementNotInteractableException:
                try:
                    self.driver.find_element(By.XPATH, '//input[@id="idPregEmitirFacN"]').click()
                except ElementNotInteractableException:
                    print("Ninguno de los elementos se encontró en la página.")
            #self.driver.find_element(By.XPATH,'//input[@id="idPreguntaSI"]').click()
            time.sleep(.5)
        self.driver.find_element(By.XPATH,'//td[@id="importesTab"]').click()
        time.sleep(.5)
        self.driver.switch_to.frame(self.driver.find_element(By.NAME,'iTarifasI'))
        self.driver.find_element(By.XPATH,"//span[@onclick=\"borrar_anadir_modificar('anadir', 'ppal');\"]").click()
        self.driver.switch_to.default_content()
        for x in ["contenido", "iDetalle"]:
            # print(driver.page_source)
            self.driver.switch_to.frame(x)
            time.sleep(.5)
        self.driver.find_element(By.ID,'codTarifaPrin').send_keys('ZB9')
        self.driver.execute_script("javascript:validaTarifa()")
        time.sleep(.5)
        self.driver.find_element(By.ID,'importeTotal').send_keys(Keys.BACK_SPACE*4)
        time.sleep(.2)
        self.driver.find_element(By.ID,'importeTotal').send_keys(self.precio)
        time.sleep(.5)
        self.driver.execute_script("grabaTarifa();")
        time.sleep(1)
        #acepta descuento
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame("contenido")
        self.driver.execute_script("aceptarPestañas();")
       # time.sleep(9)


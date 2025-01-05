from ..vars import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


class in_impor():
    def __init__(self, driver, importes):
        self.driver = driver
        self.importes = importes
        self.mueveteDescuentos(self.driver)

    def mueveteDescuentos(self, driver):
        driver.execute_script("BotonesBarra('I');activateTab('importesTab', 'cImportes');mostrarNotasInf('cImportes')")
        sleep(4)
        self.hazDescuentos(driver)


    def hazDescuentos(self,driver):
        for cadaImpor in self.importes:
            driver.switch_to.default_content()
            for je in ["contenido", "iTarifasI"]:
                driver.switch_to.frame(driver.find_element(By.NAME,je))
            # js q hace el click en boton de añadir ;)))
            driver.execute_script("borrar_anadir_modificar('anadir', 'ppal');")
            driver.switch_to.default_content()
            for x in ["contenido", "iDetalle"]:
                #print(driver.page_source)
                driver.switch_to.frame(x)
                sleep(.5)
            #diferenciamos de yyt y lat del resto q va con cantidades y tal... Diver... Tambien de parking y tal :D
            #print(driver.find_element(By.XPATH,'//div[@id="cDetalle"]/iframe').get_attribute("src"))
            if len(cadaImpor) == 2:
                if cadaImpor[1] == True:
                    driver.find_element(By.XPATH,'//option[@value="P"]').click()
                    driver.find_element(By.ID,"importeTotal").send_keys(cadaImpor[0])
                    driver.execute_script("grabaTarifa();")
                    sleep(1)
                #elif para cuando hay una cantidad y hay q modificar la cantidad
                elif type(cadaImpor[1]) == str and str(cadaImpor[1]).isdigit() and int(cadaImpor[1]) > 1:
                    driver.find_element(By.ID,"codTarifaPrin").click()
                    driver.find_element(By.ID,"codTarifaPrin").send_keys(cadaImpor[0])
                    driver.execute_script("javascript:validaTarifa()")
                    driver.find_element(By.ID,"unidades").send_keys(Keys.BACK_SPACE*len(driver.find_element(By.ID,"unidades").get_attribute('value')))
                    sleep(3)
                    driver.find_element(By.ID,"unidades").send_keys(cadaImpor[1])
                    sleep(2)
                    driver.execute_script("grabaTarifa();")
                elif cadaImpor[1] == "fueraT":
                    print("fuera tarifa!!")
                    driver.find_element(By.XPATH, '//option[@value="M"]').click()
                    sleep(2)
                    driver.find_element(By.ID, "importeTotal").send_keys(cadaImpor[0])
                    sleep(3)
                    driver.execute_script("grabaTarifa();")
                    sleep(1)
                elif cadaImpor[1] == "zb9":
                    driver.find_element(By.ID,"codTarifaPrin").click()
                    driver.find_element(By.ID,"codTarifaPrin").send_keys(cadaImpor[1])
                    driver.execute_script("javascript:validaTarifa()")
                    sleep(.5)
                    driver.find_element(By.ID,"importeTotal").send_keys(Keys.BACK_SPACE*len(driver.find_element(By.ID,"unidades").get_attribute('value')))
                    sleep(1)
                    driver.find_element(By.ID,"importeTotal").send_keys(cadaImpor[0])
                    sleep(2)
                    driver.execute_script("grabaTarifa();")
                else:
                    driver.find_element(By.ID,"codTarifaPrin").click()
                    driver.find_element(By.ID,"codTarifaPrin").send_keys(cadaImpor[0])
                    for j in ["javascript:validaTarifa()", "grabaTarifa();"]:
                        driver.execute_script(j)
                        sleep(1)
            # todo esto para abajo es para importes q no van dentro de un array
            elif cadaImpor == "guardia":
                driver.find_element(By.XPATH,'//option[@value="U"]').click()
                sleep(5)
                for j in ["javascript:validaTarifa()", "grabaTarifa();"]:
                    driver.execute_script(j)
                    sleep(4)
                sleep(1)
            else:
                if cadaImpor != "guardia":
                    driver.find_element(By.ID,"codTarifaPrin").click()
                    driver.find_element(By.ID,"codTarifaPrin").send_keys(cadaImpor)
                    for j in ["javascript:validaTarifa()", "grabaTarifa();"]:
                        driver.execute_script(j)
                        sleep(2)
            sleep(2)
        driver.switch_to.default_content()
        driver.switch_to.frame(driver.find_element(By.NAME,"contenido"))
        driver.execute_script("aceptarPestañas();")
        return driver
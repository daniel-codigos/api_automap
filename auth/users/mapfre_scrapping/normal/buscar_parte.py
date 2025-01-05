from time import sleep
from ..vars import *
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import urllib.parse


class buscar_parte():
    def __init__(self, login, parte, presu):
        self.driver_login = login
        self.elParte = parte['expediente']
        self.todoParte = parte
        self.presu = presu
        self.buscaInfocol(self.driver_login,self.elParte)
        id_parte = self.elParte

    def buscaInfocol(self, driver, elParte):
        duerme = sleep(2)
        driver.switch_to.default_content()
        # aqui ya esta dentro de infocol y ahora buscamos la forma de entrar a los putos frames para tener el code importante y poder interactuar con el.
        for y in [['//frame[@src="/MAPGEN_PR_INFOCOL/app/Principal.jsp"]', 'getServicios("pendientes");'],
                  ['//frame[@src="/MAPGEN_PR_INFOCOL/serviciosNuevos.do"]', 'buscarExpediente("' + elParte + '")']]:
            duerme
            driver.switch_to.frame(driver.find_element(By.XPATH,y[0]))
            duerme

            driver.execute_script(y[1])
            duerme
            if y == ['//frame[@src="/MAPGEN_PR_INFOCOL/app/Principal.jsp"]', 'getServicios("pendientes");']:
                driver.switch_to.default_content()
                duerme
        sleep(2)
        # aqui ya hace click en el unico q salio de la busqueda y le da a descontar y acepta el descuento.
        if not self.presu:
            #try:
            driver.find_element(By.XPATH, '//table[@id="tblServicios"]/tbody/tr[2]').click()
            #except NoSuchElementException:
             #   break
            for h in ["javascript:asumir_descontarServ()", "javascript:aceptarDescuento()"]:
                driver.execute_script(h)
                duerme
            sleep(4)
            print("mi loco tate al loro q fuimos con sleep 150s 1")
            eltext = driver.find_element(By.XPATH, '//textarea[@id="trabajoRealizado"]')
            modpush = eltext.text.split("%2F")
            if "modText" in self.todoParte.keys():
                if self.todoParte['modText']:
                    print("mooodddtext")
                    eltext.clear()
                    eltext.send_keys(modpush[1]+modpush[2]+"  "+self.todoParte['descripcion'])
            sleep(150)
        else:
            driver.find_element(By.XPATH, '//table[@id="tblServicios"]/tbody/tr[2]').click()

            driver.execute_script("javascript:asumir_descontarServ()")

            duerme
            #me da a mi q vamo a tener q hacer un switch frame asi q agarrate
            #src="/MAPGEN_PR_INFOCOL/serviciosNuevos.do"
            driver.switch_to.default_content()

            sleep(10)
            #//frame[@src="/MAPGEN_PR_INFOCOL/serviciosNuevos.do"]
            driver.switch_to.frame(driver.find_element(By.ID, 'contenido'))
            #print("++++++++++++++++++++++++++++++++++++++++")
            #print(driver.page_source)
            driver.find_element(By.XPATH, '//option[@value="4"]').click()
            duerme
            driver.execute_script("javascript:aceptarDescuento()")
            print("mi loco tate al loro q fuimos con sleep 150s 2")
            print(self.todoParte)
            sleep(150)
        # llamamos para q inicie func de descripcion del àrte y le damos driver para q tenga como seguir :D
        return driver
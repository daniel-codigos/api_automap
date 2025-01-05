from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

class finalizar():
    def __init__(self, driver):
        self.driver = driver
        #self.info_itos_poner(self.driver,self.cajon_itos)
        #for x in cajones:self.vaciarTodo(x)
        self.finalizarParte(self.driver)

    def info_itos_poner(self,driver):
        for n,c in enumerate(driver):
            if len(c) > 0:
                print("hay texto")
            else:
                print("no hay texto")


    def finalizarParte(self,driver):
        #print(driver.window_handles)
        #print(len(driver.window_handles))
        #lol = input("\n quieres q se termine esto??: ")
        #print(lol)
        #if lol == "si":
        try:
            driver.execute_script("return typeof aceptarDescuento === 'function';")
            #print("looooooool n")
        except WebDriverException:
            print("La función aceptarDescuento() no existe en el contexto actual.")
        else:
            driver.execute_script("javascript:aceptarDescuento()")
        #else:
        #    print("jojojojojo este noooo")
        sleep(8)
        if len(driver.window_handles) > 1:
            #sleep(3)
            driver.switch_to.window(driver.window_handles[1])
            driver.find_element(By.ID,"idPregMFSi").click()
            driver.execute_script("javascript:respAceptarDescuento()")
            #print(driver.page_source)
            print(driver.window_handles)
            driver.switch_to.window(driver.window_handles[0])
        sleep(3)
        try:
                alerta = self.driver.switch_to.alert
                alerta.accept()
        except NoAlertPresentException:
                print("No se ha encontrado ningún cuadro de diálogo de alerta.")

        #WebDriverWait(driver, 10).until(EC.new_window_is_opened)

        # Cambiar el foco a la nueva ventana, si existe
        #if len(driver.window_handles) > 1:
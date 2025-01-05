from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class dale_no():
    def __init__(self, driver):
        self.driver = driver
        self.daleItos(self.driver)


    def daleItos(self,driver):
        todo = driver.find_element(By.ID,"tablePreguntas")
        losQvalen = todo.find_elements(By.XPATH,'//input[@value="N"]')
        for x in losQvalen:
            cadaID = x.get_attribute("id")
            #print("loooocoooo no te rpingues!!")
            #print(cadaID)
            #loco esto solo si empiezan x preg ya q asi era, y quitas lo de exclusion y relevante. OR los nuevos itos xddddd estos putos...
            if cadaID[:4] == "preg" and cadaID not in ["pregAsistenciaNO","pregCausantes","pregunta"] or cadaID in ["mcaIntervencionTSRNO","mcaIntervencionPeriNO"]:
                try:
                    elemento = driver.find_element(By.ID, cadaID)
                    elemento.click()
                except NoSuchElementException:
                    print("Element not found")
                except ElementNotInteractableException:
                    print("Element not interactable")
        return driver
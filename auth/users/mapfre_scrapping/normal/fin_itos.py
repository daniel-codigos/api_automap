from selenium.webdriver.common.by import By

class hacer_itos():
    def __init__(self, driver, texto):
        self.driver = driver
        self.texto = texto
        self.qRellenar()
        #self.SelecItos(self.driver,"excluido")

    def qRellenar(self):
        relevante = self.texto['rele']
        excluido = self.texto['exclu']
        print(len(relevante))
        print(len(excluido))
        for x in [[relevante,"relevante"],[excluido,"excluido"]]:
            if len(x[0]) > 0:
                self.SelecItos(self.driver,x[1],x[0])


    def SelecItos(self,driver,cual,texto):
        todo = driver.find_element(By.ID,"tablePreguntas")
        losQvalen = todo.find_elements(By.XPATH,'//input[@value="S"]')
        for x in losQvalen:
            cadaID = x.get_attribute("id")
            if cadaID[:4] == "preg" and cadaID != "pregunta" and cadaID != "pregAsistenciaSI":
                if cual == "excluido":
                    if cadaID == "pregSiniestroSI":
                        driver.find_element(By.ID,cadaID).click()
                        driver.find_element(By.XPATH,'//textarea[@id="exclusion"]').send_keys(texto)
                        driver.find_element(By.ID,"pregAsistenciaSI").click()
                if cual == "relevante":
                    if cadaID == "pregInformacionSI":
                        driver.find_element(By.ID,cadaID).click()
                        driver.find_element(By.XPATH,'//textarea[@id="comentarios"]').send_keys(texto)
                        driver.find_element(By.ID,"indiciosNO").click()
        return driver
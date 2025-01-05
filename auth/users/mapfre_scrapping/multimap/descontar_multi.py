from ..vars import  *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class itos_multi():
    def __init__(self, driver):
        self.driver = driver
        self.dale_itos()

    def dale_itos(self):
        #print(self.driver.page_source)
        #idPreguntaNO
        #pregIntervencionPTSRNO
        self.driver.find_element(By.ID,"idPreguntaNO").click()
        self.driver.find_element(By.ID, "mcaIntervencionTSRNO").click()
        self.driver.find_element(By.ID, "mcaIntervencionPeriNO").click()


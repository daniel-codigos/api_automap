from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from ..vars import * # No se muestra, ajusta si necesitas variables
# import urllib.parse  # si no usas, quítalo

class BuscarParte:
    def __init__(self, driver, parte, presu):
        """
        :param driver: WebDriver ya logueado
        :param parte: dict con datos del parte, ej. { 'expediente': 'XXXX', 'descripcion': '...' }
        :param presu: boolean, indica si es o no un presupuesto
        """
        self.driver = driver
        self.parte = parte
        self.el_parte = parte.get('expediente', '')
        self.presu = presu

        self.buscar_infocol()  # realiza la acción al instanciar

    def _switch_to_default(self):
        """ Helper para ir al contenido por defecto """
        self.driver.switch_to.default_content()

    def _switch_frame_by_xpath(self, xpath, timeout=10):
        """
        Cambia de frame usando XPATH. Espera hasta que el frame sea visible.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, xpath))
            )
        except TimeoutException:
            raise TimeoutException(f"No se pudo cambiar al frame con XPATH: {xpath}")

    def _click_table_row(self):
        """
        Hace clic en la fila [2] de la tabla #tblServicios.
        Manejo de NoSuchElementException si no existiera la fila.
        """
        try:
            row = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//table[@id="tblServicios"]/tbody/tr[2]'))
            )
            row.click()
        except (TimeoutException, NoSuchElementException):
            raise NoSuchElementException("No se encontró la fila [2] en la tabla #tblServicios.")

    def _ejecutar_js(self, script):
        """
        Ejecuta un script JavaScript y maneja excepciones de forma genérica.
        """
        try:
            self.driver.execute_script(script)
        except Exception as e:
            # Podrías hacer logging aquí
            print(f"Error ejecutando script JS: {script}. Detalle: {e}")
            raise

    def buscar_infocol(self):
        """Realiza la búsqueda del parte en INFOCOL y procede al descuento o presupuesto."""

        # 1) Frame principal
        self._switch_to_default()
        self._switch_frame_by_xpath('//frame[@src="/MAPGEN_PR_INFOCOL/app/Principal.jsp"]')

        # getServicios("pendientes");
        self._ejecutar_js('getServicios("pendientes");')

        # 2) Regresar al default y cambiar al frame de serviciosNuevos
        self._switch_to_default()
        self._switch_frame_by_xpath('//frame[@src="/MAPGEN_PR_INFOCOL/serviciosNuevos.do"]')

        # 3) Llamada a buscarExpediente con el número
        js_buscar = f'buscarExpediente("{self.el_parte}")'
        self._ejecutar_js(js_buscar)

        # 4) Esperar a que aparezca la fila, hacer clic
        self._click_table_row()

        # 5) Lógica: si no es presu => asumimos/descargamos el parte
        if not self.presu:
            self._ejecutar_js("javascript:asumir_descontarServ()")

            # Esperamos un poco a que se cargue algo o se habilite
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//textarea[@id="trabajoRealizado"]'))
            )
            self._ejecutar_js("javascript:aceptarDescuento()")

            # Esperar a que aparezca 'trabajoRealizado'
            desc_box = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//textarea[@id="trabajoRealizado"]'))
            )
            texto_original = desc_box.get_attribute('value')  # .text vs. .get_attribute('value')

            # Si hay modText en parte
            if self.parte.get('modText'):
                # Example: a tu string modpush. Adaptar si es distinta la lógica
                fragmentos = texto_original.split("%2F")
                # Reemplazarlo con algo
                if len(fragmentos) > 2:
                    nuevo_texto = fragmentos[1] + fragmentos[2] + "  " + self.parte['descripcion']
                else:
                    # fallback
                    nuevo_texto = texto_original + "  " + self.parte['descripcion']

                desc_box.clear()
                desc_box.send_keys(nuevo_texto)

        # 6) Si es presu => se asume, se cambia el select, se confirma
        else:
            self._ejecutar_js("javascript:asumir_descontarServ()")
            self._switch_to_default()

            # 6.1) Cambiar al frame 'contenido' y seleccionar la opción "4" => valor para presu
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.frame_to_be_available_and_switch_to_it((By.ID, 'contenido'))
                )
            except TimeoutException:
                raise TimeoutException("No se encontró frame con ID='contenido' para presu")

            # Seleccionar la opción
            try:
                option_presu = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//option[@value="4"]'))
                )
                option_presu.click()
            except (TimeoutException, NoSuchElementException):
                raise NoSuchElementException("No se encontró <option value='4'> en 'contenido'.")

            # 6.2) Aceptar
            self._ejecutar_js("javascript:aceptarDescuento()")

        # Fin del proceso
        print(f"Proceso de {self.el_parte} finalizado con presu={self.presu}.")
        return self.driver

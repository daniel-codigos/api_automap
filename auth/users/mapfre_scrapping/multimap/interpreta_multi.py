from ..vars import  *
#import class_funciona_web.class_aceptar_fin as aceptar_fin
from ..normal.interpreta_texto import analiza
#import class_funciona_web.class_hacer_asistencia as hacer_asis

class crear_multi():
    def __init__(self,desc,brico, cerebro):
        #self.info = info
        print("aqui llega socio")
        self.cerebro = cerebro
        self.brico = brico
        self.desc = desc
        self.crear_info_multi()

    def crear_info_multi(self):
        limita_parte = [" PARTIDAS:  1.","- Ud: 1 -"]
        #descripcion_limpia = self.desc.split(limita_parte[0])[1].split(limita_parte[1])[0]
        try:
            descripcion_limpia = self.desc.split(limita_parte[0])[1].split(limita_parte[1])[0]
        except Exception as e:
            print(f"Se produjo una excepción: {e}")
            descripcion_limpia = self.descin
        analiza(descripcion_limpia, self.brico, self.cerebro)

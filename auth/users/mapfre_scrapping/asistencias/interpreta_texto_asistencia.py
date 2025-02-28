from ..vars import  *
#import class_funciona_web.class_aceptar_fin as aceptar_fin
#import class_funciona_web.class_hacer_asistencia as hacer_asis

class crear_asistencia():
    def __init__(self,info):
        self.info = info
        self.precio = ""
        self.porcentaje = ""
        self.crear_info_asistencias()

    def crear_info_asistencias(self):
        #print(self.info.split('Fecha Presupuesto:')[1].split('.'))
        todo_busca = ["Importe total cliente sin ","Impuesto IVA/IGIC/IPSI aplicado:"]
        buscar = ["Importe total cliente sin ","Impuesto IVA/IGIC/IPSI aplicado:"]
        presupuesto = "*** PRESUPUESTO ***"
        if len(self.info.split(presupuesto)) > 1:
            self.precio = '0'
            self.porcentaje = 'presu'
        else:

            for cada_buscao in todo_busca:
                if cada_buscao in str(self.info):
                    if len(self.info.split('Fecha Presupuesto:')) > 1:
                        for x in self.info.split('Fecha Presupuesto:')[1].split('.'):
                            for num,cadaBuscar in enumerate(buscar):
                                if len(x.split(cadaBuscar)) > 1:
                                    if num == 0:
                                        lamovi = float(x.split(': ')[1].split(' ')[0].replace(',','.')) / 1.12
                                        self.precio = str(round(lamovi,2))
                                    else:
                                        self.porcentaje = x.split('IVA')[1].split(':')[1].replace(' ', '')
                    break
                else:
                    self.precio = '0'
                    self.porcentaje = 'Error'
        #print(self.precio)
        #si no hay porcentaje break de tooo
        print(self.info)
        #if self.precio and self.porcentaje:
        importes.append([self.porcentaje,self.precio])
        #else:
         #   print("jajejajijsid")


    #def terminarTodo(self,como):
    #    if como == 'fin':
    #        print("hopla")
            #hacer_asis.ingresar_porcentaje(self.driver,self.porcentaje)
            #hacer_asis.ingresar_importe(self.driver,self.text_final_precio.get())
            #aceptar_fin.finalizar(self.driver)
     #   else:
     #       self.driver.execute_script("javascript:cancelarDescuento()")

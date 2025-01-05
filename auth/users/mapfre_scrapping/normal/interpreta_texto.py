from ..vars import *
from urllib.parse import unquote
import difflib


def saveInfo(data):
    data1 = "txtinfo.txt"
    with open(data1, "a") as file:
        for x in [data,"\n","------------------------------------------------------------------------------"]:
            file.write(x)

def normalizar(s,dic):
    replacements = dic
    for a, b in replacements:
        s = s.replace(a.lower(), b.lower())
    return s

def has_similar_element(textArray, cada_default_keys, threshold=0.85):
    con = []
    for idx, element in enumerate(textArray):
        similarity = difflib.SequenceMatcher(None, cada_default_keys, element).ratio()
        if similarity == 1.0:
            con.append(idx)
            #return [True, idx]  # 100% de coincidencia, no se modifica el elemento
        elif similarity >= threshold:
            #el bug es que cuando reemplazamos tambien encuentra la siguiente jajajaja entonces se duplicaaaa
            con.append(idx)
    return [True,con] if con else False

class analiza():
    def __init__(self,texto, brico, cerebro):
        print("ni entra xd")
        self.brico = brico
        print("aqui si xd jaja")
        self.rem = cerebro["remplazos"]
        self.fallida = self.array_to_rem(cerebro["fallida"])
        self.anulado = self.array_to_rem(cerebro["anulado"])
        self.suminis = self.array_to_rem(cerebro["bus_suminis"])
        #self.default = cerebro["default"]
        #tengo que hacer que coja default dos de su respectiva db.
        print("aqui buenoooooo")
        self.default = self.convert_old_json(cerebro["default"])
        print("loooooooooooooooooc")
        print(self.default)
        print(self.fallida)
        print(self.anulado)
        print(self.suminis)
        print(1)
        self.suministros = cerebro["default"]['suministros']
        print(2)
        self.importes = []
        self.numeros = numeros
        self.ez = self.array_to_rem(cerebro["ez"])
        #print(self.driver)
        print("tamos locos")
        print(">>>>>")
        resultado = self.descripcionParte(texto)
        importes.append(self.importes)
        #print(self.importes)

    def array_to_rem(self,arr):
        new = []
        for x in arr:
            new.append(normalizar(x,self.rem))
        return new


    def convert_old_json(self,old):
        new = {}
        for x in old:
            for cada_nom in old[x]:
                #print("flipas")
                normalized_nombre = normalizar(cada_nom,self.rem)
                #if normalized_nombre.endswith("e"):
                #    new.update({normalized_nombre[:-1]: old[x][cada_nom]})
                new.update({normalized_nombre: old[x][cada_nom]})
        return new


    def dale(self, data, pala, canti):
        cantidad = canti
        palabra = pala
        print(palabra)
        print(self.default[palabra])
        #el fallo es que tambien le tengo que enseñar aqui... o pensar en como puede llegar aqui sabiend la posi del eleemento tmabien de default
        if self.default[palabra]:
            if self.importes == ["yyt"] and len(self.importes) <= 2 or self.importes[0] == "guardia" and len(self.importes) <= 3:
                #print("ha entradooo")
                if cantidad > "1":
                    for auto1 in [[self.default[palabra][0], "1"], [self.default[palabra][1], str(int(cantidad) - int("1"))]]:
                        # aqui un puto se guarda como integral y me esta jodiendo el mamon. AQUIIIII
                        print('primiko1')
                        self.importes.append(auto1)
                    for auto2 in [cantidad, palabra]:
                        if auto2 in data:
                            data.remove(auto2)
                else:
                    print('primiko2')
                    self.importes.append([self.default[palabra][0], cantidad])
                    for auto1 in [cantidad, palabra]:
                        if auto1 in data:
                            data.remove(auto1)
            else:
                print('primiko3')
                if self.default[palabra][1] == 'sht':
                    if int(cantidad) > 5:
                        cantidad = '2'
                    elif int(cantidad) > 10:
                        cantidad = '3'
                    elif int(cantidad) > 15:
                        cantidad = '4'
                    else:
                        cantidad = '1'
                self.importes.append([self.default[palabra][1], cantidad])
                # #print(default[palabra][1])
                # #print(cantidad)

    def buscar_suministros(self, text_array):
        print("hiiii")
        print(text_array)
        print(self.suministros)
        #creo que es bu8ena opcion mirar los suministros despues de encontrar la palabra.
        for cada_sumis in self.suministros:
            normal = normalizar(cada_sumis,self.rem)
            if normal in text_array:
                print("encontrao:")
                print(self.suministros[cada_sumis])
                #temabien le tengo que enseñar que mire la palabra de antes y si es algun numero que meta ese en cantidad, ESTA YA ESTA HECHO DE ANTES!! BUSCA EN EL PROYECTO!!
                #pilla la palabra clave y lo que haya despues y ya esta fin con un break
                #self.importes.append([self.default[palabra][1], cantidad])
                break
        print("hola")

#empieza aqui y de aqui entra en dale
    def descripcionParte(self,texto):
        print("chungo")
        ori = normalizar(unquote(texto).lower(),self.rem)
        existeNum = bool
        ledamos = bool
        textArray = ori.split(" ")
        print(textArray)
        #hay q mejorar esto y las exclusiones, las 2 primeras deben ser 1 y mirar...
        #mete btn de borrar y añadir en react!!
        for cada_exclu in self.ez:
            #k es para saber si es una exclusion o no cucu
            #aqui es para que si es exclu peeeero tiene algo que se repone o sustituye
            if cada_exclu in ori and not any(item in textArray for item in ["repone","utituye"]) and not any(item in textArray for item in self.suminis):
                print("meeeeeeeeeeeeeeeec excluido")
                ledamos = False
                break
            else:
                ledamos = True

        if any(item in self.suminis for item in textArray):
            #esta bien pero debes hacer un check para que no se cuelen partes como: se devuelve el suministro de luz a la vivienda.
            #otro ejemplo :  Se restablece el suministro eléctrico total en vivienda
            #pero hay partes que tienen esto escrito aun teniendo que suministrar algo. Igual es mejor hacerle entender luego que tiene q suministrar o no con los importes x ejemplo.
            print("JODER SE SUMINISTRAAAAA!!!")
            print(self.suminis)
            print(self.suministros)
            self.buscar_suministros(textArray)
            #no esta default organizado con categorias como en react, pensar como sacar suministro de default
        #ya no se necesita ver texto y buscar guardia desde update de fecha de asignacion de mapfe xddddddd xfin argo primiko
        #if "guardia" in textArray:
            #self.importes.append("guardia")
        print("kansdjknaskldjbnkas")
        print(type(ori))
        print(self.fallida)
        if "bricolaje" in textArray and textArray.index("bricolaje") < 6 or self.brico == 'si' and not any(str(item) in str(ori) for item in self.fallida) and not any(str(item) in str(ori) for item in self.anulado):
            print("yyt jodeeeeeeeeer")
            print(self.fallida)
            self.importes.append("yyt")
        #elif any(item in textArray for item in self.fallida):
        elif any(str(item) in str(ori) for item in self.fallida):

            print("primooooooooooooooooooooooooooooo")
            for h in ["yyt", "lvt"]:
                self.importes.append(h)
            return
        #elif any(item in textArray for item in self.anulado):
        elif any(str(item) in str(ori) for item in self.anulado):
            print("dotooooorrrr anula")
            print(any(str(item) in str(ori) for item in self.anulado))
            print(str(ori))
            print(self.anulado)
            for h in [["zb9","0"]]:
                self.importes.append(h)
            return
        else:
            #~quizass si no es brico meter algo pa q quiite morralla cuando es un suministro que describen mucho... o no se
            print(self.anulado)
            print(ori)
            print("no es ningun diccionario encontrado!!")
            for h in ["yyt", "lat"]:
                self.importes.append(h)
        for k in self.numeros:
            if k in textArray:
                existeNum = True
                break
            else:
                existeNum = False
        if not existeNum:
            if ledamos:
                for k in self.default.keys():
                    if k in textArray:
                        self.dale(textArray, k, "1")
        else:
            #si no es una exclusion:
            if ledamos:
                print("aqui suuuuuuuuuuuuuuuu")
                try:
                    print(self.default)
                    #print(self.default)
                    for cada_default_keys in self.default.keys():
                        check_similar_text = has_similar_element(textArray, cada_default_keys)
                        if check_similar_text != False:
                            print("--------------------------------------------------++")
                            print(check_similar_text)
                            print(cada_default_keys)
                            print(textArray)
                            #palabra es la palabra que encontramos jeje ;) aqui testaco de los enchufes a 0 ostiaaa
                            palabra_bonita = cada_default_keys
                            print(check_similar_text[1])
                            if len(check_similar_text[1]) > 1:
                                    #si hay mas de una coincidencia!!! ojo!!!
                                palabra = check_similar_text[1]
                            else:
                                palabra = textArray[check_similar_text[1][0]]
                            ult_ojo_mira = None
                            #falta por colocar ojo con esta revisar o sin falta solo por colocar
                            cuidado = "in colocar"
                            ojo = []
                            ##testea esto tio creo q hay fallo ya que si existe in o colocar lo falla. mete colocar en textarray fuera del bucle y comprueba con print
                            if cuidado in ori:
                                print("wey wey weyyyy weyyyy")
                                ult_ojo_mira = True
                            if ult_ojo_mira == None:
                                if type(palabra) != list:
                                    print(palabra)
                                    print(type(palabra))
                                    print("seguimoss paa")
                                    if textArray[textArray.index(palabra) - 1] in self.numeros:
                                        #aqui sacamos cantidades
                                        cantidad = textArray[textArray.index(palabra) - 1]
                                    else:
                                        cantidad = "1"
                                    try:
                                        print(textArray)
                                        print(palabra_bonita)
                                        print(cantidad)
                                        print("importes:")
                                        print(self.importes)
                                        self.dale(textArray, palabra_bonita, cantidad)
                                        print("--------------------------------------------------++")
                                    except ValueError:
                                        print("Aqui meter cancelar parte xk sa vuelto mas loco q lokin")
                                        break
                                else:
                                    for cada_pa_repetida in palabra:
                                        if textArray[int(cada_pa_repetida) - 1] in self.numeros:
                                            cantidad = textArray[int(cada_pa_repetida) - 1]
                                        else:
                                            cantidad = "1"
                                        try:
                                            print("ESTAMOS EN DOBLEEEEEEEEEEEEEEEEES JAJAJAJAJAJJAJA")
                                            print(textArray)
                                            print(palabra_bonita)
                                            print(cantidad)
                                            print("importes:")
                                            print(self.importes)
                                            self.dale(textArray, palabra_bonita, cantidad)
                                            print("--------------------------------------------------++")
                                        except ValueError:
                                            print("Aqui meter cancelar parte xk sa vuelto mas loco q lokin")
                                            break

                except KeyError:
                    print("KEYERROR :(")
                except TypeError:
                    print("TYPEeRROR :(")
                    print("- ")
        return [self.importes]
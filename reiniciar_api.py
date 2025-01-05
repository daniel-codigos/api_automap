#!/usr/bin/python
#import botaso.var as var
import os
import subprocess


class reset_bot_users():
    def __init__(self,lista):
        self.lista = lista
        self.reiniciar_lista(self.lista)

    def reiniciar_lista(self,lista):
        for cadaUno in lista:
            if cadaUno != 'db':
                reset_bot(cadaUno)

class reset_bot():
    def __init__(self,file):
        self.file = file
        #self.ruta = var.ruta_bot_users
        self.reinicia()

    def reinicia(self):
        print("asd")
        #os.system("pkill -f "+self.file)
 #       subprocess.Popen(["screen","-dm","-S", "botaso_"+self.file, "python3", self.ruta+self.file])


def reset_prin():
    subprocess.Popen(["screen", "-dmL","-Logfile", "/home/pi/logs/screenlogmap.0", "-S", "apii", "python3", "/home/pi/api_map/auth/manage.py", "runserver", "192.168.1.44:2230"])



if __name__ == "__main__":
    #os.system('pkill -f ".py"')
    #list_bot_user = os.listdir(var.ruta_bot_users)
  #  reset_bot_users(list_bot_user)
    reset_prin()



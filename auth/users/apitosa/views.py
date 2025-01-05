from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from ..mapfre_scrapping.normal.interpreta_texto import analiza
from ..opciones_fast import *
import time
from ..serializers import UserSerializer
from ..mapfre_scrapping import login_mapfre, vars, sacar_listado_partes
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from ..models import User, Register_new_hour
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_off(request):
    user = request.user
    vars.importes.clear()
    vars.listado_partes.clear()
    vars.info_todos_partes.clear()
    print("Empezamos a descontar!!!!!!!")
    print(user.id)
    #for cada_parte in request.data['info']:
    if test_desc == "si":
        login_mapfre.sacar_partes('descontar', request.data['info'], "test", user)
    else:
        info = SaveUser.objects.filter(user=user).first()
        print("a lo q estamos ja")
        print(info)
        if info:
            creden_info = {'user': info.username_infocol, 'passwd': info.password_infocol}
            username = creden_info['user']
            password = creden_info['passwd']
            login_mapfre.sacar_partes('descontar', request.data['info'], "nada",user,creden_info)

    return Response({'info':vars.noDescontados})




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_in_hour(request):
    user = request.user
    info = user.register_new_hour_set.all()
    serializer = register_hour_serializer(info, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def hour_view_register(request):
    serializer = register_hour_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response()


class delete_hourss(APIView):
    def get(self,request,id):
        dele = Register_new_hour.objects.get(id=int(id))
        dele.delete()
        return Response()


class getConfig(APIView):
    def get(self, request):
        user = request.user
        info = user.save_config_set.all()
        print(f"Info: {info}")  # Agrega este mensaje para verificar si la lista está vacía o no

        if info:
            if info[0].json:
                print(info[0].json)
                return Response(info[0].json)
            else:
                return Response({"Error": "¡No existe nada!"})
        else:
            return Response({"Error": "¡No se encontraron datos!"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_in(request):
    #start
    user = request.user
    vars.importes.clear()
    vars.listado_partes.clear()
    vars.info_todos_partes.clear()
    config = getConfig()
    #print(info[0])
    #time.sleep(60)
    cerebro = config.get(request).data
    print("cerebroo:")
    print(cerebro)
    if test_desc == "si":
        info = user.save_bad_set.all()
        print(info)
        cont = 0
        for num,cadainfo in enumerate(info):
            if cadainfo.json['expediente'][0] != "ç":
                print("-----------------------------------------------------------------")
                print(cadainfo.id)
                cadainfo.json["imp_anti"] = cadainfo.json['importes']
                #print(x.json['expediente'][0])
                print(cadainfo.json['descripcion'])
                analiza(cadainfo.json['descripcion'], cadainfo.json['brico'], cerebro)
                time.sleep(.1)
                print(vars.importes)
                time.sleep(.1)
                print(vars.importes[cont])
                cadainfo.json['importes'] = vars.importes[cont]
                #cadainfo.json["test"] = "si"
                cadainfo.json["id_ex"] = cadainfo.id
                vars.listado_partes.append(cadainfo.json)
                cont += 1
        print("mira estooooo ostiaaaa")
        print(len(vars.listado_partes))
        print(vars.listado_partes)
        return Response({'test':'si','info':vars.listado_partes})
    else:
        try:
            #login_mapfre.sacar_partes('sacar_partes',None,cerebro,user)
            #print("mira estooooo ostiaaaa")
            #print(len(vars.listado_partes))
            #print(vars.listado_partes)
            #return Response({'test':'no','info':vars.listado_partes})
            info = SaveUser.objects.filter(user=user).first()
            print("a lo q estamos ja")
            print(info)
            if info:
                creden_info = {'user':info.username_infocol,'passwd':info.password_infocol}
                username = creden_info['user']
                password = creden_info['passwd']
                print(username)
                print(password)
                sacar_listado = sacar_listado_partes.SacarListado(username, password,cerebro)

                try:
                    print("Iniciando sesión...")
                    sacar_listado.login()
                    print("Accediendo a la pantalla principal...")
                    sacar_listado.cargar_pagina_principal()
                    print("Cargando página de inicio...")
                    sacar_listado.cargar_inicio()
                    print("Obteniendo lista de servicios pendientes...")
                    servicios = sacar_listado.obtener_servicios_pendientes()

                    print("Servicios obtenidos:")
                    for servicio in servicios:
                        print(servicio)
                except Exception as e:
                    print(f"Error: {e}")
            return Response({'test':'no','info':vars.listado_partes})
        except Exception as e:
            print(e)


#saveConfig
class saveConfig(APIView):
    def post(self, request):
        try:
            user = request.user  # obtener el usuario actual
            # buscar si existe un registro previo con el mismo usuario
            prev_config = Save_config.objects.filter(user=user)
            if prev_config.count() > 0:
                prev_config.delete()  # eliminar el registro previo
            for cada_tabla in request.data['json']:
                if cada_tabla not in ["default","bus_suminis"]:
                    request.data['json'][cada_tabla] = [item for item in request.data['json'][cada_tabla] if item is not None]
            #data = json.dumps(request.data)
            data = request.data
            serializer = save_config_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(request.data)
        except Exception as e:
            error_message = str(e)
            return Response({"error": error_message})


class saveUser(APIView):
    def post(self, request):
        try:
            user = request.user  # obtener el usuario actual
            data = request.data
            print(data)
            # buscar si existe un registro previo con el mismo usuario
            prev_config = SaveUser.objects.filter(user=user)
            print(prev_config.count())
            if prev_config.count() > 0:
                print("ya tenemos user putasoooo, hay que modificar lo guardadooo")
            else:
                print("amos a crearlooooo")
                data = {'user':user.id,'username_infocol':data['user'],'password_infocol':data['pass']}
                print(data)
                serializer = save_user(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'Saveit': 'ok'})
                #print(serializer.is_valid(raise_exception=True))
            #prev_config.delete()  # eliminar el registro previo
        except Exception as e:
            error_message = str(e)
            return Response({"error": error_message})


class saveBad(APIView):
    def post(self,request):
        try:
            data = request.data
            user = request.user
        #en windows funciona bien sin nada, en linux igual tengo que pasarlo a unicode.
            print(type(data))
            print(data)
            data['user'] = user.id
            print(data)
            serializer = SaveBadParteSerial(data=data)
            if serializer.is_valid(raise_exception=True):
                print(serializer)
                serializer.save()
                return Response(request.data)
        except Exception as e:
            print('errorrrrr')
            error_message = str(e)
            print(error_message)
            return Response({"error": error_message})



class removeBad(APIView):
    def post(self,request):
        try:
            user = request.user
            data = request.data
            print(data['info'])
            serializer = save_bad_info(data={'json': data['info']})
            print("lol")
            print(serializer)
            #serializer.is_valid(raise_exception=True)
            print("lal")
            print(data['info']['id_ex'])
            match_re = Save_bad.objects.filter(id=data['info']['id_ex'])
            print(match_re)
            deleted_count = match_re.delete()
            print(deleted_count)
            print("finito")
            return Response("Datos eliminados exitosamente", status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

class piensaBad(APIView):
    def post(self,request):
        try:
            data = request.data
            print(data)
            vars.importes.clear()
            vars.listado_partes.clear()
            vars.info_todos_partes.clear()
            config = getConfig()
            cerebro = config.get(request).data
            #aqui enviar datos a cabeza pensante
            print(data['info'])
            print("lol")
            print("+------------------------------------------------------------------+")
            analiza(data['info']['descripcion'], data['info']['brico'], cerebro)
            print("+------------------------------------------------------------------+")
            time.sleep(.1)
            print(vars.importes)
            time.sleep(.1)
            print(vars.importes)
            data['info']['importes'] = vars.importes[0]
            # cadainfo.json["test"] = "si"
            #data.json["id_ex"] = cadainfo.id
            print(data)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            error_message = str(e)
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_info(request):
    auth = get_authorization_header(request).split()
    print('aquiiii:')
    print(auth)
    if auth and len(auth) == 2:
        print('entrar entra')
        print(request)
        token = auth[1].decode('utf-8')
        #aqui es donde dice desautentificado, linea de abajo
        #id = decode_access_token(token)[0]
        print('lolaso')
        id="lol"
        user = User.objects.filter(pk=id).first()
        print('lol')
        print("axooooooooooooooooooooooooooooo")
        print(UserSerializer(user).data)
        return Response(UserSerializer(user).data)
    raise AuthenticationFailed('Desautentificado!lol')
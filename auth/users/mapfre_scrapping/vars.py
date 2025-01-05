info_todos_partes = []
listado_partes = []
id_parte=''
todos_partes = []
checked_checks = []
limpieza = ["/*EL SERVICIO DISPONE DE DOCUMENTACIÓN*/","/*EL SERVICIO DISPONE DE PARTE DE TRABAJO*/"]
importe_seleccionado = []
importes = []
numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32"]
ez = ["rearma el diferencial", "falo contacto", "dañado por humedad", "e conecta cable uelto", "funcionan correctamente","e dconecta y e rtablece","todo ta correcto", "va todo correcto", "mal contacto", "fallo interno del mimo", "problema interno", "e dmonta y e dconecta", "e tablece el uminitro", "e revia y e repara conexion detra de", "no hay alteracion electrica", "funciona perfectamente", "todo ta en condicion", "e conecta y queda todo funcionando", "e encuentra correcta", "contacto uelto", "conexion uelta", "e encuentra correcto", "se aconeja actualizar", "recibe tenion correctamente", "parte anulado", "excluida", "excluido", "uperacion de conumo contratado", "por uperacion de conumo", "no e trata de averia electrica", "no e trata de 1 averia electrica", "e trata de mantenimiento", "por 1 fallo de", "funciona correctamente", "e deja anulado"]
noDescontados = []

#diccionario de suministros :D
suministros = {
    "diferencial": ['pat', 'dat'],
    "magnetoterminco": ['pat', 'iat'], #tambien automatico
    "dpn": ['pat', 'ift'],
    "fusible 63" : ['pat', '15'],
    "mecanismo doble": ['tat']
}



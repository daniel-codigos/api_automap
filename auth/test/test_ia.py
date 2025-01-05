import requests
import json

# Preparar la carga útil con instrucciones mejoradas
payload = {
    "model": "llama3.2:1b",
    "messages": [
        {"role": "assistant", "content": "Eres un secretario experto en análisis de descripciones de trabajo y debes generar un JSON detallado basado y ajustado únicamente a la información proporcionada por el usuario."},
        {"role": "assistant", "content": "Para cada descripción, sigue estas reglas:\n1. Si se menciona 'bricolaje', establece 'bricolaje': 'si'.\n2. En 'materiales', incluye solo objetos mencionados explícitamente. Usa la estructura {'nombre': <nombre del material>, 'cantidad': <cantidad>, 'material': 'asegurado' o 'suministrado'}.\n3. Marca un material como 'suministrado' solo si se especifica claramente en el texto. Si no se menciona 'suministrado', siempre debe ser 'asegurado'."},
        {"role": "assistant", "content": "Ejemplos correctos:\n- Si el texto es 'Se coloca un mecanismo y se recolocan 2', el JSON debe ser:\n{\n\t\"bricolaje\": \"si\",\n\t\"materiales\": [{\"nombre\": \"3 mecanismos\", \"cantidad\": 3, \"material\": \"asegurado\"}]\n}\n- No infieras materiales adicionales ni cambies 'asegurado' a 'suministrado' sin una indicación clara."},
        {"role": "user", "content": "Se verifica enchufe del dormitorio y se encuentra funcionando correctamente.Se limpia y se recoloca ( estaba manchado cuando han enchufado la lámpara de mesa yse  ha producido un corto interno de la lámpara. Excluido "}
    ],
    "format": "json",
    "stream": False,
    "options": {
        "temperature": 0.3
    }
}

# Realizar la solicitud a la API
response = requests.post(
    "http://192.168.1.110:11434/api/chat",
    json=payload
)

# Analizar y mostrar la respuesta JSON
response_json = response.json()
print(json.dumps(response_json, indent=4))
print(response_json['message']['content'])

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProgressInfo(AsyncWebsocketConsumer):
    async def connect(self):
        print(f"esto es scope:{self.scope}")
        user = self.scope.get('user')
        if user:
            self.group_name = f"user_{user}"
            print(self.group_name)
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            print(f"Conexión aceptada para el usuario: {user}")
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Mensaje recibido: {data}")
        # Responde al cliente si es necesario
        await self.send(text_data=json.dumps({
            'message': 'Datos recibidos',
            'received': data
        }))

    async def send_progress(self, event):
        # Envía actualizaciones de progreso al cliente
        print("vamos a enviaaarrrr")
        print(json.dumps(event['progress_data']))
        await self.send(text_data=json.dumps(event['progress_data']))

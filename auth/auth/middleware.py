from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import AccessToken
from urllib.parse import parse_qs


class WebSocketTokenAuthMiddleware(BaseMiddleware):
    """
    Middleware para autenticar conexiones WebSocket utilizando tokens JWT.
    """

    async def __call__(self, scope, receive, send):
        query_string = scope['query_string'].decode()
        params = parse_qs(query_string)

        user = params.get('user', [None])[0]
        token = params.get('token', [None])[0]
        print(f"esto es user:{user} y esto es token: {token}")
        if token:
            try:
                validated_token = AccessToken(token)
                scope['user'] = validated_token['user_id']  # Ajusta según tu modelo
                print(f"Usuario autenticado: {scope['user']}")
            except Exception as e:
                print(f"Token inválido: {e}")
                scope['user'] = None
        else:
            scope['user'] = user  # Si no hay token, asigna directamente el usuario

        return await super().__call__(scope, receive, send)

from django.urls import path
from .info_partes import ProgressInfo

ws_url = [
    path('ws/process', ProgressInfo.as_asgi()),
]

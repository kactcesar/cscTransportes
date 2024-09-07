from django.urls import path
from . views import *

app_name = 'viagens'

urlpatterns = [
    
    path('', viagens_index, name='charts_index'),
    path('dados_viagem_lista/', dados_viagem_lista, name='dados_viagem_lista'),
    path('grafico_viagem_lista/', grafico_viagem_lista, name='grafico_viagem_lista'),
    path('obter_dados_grafico/', obter_dados_grafico, name='obter_dados_grafico'),

]
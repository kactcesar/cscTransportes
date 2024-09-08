from django.urls import path
from . views import *

app_name = 'viagens'

urlpatterns = [
    
    path('', viagens_index, name='charts_index'),
    path('dados_tabela_lista/', dados_tabela_lista, name='dados_tabela_lista'),
    path('querry_tabela_lista/', querry_tabela_lista, name='querry_tabela_lista'),
    path('querry_lista/', querry_lista, name='querry_lista'),
    path('dados_grafico/', dados_grafico, name='dados_grafico'),

]
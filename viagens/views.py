from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from .querry import*
from viagens.serializador import *
from django.db import DatabaseError
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

def viagens_index(request):
    return render(request, 'viagens/charts.html')


dadosTabela = {}

def querry_tabela_lista(request):  
    start_date_tab = request.GET.get('start_date_tab')
    end_date_tab = request.GET.get('end_date_tab')
    
    dados = consulta(start_date_tab, end_date_tab)
    print(dados)
    
    global dadosTabela
    dadosTabela = dados
    
    if 'error' in dados:
        return JsonResponse({
            'error': dados['error'],
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
        
    return JsonResponse({'dados': dados})


def dados_tabela_lista(request):
    global dadosTabela

    return JsonResponse({'dados': dadosTabela})


dadosGrafico = {}

def querry_lista(request):  
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    dados = consulta_grafico(start_date, end_date)  
    global dadosGrafico
    dadosGrafico = dados
    
    if 'error' in dados:
        return JsonResponse({
            'error': dados['error'],
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
        
    return JsonResponse({'dados': dados})

@require_GET
def dados_grafico(request):
    global dadosGrafico

    if not dadosGrafico:
        return JsonResponse({'error': 'Nenhum dado disponível'}, status=404)

    return JsonResponse({'dados': dadosGrafico})
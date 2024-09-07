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
# View que retorna o resultado da consulta SQL em JSON



def dados_viagem_lista(request):
    dados = consulta()
    if 'error' in dados:
        return JsonResponse({
            'error': dados['error'],
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
    # Envolva os dados retornados dentro da chave 'data'
    return JsonResponse({'dados': dados})


dadosGrafico = {}

def grafico_viagem_lista(request):  
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    dados = consulta_grafico(start_date, end_date)
    print(dados)
    
    global dadosGrafico
    dadosGrafico = dados
    
    if 'error' in dados:
        return JsonResponse({
            'error': dados['error'],
            'aviso': 'Problema ao consultar os dados'
        }, status=500)
        
    return JsonResponse({'dados': dados})

@require_GET
def obter_dados_grafico(request):
    # Retornar os dados armazenados na variável global
    global dadosGrafico

    if not dadosGrafico:
        return JsonResponse({'error': 'Nenhum dado disponível'}, status=404)

    return JsonResponse({'dados': dadosGrafico})
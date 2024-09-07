from django.db import connection, DatabaseError
from django.http import JsonResponse

# Função que executa a query SQL personalizada
def consulta():
    with connection.cursor() as cursor:
        try:
            query = """
                    SELECT
                    driver_id AS id_motorista,
                    COUNT(id) AS total_viagens,
                    SUM(total_time) AS tempo_total_viagem,
                    SUM(fuel_used) AS combustível_usado,
                    SUM(count_over_speed) AS total_excessos_velocidade
                FROM
                    dadosviagem  
                WHERE
                    start_time >= '2024-01-01' AND start_time < '2024-03-01'
                GROUP BY
                    driver_id
                ORDER BY
                    total_viagens DESC;

            """
            # Executar a consulta
            cursor.execute(query)
            rows = cursor.fetchall()

            # Pegar os nomes das colunas para criar o dicionário
            columns = [col[0] for col in cursor.description]

            # Construir o dicionário de resultados
            resultados = [dict(zip(columns, row)) for row in rows]
            return resultados
        
        except DatabaseError as error:
            print(error)
            return {'error': str(error)}



def consulta_grafico(start_date, end_date):
    with connection.cursor() as cursor:
        try:
            query = """
                WITH desempenho AS (
                SELECT
                    driver_id,
                    SUM(count_over_speed) AS total_excessos_velocidade
                FROM
                    dadosviagem
                WHERE
                    start_time >= %s AND start_time < %s
                GROUP BY
                    driver_id
            )
            SELECT
                CASE
                    WHEN total_excessos_velocidade = 0 THEN 'Eficiente'
                    WHEN total_excessos_velocidade <= 5 THEN 'Moderadamente Eficiente'
                    WHEN total_excessos_velocidade <= 10 THEN 'Ineficiente'
                    ELSE 'Muito Ineficiente'
                END AS categoria,
                COUNT(driver_id) AS quantidade_motoristas
            FROM
                desempenho
            GROUP BY
                categoria
            ORDER BY
                quantidade_motoristas DESC;

            """
            # Executar a consulta
            cursor.execute(query, [start_date, end_date])
            rows = cursor.fetchall()

            # Pegar os nomes das colunas para criar o dicionário
            columns = [col[0] for col in cursor.description]

            # Construir o dicionário de resultados
            resultados = [dict(zip(columns, row)) for row in rows]
            return resultados
        
        
        except DatabaseError as error:
            print(error)
            return {'error': str(error)}
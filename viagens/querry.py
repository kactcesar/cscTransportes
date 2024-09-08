from django.db import connection, DatabaseError
from django.http import JsonResponse

# Função que executa a query SQL personalizada
def consulta(start_date_tab, end_date_tab):
    with connection.cursor() as cursor:
        try:
            query = """
                    SELECT
                driver_id AS id_motorista,
                COUNT(id) AS total_viagens,
                TO_CHAR(TO_TIMESTAMP(SUM(total_time)), 'HH24:MI:SS') AS tempo_total_viagem,
                ROUND(SUM(fuel_used) / 1000, 2) AS combustivel_usado_litros,
                SUM(count_over_speed) AS total_excessos_velocidade
            FROM
                dadosviagem  
            WHERE
                start_time >= %s AND start_time < %s
            GROUP BY
                driver_id
            ORDER BY
                total_viagens DESC;


            """
            # Executar a consulta
            cursor.execute(query, [start_date_tab, end_date_tab])
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
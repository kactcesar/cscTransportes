"use strict";

$.fn.dataTable.Api.register('column().title()', function() {
    return $(this.header())[0].dataset.field;
}); 

const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.addEventListener('mouseenter', Swal.stopTimer)
        toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
});



var tab_csc_trans = function() {
    var kt_csc_trans = function() {
        
        var table = $('#kt_csc_trans');
        // begin first table
        table.on('processing.dt', function (e, settings, processing) {
            if (processing) {
                Toast.fire({
                    icon: 'primary',
                    title: 'Sucesso! Carregando os dados ...'
                });
            } else {
                Toast.close();
            }
        }).DataTable({
            responsive: true,
            processing: true,
            pageLength: 10,
            paging: false,
            language: {
                processing:     "Processamento em andamento...",
                search:         "Pesquisar:",
                lengthMenu:     "MENU registros por página",
                info:           "Mostrando de START até END de TOTAL registros",
                infoEmpty:      "Mostrando 0 até 0 de 0 registros",
                infoFiltered:   "(Filtrados de MAX registros)",
                infoPostFix:    "",
                loadingRecords: "Carregando registros...",
                zeroRecords:    "Nenhum registro encontrado",
                emptyTable:     "Nenhum registro encontrado",
                paginate: {
                    first:      "Primeiro",
                    previous:   "Anterior",
                    next:       "Avançar",
                    last:       "Último"
                },
                aria: {
                    sortAscending:  ": Ordenar coluna por ordem crescente",
                    sortDescending: ": Ordenar coluna por ordem decrescente"
                }
            },
            ajax: {
                url: '/viagens/dados_viagem_lista/',
                type: 'POST',
                dataSrc: 'dados',
                data: function(d) {
                    d.csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
                },
            },
            order: [[ 0, 'asc' ]],
            columns: [
                {data: 'id_motorista'},               
                {data: 'total_viagens'},    
                {data: 'tempo_total_viagem'},         
                {data: 'combustível_usado'},  
                {data: 'total_excessos_velocidade'},  
            ],            
            columnDefs: [               
            ],
        });  
    };

    return {
        //main function to initiate the module
        init: function() {
            kt_csc_trans();
        },
    };
}();



jQuery(document).ready(function() {
    tab_csc_trans.init()

    $('button[type="submit"]').on('click', function(event) {
        event.preventDefault();  // Prevenir o comportamento padrão do botão de submit

        // Pegar os valores das datas
        let startDate = $('#start_date').val();
        let endDate = $('#end_date').val();

        // Validar se as datas foram preenchidas
        if (!startDate || !endDate) {
            alert("Por favor, preencha as duas datas.");
            return;
        }

        $.ajax({
            url: '/viagens/grafico_viagem_lista/',  // URL para o seu backend
            method: 'GET',
            data: {
                start_date: startDate,
                end_date: endDate
            },
            success: function(response) {
                // Apenas logar a resposta por enquanto
                KTApexChartsDemo.init();
                console.log(response);
            },
            error: function(error) {
                console.error('Erro:', error);
            }
        });
    });

    
});

var KTApexChartsDemo = function () {
    var chart; // Armazenará a instância do gráfico

    var grafico = function () {
        const apexChart = "#chart_2";

        // Realizar a requisição AJAX para obter os dados da URL
        fetch('/viagens/obter_dados_grafico/')
            .then(response => response.json())
            .then(data => {
                // Verificar se há erro nos dados
                if (data.error) {
                    console.error(data.error);
                    return;
                }

                // Verificar se não há dados
                if (!data.dados || data.dados.length === 0) {
                    Swal.fire({
                        icon: 'info',
                        title: 'Sem Dados',
                        text: 'Não há dados disponíveis para exibir no gráfico.',
                        confirmButtonText: 'OK'
                    });
                    // Opcional: limpar o gráfico se necessário
                    document.querySelector(apexChart).innerHTML = ''; 
                    return;
                }

                console.log('Dados recebidos:', data);
                // Preparar os dados do gráfico
                var seriesData = [];
                var labelsData = [];

                // Preencher as séries e labels com base nos dados retornados
                data.dados.forEach(item => {
                    labelsData.push(item.categoria); // A categoria do motorista
                    seriesData.push(item.quantidade_motoristas); // A quantidade de motoristas por categoria
                });

                // Configurar as opções do gráfico com os dados retornados
                var options = {
                    series: seriesData,  // Dados recebidos
                    chart: {
                        width: 580,
                        type: 'pie',  // Tipo de gráfico, modifique conforme necessário
                    },
                    labels: labelsData,  
                    responsive: [{
                        breakpoint: 480,
                        options: {
                            chart: {
                                width: 300
                            },
                            legend: {
                                position: 'bottom'
                            }
                        }
                    }],
                    colors: ['#008FFB', '#00E396', '#FEB019', '#FF4560', '#775DD0']
                };

                // Renderizar o gráfico
                if (chart) {
                    chart.updateOptions(options);
                } else {
                    chart = new ApexCharts(document.querySelector(apexChart), options);
                    chart.render();
                }
            })
            .catch(error => {
                console.error('Erro ao carregar dados:', error);
            });
    }

    // Função para atualizar a série de dados do gráfico
    var updateSeries = function(newData) {
        if (chart) {
            // Atualizar a série do gráfico com novos dados
            chart.updateSeries([{
                data: newData.seriesData
            }], false); // O segundo parâmetro `false` evita a animação
            chart.updateOptions({
                labels: newData.labelsData
            });
        } else {
            console.error('O gráfico ainda não foi inicializado.');
        }
    }

    return {
        // Funções públicas
        init: function () {
            grafico();
        },
        updateSeries: updateSeries // Exportar a função para atualização
    };
}();

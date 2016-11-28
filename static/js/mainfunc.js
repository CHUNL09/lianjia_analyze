/**
 * Created by liuchun on 2016/11/27.
 */
$(function () {
            function formatDate(timestamp_v) {
                  var now = new Date(parseFloat(timestamp_v)*1000);
                  var   year=now.getFullYear();
                  var   month=now.getMonth()+1;
                  var   date=now.getDate();
                  var   hour=now.getHours();
                  var   minute=now.getMinutes();
                  var   second=now.getSeconds();
                  return   year+"-"+month+"-"+date+"   "+hour+":"+minute+":"+second;

            };


            var category_source = {{ cata_list }};
            var data_source = {{ data_list }};
            var category_processed = new Array();
            for(var i=0; i<category_source.length;i++){
                category_processed[i]= formatDate(category_source[i]);
            };

            $('#sh_total_dealed_graph').highcharts({
                title: {
                    text: '上海房屋成交总量',
                    x: -20 //center
                },
                subtitle: {
                    text: 'Source: lianjia.com',
                    x: -20
                },
                xAxis: {
                      categories: category_processed
                },
                yAxis: {
                    title: {
                        text: '成交量 '
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    valueSuffix: '套'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: [{
                    name: '上海二手房成交总量',
                    data: data_source
                }]

            });

            var all_date_source = {{ all_date_list }};
            var all_data_source = {{ all_data_list }};
            var all_date_list_processed = new Array();
            for(var i=0; i<all_date_source.length;i++){
                all_date_list_processed[i]= formatDate(all_date_source[i]);
            };
            $('#avg_price_graph').highcharts({
                title: {
                    text: '二手房均价',
                    x: -20 //center
                },
                subtitle: {
                    text: 'Source: lianjia.com',
                    x: -20
                },
                xAxis: {
                      categories: all_date_list_processed
                },
                yAxis: {
                    title: {
                        text: '均价 '
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    valueSuffix: '元／平'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: [{
                    name: '城市挂牌均价',
                    data: all_data_source
                }]

            });

            var all_on_sale_list = {{ all_on_sale_list }};
            var all_on_sale_list_processed = new Array();
            for(var i=0; i<all_on_sale_list.length;i++){
                all_on_sale_list_processed[i] = new Array();
                all_on_sale_list_processed[i][0]= formatDate(all_on_sale_list[i][0]);
                all_on_sale_list_processed[i][1]= all_on_sale_list[i][1];
            };

            console.log(all_on_sale_list_processed);
            $('#on_sale_graph').highcharts({
                chart: {
                    type: 'column'
                },
                title: {
                    text: '在售房源'
                },
                subtitle: {
                    text: 'Source: lianjia.com'
                },
                xAxis: {
                    type: 'category',
                    labels: {
                        rotation: -45,
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                },
                yAxis: {
                    min: 0,
                    title: {
                        text: '二手房源 (套)'
                    }
                },
                legend: {
                    enabled: false
                },
                tooltip: {
                    pointFormat: '在售房源: <b>{point.y:.1f} 套</b>'
                },
                series: [{
                    name: 'on_sale_graph',
                    data: all_on_sale_list_processed,
                    dataLabels: {
                        enabled: true,
                        rotation: -90,
                        color: '#FFFFFF',
                        align: 'right',
                        format: '{point.y:.1f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }]
            });

            var all_sold_in_90_list = {{ all_sold_in_90_list }};

            $('#sold_in_90_graph').highcharts({
                title: {
                    text: '近90天成交量',
                    x: -20 //center
                },
                subtitle: {
                    text: 'Source: lianjia.com',
                    x: -20
                },
                xAxis: {
                      categories: all_date_list_processed
                },
                yAxis: {
                    title: {
                        text: '成交量 '
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    valueSuffix: '套'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: [{
                    name: '近90天成交量',
                    data: all_sold_in_90_list
                }]

            });

            var all_yesterday_check_num = {{ all_yesterday_check_num }};

            $('#sold_in_90_graph').highcharts({
                title: {
                    text: '昨日带看(次)',
                    x: -20 //center
                },
                subtitle: {
                    text: 'Source: lianjia.com',
                    x: -20
                },
                xAxis: {
                      categories: all_date_list_processed
                },
                yAxis: {
                    title: {
                        text: '带看次数 '
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },
                tooltip: {
                    valueSuffix: '次'
                },
                legend: {
                    layout: 'vertical',
                    align: 'right',
                    verticalAlign: 'middle',
                    borderWidth: 0
                },
                series: [{
                    name: '昨日带看',
                    data: all_yesterday_check_num
                }]

            });

        });

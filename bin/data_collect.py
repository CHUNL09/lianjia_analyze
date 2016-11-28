import re
from bs4 import BeautifulSoup
import datetime
import time
from tornado import httpclient,gen,ioloop,httpserver
from tornado import web

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings
from database_init import Online_Data,SH_Total_city_dealed,SH_Area
from tornado.options import define,options

define("port",default=8888,type=int)


@gen.coroutine
def obtain_page_data(target_url):
    response = yield httpclient.AsyncHTTPClient().fetch(target_url)
    data = response.body.decode('utf8')
    print("start %s %s" %(target_url,time.time()))

    raise gen.Return(data)

@gen.coroutine
def get_total_dealed_house(target_url):
    # 获取总的房屋成交量
    page_data = yield obtain_page_data(target_url)
    soup_obj = BeautifulSoup(page_data,"html.parser")
    dealed_house = soup_obj.html.body.find('div', {'class': 'list-head'}).text
    dealed_house_num = re.findall(r'\d+', dealed_house)[0]

    raise gen.Return(int(dealed_house_num))

@gen.coroutine
def get_online_data(target_url):
    # 获取 城市挂牌均价，正在出售数量，90天内交易量，昨日看房次数
    page_data = yield obtain_page_data(target_url)
    soup_obj = BeautifulSoup(page_data, "html.parser")
    online_data_str = soup_obj.html.body.find('div', {'class': 'secondcon'}).text
    online_data = online_data_str.replace('\n', '')
    avg_price, on_sale, _, sold_in_90, yesterday_check_num = re.findall(r'\d+', online_data)

    raise gen.Return({'avg_price':avg_price,'on_sale':on_sale,'sold_in_90':sold_in_90,'yesterday_check_num':yesterday_check_num})

@gen.coroutine
def shanghai_data_process():
    '''
    获取上海各个区的数据
    :return:
    '''
    start_time = time.time()
    chenjiao_page = "http://sh.lianjia.com/chengjiao/"
    ershoufang_page = "http://sh.lianjia.com/ershoufang/"
    dealed_house_num = yield get_total_dealed_house(chenjiao_page)
    sh_online_data = {}
    for key,value in settings.sh_area_dict.items():
        sh_online_data[key] = yield get_online_data(ershoufang_page+settings.sh_area_dict[key])
    print("dealed_house_num %s" %dealed_house_num)
    for key,value in sh_online_data.items():
        print(key,value)

    print("tornado time cost: %s" %(time.time()-start_time) )

    #settings.session
    update_date = datetime.datetime.now()
    dealed_house_num_obj = SH_Total_city_dealed(dealed_house_num=dealed_house_num,
                                                date = update_date)
    settings.session.add(dealed_house_num_obj)

    for key,value in sh_online_data.items():
        area_obj = settings.session.query(SH_Area).filter_by(name=key).first()
        online_data_obj = Online_Data(sold_in_90 = value['sold_in_90'],
                                      avg_price = value['avg_price'],
                                      yesterday_check_num = value['yesterday_check_num'],
                                      on_sale = value['on_sale'],
                                      date = update_date,
                                      belong_area = area_obj.id)
        settings.session.add(online_data_obj)
    settings.session.commit()

class IndexHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        total_dealed_house_num = settings.session.query(SH_Total_city_dealed).all()
        cata_list = []
        data_list = []
        for item in total_dealed_house_num:
            cata_list.append(time.mktime(item.date.timetuple()))
            data_list.append(item.dealed_house_num)

        area_id = settings.session.query(SH_Area).filter_by(name='all').first()
        area_avg_price = settings.session.query(Online_Data).filter_by(belong_area = area_id.id).all()
        area_date_list = []
        area_data_list = []
        area_on_sale_list = []
        area_sold_in_90_list = []
        area_yesterday_check_num = []
        for item in area_avg_price:
            area_date_list.append(time.mktime(item.date.timetuple()))
            area_data_list.append(item.avg_price)
            area_on_sale_list.append([time.mktime(item.date.timetuple()),item.on_sale])
            area_sold_in_90_list.append(item.sold_in_90)
            area_yesterday_check_num.append(item.yesterday_check_num)
        self.render("index.html",cata_list=cata_list,
                    data_list=data_list,area_date_list = area_date_list,area_data_list = area_data_list,
                    area_on_sale_list = area_on_sale_list,area_sold_in_90_list=area_sold_in_90_list,
                    area_yesterday_check_num = area_yesterday_check_num,city="sh",area="all")

class QueryHandler(web.RequestHandler):
    def get(self,city,area):

        if city == "sh":
            total_dealed_house_num = settings.session.query(SH_Total_city_dealed).all()

            cata_list = []
            data_list = []
            for item in total_dealed_house_num:
                cata_list.append(time.mktime(item.date.timetuple()))
                data_list.append(item.dealed_house_num)

            area_id = settings.session.query(SH_Area).filter_by(name=area).first()
            area_avg_price = settings.session.query(Online_Data).filter_by(belong_area=area_id.id).all()
            area_date_list = []
            area_data_list = []
            area_on_sale_list = []
            area_sold_in_90_list = []
            area_yesterday_check_num = []
            for item in area_avg_price:
                area_date_list.append(time.mktime(item.date.timetuple()))
                area_data_list.append(item.avg_price)
                area_on_sale_list.append([time.mktime(item.date.timetuple()), item.on_sale])
                area_sold_in_90_list.append(item.sold_in_90)
                area_yesterday_check_num.append(item.yesterday_check_num)

            self.render("index.html", cata_list=cata_list,
                        data_list=data_list, area_date_list=area_date_list, area_data_list=area_data_list,
                        area_on_sale_list=area_on_sale_list, area_sold_in_90_list=area_sold_in_90_list,
                        area_yesterday_check_num=area_yesterday_check_num,city=city,area=area)
        else:
            self.redirect("/")




class MyApplication(web.Application):
    def __init__(self):
        handlers = [
            (r'/',IndexHandler),
            (r'/view/(\w+)/(\w+)',QueryHandler),

        ]

        settings = {
            'static_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),
            'template_path': os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
        }

        super(MyApplication,self).__init__(handlers,**settings)


if __name__=='__main__':
    http_server = httpserver.HTTPServer(MyApplication())
    http_server.listen(options.port)
    ioloop.PeriodicCallback(shanghai_data_process,86400000).start() #毫秒 86400000，每天定时跑
    ioloop.IOLoop.instance().start()


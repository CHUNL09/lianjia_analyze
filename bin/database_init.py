from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime


import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from conf import settings

Base = declarative_base()
db_session = scoped_session(sessionmaker(bind=settings.engine))


class SH_Area(Base):
    __tablename__ = 'sh_area'  # 表名
    id = Column(Integer, primary_key=True)
    name = Column(String(64))

class Online_Data(Base):
    __tablename__ = 'online_data'  # 表名
    id = Column(Integer, primary_key=True)
    sold_in_90 = Column(Integer)
    avg_price = Column(Integer)
    yesterday_check_num = Column(Integer)
    on_sale = Column(Integer)
    date = Column(DateTime)
    belong_area = Column(Integer,ForeignKey('sh_area.id'))

class SH_Total_city_dealed(Base):
    __tablename__ = 'sh_total_city_dealed'  # 表名
    id = Column(Integer, primary_key=True)
    dealed_house_num = Column(Integer)
    date = Column(DateTime)
    memo = Column(String(64),nullable=True)

def db_init():
    Base.metadata.create_all(settings.engine)  # 创建表结构
    for district in settings.sh_area_dict.keys():
        item_obj = SH_Area(name = district)
        db_session.add(item_obj)
    db_session.commit()
    db_session.remove()


if __name__ == '__main__':
    db_init()
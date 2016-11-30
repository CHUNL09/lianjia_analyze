import os
from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker,scoped_session
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB={
    'connector':'mysql+pymysql://root:aircool123@127.0.0.1:3306/devdb1',
    'max_session':5
}

engine = create_engine(DB['connector'], max_overflow= DB['max_session'], echo= False)
# SessionCls = sessionmaker(bind=engine)
# session = SessionCls()
#db_session = scoped_session(sessionmaker(bind=engine))


sh_area_dict = {
        "all":"",
        "pudongxinqu": "pudongxinqu/",
        "minhang": "minhang/",
        "baoshan": "baoshan/",
        "xuhui": "xuhui/",
        "putuo": "putuo/",
        "yangpu": "yangpu/",
        "changning": "changning/",
        "songjiang": "songjiang/",
        "jiading": "jiading/",
        "huangpu": "huangpu/",
        "jingan": "jingan/",
        "zhabei": "zhabei/",
        "hongkou": "hongkou/",
        "qingpu": "qingpu/",
        "fengxian": "fengxian/",
        "jinshan": "jinshan/",
        "chongming": "chongming/",
        "shanghaizhoubian": "shanghaizhoubian/",
    }
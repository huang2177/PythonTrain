# 导入:
from sqlalchemy import Column, String, create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(String(5), primary_key=True)
    name = Column(String(15))
    age = Column(String(5))
    school = Column(String(20))
    city = Column(String(20))
    sex = Column(String(2))
    height = Column(String(5))


def query():
    users = DBsession.query(User).all()
    for user in users:
        print(user.__dict__)


def update():
    query = DBsession.query(User)
    user = query.get('11')
    user.name = 'huangH'
    DBsession.flush()
    print(user.name)


engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/huang')
DBsession = sessionmaker(bind=engine)()

update()

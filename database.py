from sqlalchemy import create_engine, Column, String, Integer, Date, insert, BIGINT, DateTime, ForeignKey, types
from sqlalchemy_utils import ChoiceType, Timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from constants import *
import datetime
from dateutil.relativedelta import relativedelta

engine = create_engine(DATA_BASE, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Bus_Travel(Base):
    __tablename__ = 'bus_travel'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    number = Column(BIGINT)
    origin = Column(String(50))
    destination = Column(String(50))
    date = Column(Date())
    passenger = Column(Integer)
    user_chat_id = Column(Integer)


Base.metadata.create_all(engine)


class BusDistributor(Base):
    __tablename__ = 'bus_distributor'

    id = Column(Integer, primary_key=True)
    distributor_name = Column(String(50))
    distributor_number = Column(BIGINT)
    distributor_origin = Column(String(50))
    distributor_destination = Column(String(50))
    distributor_travel_dates = Column(Date())
    passenger_capacity = Column(Integer)
    distributor_chat_id = Column(Integer)


Base.metadata.create_all(engine)


class Token(Base, Timestamp):
    __tablename__ = 'admin_token'

    id = Column(Integer, primary_key=True)
    number_of_months = Column(Integer)
    token = Column(String(30))
    status = Column(ChoiceType(TOKEN_STATUS), default='Active')


Base.metadata.create_all(engine)


def after_month(context):
    start_date = context.get_current_parameters()['start_date']
    token = context.get_current_parameters()['token']
    token_obj = session.query(Token).filter(Token.id == token).first()
    end_date = start_date + relativedelta(months=+token_obj.number_of_months)
    return end_date


class Subscription(Base, Timestamp):
    __tablename__ = 'agency_subscription'

    id = Column(Integer, primary_key=True)
    token = Column(Integer, ForeignKey('admin_token.id'))
    agency_chat_id = Column(Integer)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, default=after_month)
    status = Column(ChoiceType(TOKEN_STATUS), default='Active')


Base.metadata.create_all(engine)


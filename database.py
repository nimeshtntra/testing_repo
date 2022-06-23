from sqlalchemy import create_engine, Column, String, Integer, Date, insert, BIGINT, DateTime, ForeignKey, types
from sqlalchemy_utils import ChoiceType, Timestamp
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from constants import *

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
    __tablename__ = 'agency_token'

    id = Column(Integer, primary_key=True)
    token = Column(String(10))
    status = Column(ChoiceType(TOKEN_STATUS), default='is_active')


Base.metadata.create_all(engine)


class Subscription(Base, Timestamp):
    __tablename__ = 'agency_subscription'

    id = Column(Integer, primary_key=True)
    agency_id = Column(Integer, ForeignKey("bus_distributor.id"))
    token = Column(Integer, ForeignKey("agency_token.id"))
    start_date = Column(Date())
    end_date = Column(Date())
    status = Column(ChoiceType(TOKEN_STATUS), default='is_active')


Base.metadata.create_all(engine)


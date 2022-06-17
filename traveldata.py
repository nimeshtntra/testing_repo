from sqlalchemy import create_engine, Column, String, Integer, Date, insert, BIGINT
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import requests
from constants import *

engine = create_engine(DATABASE, echo=True)
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


class UserInsertDb:
    def travel_data(self, name, number, origin, destination, dates, passenger, chat_id):
        data = Bus_Travel(name=name, number=number, origin=origin, destination=destination, date=dates, passenger=passenger, user_chat_id=chat_id)
        session.add(data)
        session.commit()


class DistributorInsertDb:
    def distributor_data(self, distributor_name, distributor_number, distributor_origin, distributor_destination, distributor_travel_dates, passenger_capacity, chat_id):
        data = BusDistributor(distributor_name=distributor_name, distributor_number=distributor_number, distributor_origin=distributor_origin, distributor_destination=distributor_destination, distributor_travel_dates=distributor_travel_dates, passenger_capacity=passenger_capacity, distributor_chat_id=chat_id)
        session.add(data)
        session.commit()


class DistributorFilterData:
    def distributor_filter(self, origin, destination, dates):
        result = session.query(BusDistributor).filter(BusDistributor.distributor_origin==origin, BusDistributor.distributor_destination==destination, BusDistributor.distributor_travel_dates==dates).first()
        return result


class UserFilterData:

    def user_filter(self, origin, destination, dates):
        result = session.query(Bus_Travel).filter(Bus_Travel.origin == origin, Bus_Travel.destination == destination, Bus_Travel.date == dates)
        return result


class UserPrivetMessage:
    def send_msg(self, seat, chat_id):
        url_req = "https://api.telegram.org/bot" + str(TOKEN) + "/sendMessage" + "?chat_id=" + str(chat_id) + "&text=" + seat
        requests.get(url_req)

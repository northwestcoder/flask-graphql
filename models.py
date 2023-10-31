import psycopg2
from sqlalchemy import *
from sqlalchemy.orm import (scoped_session, sessionmaker, relationship,
                            backref)

from sqlalchemy.ext.declarative import declarative_base


# EDIT THESE

USERNAME = "USER"
PASS = "PASS"
HOST = "HOST_OR_IP"
DBNAME = "DBNAME"

#######################################################
    
#this engine points at a demo db which is exposed, and only contains fake data
connection_string = 'postgresql+psycopg2://' + USERNAME + ':' + PASS + '@' + HOST + '/' + DBNAME
engine = create_engine(connection_string)

#this engine would create a local sqlite db on the flask/python machine, in the current working dir
#engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = db_session.query_property()


# below, 'graphql_people' and 'graphql_transactions' are actual table names in our postgres db
# a lack of a specified schema assumes 'public' schema

class People(Base):
    __tablename__ = 'graphql_people'
    customer_id = Column(String, primary_key=True)
    gender = Column(String)
    name_prefix = Column(String)
    name_first = Column(String)
    name_last = Column(String)
    email = Column(String)
    employment = Column(String)
    address = Column(String)
    city = Column(String)
    county = Column(String)
    state = Column(String)
    postal_code = Column(String)
    birth_dt = Column(Date)
    is_deleted = Column(Integer)
    job_type = Column(String)
    account_type = Column(String)
    phone_number = Column(String)
    ssn = Column(String)
    allergies = Column(String)
    blood_type = Column(String)
    last_ipaddress = Column(String)



class Transactions(Base):
    __tablename__ = 'graphql_transactions'
    trans_customer_id = Column(String, ForeignKey('graphql_people.customer_id'))
    people = relationship(
        People,
        backref=backref(
            'graphql_people',
            uselist=True,
            cascade='delete,all'))
    orderid = Column(String, primary_key=True)
    purchasedatetime = Column(String)
    transactiontotal = Column(Numeric)
    numberofitems = Column(Integer)
    productcode = Column(String)
    productcategory = Column(String)
    cc_number = Column(String)
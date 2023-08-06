#!/usr/bin/env python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def getConn():
    engin = create_engine("mysql+pymysql://root:roottest@127.0.0.1:1306/appdb")
    conn = sessionmaker(bind=engin)
    return conn()

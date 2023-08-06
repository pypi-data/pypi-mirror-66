#!/usr/bin/env python3
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__name__))))

from pyorm.dbs import mysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)
    name = Column(String(20))

    @staticmethod
    def addUser(id, name):
        conn = mysql.getConn()
        user = User(id=id, name=name)
        conn.add(user)
        conn.commit()
        conn.close()

    def getUser(id):
        conn = mysql.getConn()
        user = conn.query(User).filter(User.id == id).one()
        return user


if __name__ == "__main__":
    # User.addUser(1, "王二")
    print(User.getUser(1).name)

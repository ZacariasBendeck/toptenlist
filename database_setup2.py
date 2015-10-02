# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27

@author: Z
"""

####### CONFIGURATION CODE #############
import sys
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    email = Column(String(80))
    picture = Column(String(1000))
    page_profile = Column(String(25))


### CLASS Code ###
class  Owner(Base):
    ### TABLE INFORMATION ###
    __tablename__ = 'owner'

    ### MAPPERS ###
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    pic_url = Column(String(1000))
    slogan = Column(String(250))
    id =  Column(Integer, primary_key = True)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User

    @property
    def serialize(self):
        return {
        'name' : self.name,
        'description' : self.description,
        'pic_url': self.pic_url,
        'id': self.id,
        'user_id' : self.user_id
        }

### CLASS Code ###
class  Lists(Base):
    ### TABLE INFORMATION ###
    __tablename__ = 'lists'

    ### MAPPERS ###
    name = Column(String(80), nullable = False)
    description = Column(String(250))
    list_type = Column(String(250))
    id =  Column(Integer, primary_key = True)
    pic_url = Column(String(250))

    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship(Owner)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User

    @property
    def serialize(self):
        return {
        'name' : self.name,
        'description' : self.description,
        'list_type' : self.list_type,
        'pic_url': self.pic_url,
        'id': self.id,
        'owner_id' : self.owner_id,
        'user_id' : self.user_id
        }


### CLASS CODE ##
class Items(Base):  ### classes in camelcase
    ### TABLE INFORMATION
    __tablename__ = 'items'  ## table names in lowercase

    ###  MAPPER CODE
    name = Column(String(90), nullable = False)
    id = Column(Integer, primary_key = True)
    url = Column(String(250))
    description = Column(String(250))
    rank = Column(Integer)
    pic_url = Column(String(250))
    second_pic_url = Column(String(250))
    essay = Column(String(10000))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User

    lists_id = Column(Integer, ForeignKey('lists.id'))
    lists = relationship(Lists)


    @property
    def serialize(self):
        return {
        'name' : self.name,
        'description' : self.description,
        'id' : self.id,
        'pic_ url': self.pic_url,
        'url' : self.url,
        'rank': self.rank,
        'lists_id': self.lists_id,
        'essay': self.essay,
        'rank' : self.rank,
        'user_id' : self.user_id
        }

########insert at the end of the file  ###############
#####
engine = create_engine('sqlite:///finalProject.db')

Base.metadata.create_all(engine)

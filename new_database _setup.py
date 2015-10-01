# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27

@author: Z
"""

####### CONFIGURATION CODE #############
import sys, psycopg2
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()



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

    @property
    def serialize(self):
        return {
        'name' : self.name,
        'description' : self.description,
        'pic_url': self.pic_url,
        'id': self.id
        }

### CLASS Code ###
class  Lists(Base):
    ### TABLE INFORMATION ###
    __tablename__ = 'lists'

    ### MAPPERS ###
    name = Column(String(80), nullable = False)
    id =  Column(Integer, primary_key = True)
    description = Column(String(250))
    list_type = Column(String(250))
    pic_url = Column(String(250))
    date_created = Column(String(25))
    date_last_modified = Column(String(25))

    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship(Owner)

    @property
    def serialize(self):
        return {
        'name' : self.name,
        'description' : self.description,
        'list_type' : self.list_type,
        'pic_url': self.pic_url,
        'id': self.id,
        'owner_id' : self.owner_id,
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
        'rank' : self.rank
        }

########insert at the end of the file  ###############
#####
engine = create_engine('psycopg2:///finalProject.db')

Base.metadata.create_all(engine)
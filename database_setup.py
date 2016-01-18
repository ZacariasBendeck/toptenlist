import sys
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
    created = Column(String(100))
    updated = Column(String(100))
    email = Column(String(250), nullable = False)
    id =  Column(Integer, primary_key = True)

    @property
    def serialize(self):
        return {
        'name' : self.name,
        'description' : self.description,
        'pic_url': self.pic_url,
        'id': self.id,
        "created" : self.created,
        "updated" : self.updated,
        'slogan' : self.slogan,
        'email' : self.email
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
    published = Column(String(100))
    updated = Column(String(100))
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
        "published" : self.published,
        "updated" : self.updated
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
    published = Column(String(100))
    updated = Column(String(100))

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
        "published" : self.published,
        "updated" : self.updated
        }

########insert at the end of the file  ###############
#####
engine = create_engine('sqlite:///finalProject.db')

Base.metadata.create_all(engine)

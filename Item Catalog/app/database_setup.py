import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()

class Category(Base):

    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(80),nullable=False)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id,
        }


class Item(Base):
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    cateory = relationship(Category)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category_id': self.category_id
        }

# DIALCT = "mysql"
# DRIVER = "pymysql"
# USERNAME = "root"
# PASSWORD = ""
# HOST = "127.0.0.1"
# PORT = "3306"
# DATABASE = "item_catalog"
# DB_URI="{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
# engine = create_engine(DB_URI)
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
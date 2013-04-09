from datetime import datetime
from sqlalchemy import (create_engine,Table,ForeignKey,
                        Column,Integer,String,Text,DateTime)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relation,backref
#from .app import config

engine = create_engine('mysql://root:@localhost/mytokiolife')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

content_categories = Table("content_categories",Base.metadata,
                           Column("content_id",Integer,ForeignKey("contents.id")),
                           Column("category_id",Integer,ForeignKey("categories.id")))

class Content(Base):
    __tablename__ = 'contents'
    id = Column(Integer,primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    categories = relation("Category",
                          secondary=content_categories,
                          backref="contents")
    create_at = Column(DateTime)

    def __init__(self,title,content,categories=None):
        self.title = title
        self.content = content
        self.categories = [Category(name) for name in categories] 
        self.create_at = datetime.now()

    def __repr__(self):
        return '<Content {}{}>'.format(self.id,self.title)

    @classmethod
    def create(cls,title,content,categories):
        content = cls(title,content,categories)
        session.add(content)
        session.commit()

    @classmethod    
    def get_by_id(cls,id):
        return session.query(cls).get(id)

    @classmethod
    def get_popular(cls):
        pass

    @classmethod
    def get_newest(cls):
        return session.query(cls).order_by(cls.create_at.desc())[0:5]

    def get_relevant(self,num=5):
        pass

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer,primary_key=True)
    name = Column(String(50),nullable=False,unique=True)
    
    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return "<Category {}>".format(self.name)

def init_db():
    print type(Base)
    Base.metadata.create_all(bind=engine)
    


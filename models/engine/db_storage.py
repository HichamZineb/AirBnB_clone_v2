#!/usr/bin/python3
""" New engine DBStorage """

from os import getenv
from models.base_model import BaseModel
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship


class DBStorage:
    """ class DBStorage """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize DBStorage """
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Query on the current database session """
        if cls is None:
            objects = self.__session.query(State).all()
            objects.extend(self.__session.query(City).all())
            objects.extend(self.__session.query(User).all())
            objects.extend(self.__session.query(Place).all())
            objects.extend(self.__session.query(Review).all())
            objects.extend(self.__session.query(Amenity).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            objects = self.__session.query(cls)
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objects}

    def new(self, obj):
        """ Add object """
        self.__session.add(obj)

    def save(self):
        """ Save changes """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete object """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Reloads storage """
        Base.metadata.create_all(self.__engine)
        SessionFactory = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """ Closes the session """
        self.__session.close()

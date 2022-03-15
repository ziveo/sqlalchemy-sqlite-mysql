from sqlalchemy import Column, String, Integer, create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=200))
    age = Column(Integer)


# SQLite
url = "sqlite:///class.db"

# MySQL - PyMySQL
# url = "mysql+pymysql://root:root@localhost/sql_alchemy_test"

engine = create_engine(url)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

try:
    session = scoped_session(Session)
    users = [
        User(name="Joe 11", age=45),
        User(name="Joe 12", age=55),
        User(name="Joe 13", age=65),
    ]
    session.add_all(users)
    session.commit()
    print("Records committed")
except SQLAlchemyError as e:
    session.rollback()
finally:
    session.close()

from sqlalchemy import Column, String, Integer, create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


url = "sqlite:///class_hooks.db"
engine = create_engine(url)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


@event.listens_for(User, "before_insert")
def before_insert(mapper, connection, user):
    print(f"before insert: {user.name}")


@event.listens_for(User, "after_insert")
def after_insert(mapper, connection, user):
    print(f"after insert: {user.name}")


try:
    session = scoped_session(Session)
    users = []
    users.append(User(name="Joe 11", age=45))
    users.append(User(name="Joe 12", age=55))
    users.append(User(name="Joe 13", age=65))
    # user1 = User(name="Joe 1", age=45)
    # user2 = User(name="Joe 2", age=55)
    # user3 = User(name="Joe 3", age=65)
    # users = [user1, user2, user3]
    # session.add(user)
    session.add_all(users)
    session.commit()
except SQLAlchemyError as e:
    session.rollback()
finally:
    session.close()

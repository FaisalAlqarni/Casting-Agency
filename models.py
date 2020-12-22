# ==========================================
# IMPORTS
# ==========================================
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from datetime import datetime
import json
from flask_migrate import Migrate


# ==========================================
# CONFIGS
# ==========================================
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = 'postgres://jwwsigkdbkpuzf:67217f9ad3ba2ccc05c9b584505a7c938788451a7a5b1117049218ab8ffadc6b@ec2-52-5-176-53.compute-1.amazonaws.com:5432/ddsehqr6jp4nui'

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    migrate = Migrate(app, db)
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.create_all()
    db_seeding()


'''
db_seeding()
    inserts a dummy data into a database
'''


def db_seeding():
    movie1 = Movie(title="First Movie", release_date="10/10/2010")
    movie2 = Movie(title="Second Movie", release_date="1/12/2015")
    movie3 = Movie(title="Final Movie", release_date="1/10/2018")
    actor1 = Actor(name="First", age=18, gender="male")
    actor2 = Actor(name="Second", age=25, gender="male")
    actor3 = Actor(name="Third", age=40, gender="male")
    actor4 = Actor(name="Thirds", age=13, gender="female")
    actor5 = Actor(name="wally", age=16, gender="femal")
    actor6 = Actor(name="jhon", age=20, gender="male")

    Helpers.insert(movie1)
    Helpers.insert(movie2)
    Helpers.insert(movie3)
    Helpers.insert(actor1)
    Helpers.insert(actor2)
    Helpers.insert(actor3)
    Helpers.insert(actor4)
    Helpers.insert(actor5)
    Helpers.insert(actor6)

    association1 = association.insert().values(
        movie_id=movie1.id, actor_id=actor1.id)
    association2 = association.insert().values(
        movie_id=movie1.id, actor_id=actor2.id)
    association3 = association.insert().values(
        movie_id=movie1.id, actor_id=actor3.id)
    association4 = association.insert().values(
        movie_id=movie1.id, actor_id=actor4.id)
    association5 = association.insert().values(
        movie_id=movie1.id, actor_id=actor5.id)
    association6 = association.insert().values(
        movie_id=movie1.id, actor_id=actor6.id)

    association7 = association.insert().values(
        movie_id=movie2.id, actor_id=actor1.id)
    association8 = association.insert().values(
        movie_id=movie2.id, actor_id=actor2.id)
    association9 = association.insert().values(
        movie_id=movie2.id, actor_id=actor3.id)

    association10 = association.insert().values(
        movie_id=movie3.id, actor_id=actor4.id)
    association11 = association.insert().values(
        movie_id=movie3.id, actor_id=actor5.id)
    association12 = association.insert().values(
        movie_id=movie3.id, actor_id=actor6.id)

    db.session.execute(association1)
    db.session.execute(association2)
    db.session.execute(association3)
    db.session.execute(association4)
    db.session.execute(association5)
    db.session.execute(association6)
    db.session.execute(association7)
    db.session.execute(association8)
    db.session.execute(association9)
    db.session.execute(association10)
    db.session.execute(association11)
    db.session.execute(association12)
    db.session.commit()

# ==========================================
# BASE
# ==========================================


class Base(db.Model):
    """Base model."""

    __abstract__ = True

    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    updated_on = db.Column(db.DateTime, default=datetime.utcnow)


# ==========================================
# HELPERS
# ==========================================
class Helpers():
    """helper methods."""
    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            Helpers.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a new model from database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Black Coffee'
            Helpers.update()
    '''

    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a new model from a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            Helpers.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# ==========================================
# MODELS
# ==========================================
'''
association
an association table, to apply many-to-many relationship
'''
association = db.Table('association',
                       Column('movie_id', Integer, db.ForeignKey('movies.id')),
                       Column('actor_id', Integer, db.ForeignKey('actors.id')),
                       # db.UniqueConstraint('movie_id', 'actor_id', name='UC_movie_id_actor_id')
                       )

'''
Movie
a persistent Movie entity, extends the base SQLAlchemy Model
'''


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    release_date = Column(String(180), nullable=False)
    actors = db.relationship('Actor',
                             secondary=association,
                             backref="movie",
                             lazy='dynamic',
                             cascade="all",
                             passive_deletes=True)

    def __init__(self, title,  release_date):
        self.title = title
        self.release_date = release_date

    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]
        }

    def __repr__(self):
        return json.dumps(self.short())


'''
Actor
a persistent Actor entity, extends the base SQLAlchemy Model
'''


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False)
    age = Column(Integer(), nullable=False)
    gender = Column(String(10), nullable=False)
    # movies = db.relationship('Movie',
    #                          secondary = association,
    #                          backref="actor",
    #                          cascade="all",
    #                          passive_deletes=True)

    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            # 'movies': [movie.title for movie in self.movies]
        }

    def __repr__(self):
        return json.dumps(self.short())

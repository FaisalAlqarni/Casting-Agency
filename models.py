# ==========================================
# IMPORTS
# ==========================================
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from datetime import datetime
import json 
import constants



# ==========================================
# CONFIGS
# ==========================================
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = 'postgres://postgres:1111@localhost:5432/agency'

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()



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
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            actor = Actor(...)
            actor = Actor(...)
            Helpers.assign_actors_to_movie([1,2],1)
    '''
    def assign_actors_to_movie(actor_ids, movie_id):
        actors = db.session.query(Actor).filter(Actor.id.in_(actor_ids)).all()
        movie = db.session.query(Movie).filter(Movie.id == movie_id).first()
        movie.actors = [actor for actor in actors]
        db.session.commit()
        
    def assign_movies_to_actor(movie_ids, actor_id):
        movies = db.session.query(Movie).filter(Movie.id.in_(movie_ids)).all()
        actors = db.session.query(Actor).filter(Actor.id == actor_id).first()
        actors.movies = [movie for movie in movies]
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
association_table
an association table, to apply many-to-many relationship
'''
association_table = db.Table('association', Base.metadata,
    Column('movies_id', Integer, db.ForeignKey('movies.id')),
    Column('actors_id', Integer, db.ForeignKey('actors.id'))
)

'''
Movie
a persistent Movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer(), primary_key=True)
    title = Column(String(), nullable=False)
    release_date =  Column(String(180), nullable=False)
    # actors = db.relationship('Actor', backref='movies', lazy=True)
    children = db.relationship('Actor', secondary = association_table, back_populates= 'movies')

    def __init__(self, title,  release_date):
        self.title = title
        self.release_date = release_date
        
    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': json.loads(self.actors)
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
    age =  Column(Integer(), nullable=False)
    gender =  Column(String(), nullable=False)
    # movie = db.Column(db.Integer, db.ForeignKey('movies.id'))
    movies = db.relationship('movies', secondary = association_table, back_populates= 'actors')
    
    def short(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'recipe': json.loads(self.movie)
        }

    def __repr__(self):
        return json.dumps(self.short())
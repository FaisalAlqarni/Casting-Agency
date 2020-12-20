# ==========================================
# IMPORTS
# ==========================================
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from flask.cli import with_appcontext
from models import db_drop_and_create_all, setup_db, Movie, Actor, Helpers, db
from auth import AuthError, requires_auth



# ==========================================
# CONFIGS
# ==========================================
app = Flask(__name__)
setup_db(app)
CORS(app)
db_drop_and_create_all()



# ==========================================
# ROUTES
# ==========================================
@app.route('/movies', methods=['GET'])
@requires_auth('get:movies')
def get_movies():
    movies = Movie.query.all()
    movies_short = [movie.short() for movie in movies]
    return jsonify({
        'success': True,
        'Movies': movies_short
    })

@app.route('/actors', methods=['GET'])
@requires_auth('get:actors')
def get_actors():
    actors = Actor.query.all()
    actors_short = [actor.short() for actor in actors]
    return jsonify({
        'success': True,
        'Actors': actors_short
    })

@app.route('/movies/<int:id>', methods=['GET'])
@requires_auth('get:movies')
def show_movie(id):
    movie = Movie.query.filter_by(id=id).first()
    if not movie:
        return abort(404)
    return jsonify({
        'success': True,
        'data': movie.short()
    }), 200
    
@app.route('/actors/<int:id>', methods=['GET'])
@requires_auth('get:actors')
def show_actor(id):
    actor = Actor.query.filter_by(id=id).first()
    if not actor:
        return abort(404)
    return jsonify({
        'success': True,
        'data': actor.short()
    }), 200

@app.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(id):
    try:
        movie = Movie.query.filter_by(id=id).first()
        if not movie:
            return abort(404)
        for ass in movie.actors:
            db.session.delete(ass)

        Helpers.delete(movie)
        return jsonify({
            'success': True,
            'deleted': movie.id,
        }), 200
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close() 
          
@app.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(id):
    try:
        actor = Actor.query.filter_by(id=id).first()
        if not actor:
            return abort(404)
        Helpers.delete(actor)
        return jsonify({
            'success': True,
            'deleted': actor.id,
        }), 200
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

@app.route('/actors', methods=['POST'])
@requires_auth('post:actors')
def add_actor():
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)
    
    if ((name is None) or (age is None) or (gender is None)):
        return abort(422)
    try:
        new_actor = Actor(name = name, age = age, gender = gender)
        Helpers.insert(new_actor)
        return jsonify({
            'success': True,
            'actor': new_actor.short()
        }), 201
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
    
@app.route('/movies', methods=['POST'])
@requires_auth('post:movies')
def add_movie():
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get("release_date", None)
    
    if ((title is None) or (release_date is None)):
        return abort(422)
    try:
        new_movie = Movie(title = title, release_date = release_date)
        Helpers.insert(new_movie)
        return jsonify({
            'success': True,
            'actor': new_movie.short()
        }), 201
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()

@app.route('/movies/<int:id>', methods=['PATCH'])
@requires_auth('patch:movies')
def update_movie(id):
    the_movie = Movie.query.filter(Movie.id == id).one_or_none()
    if the_movie is None:
        return abort(404)
    
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get("release_date", None)
    
    if ((title is None) and (release_date is None)):
        return abort(422)
    try:
        if title is not None:
            the_movie.title = title
        if release_date is not None:
            the_movie.release_date = release_date
        
        Helpers.update(the_movie)
        return jsonify({
            'success': True,
            'actor': the_movie.short()
        }), 201
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()
        
@app.route('/actors/<int:id>', methods=['PATCH'])
@requires_auth('patch:actors')
def update_actor(id):
    the_actor = Actor.query.filter(Actor.id == id).one_or_none()
    if the_actor is None:
        return abort(404)
    
    body = request.get_json()
    name = body.get('name', None)
    age = body.get("age", None)
    gender = body.get("gender", None)
    
    if ((name is None) and (age is None) and (gender is None)):
        return abort(422)
    try:
        if name is not None:
            the_actor.name = name
        if age is not None:
            the_actor.age = age
        if gender is not None:
            the_actor.gender = gender
        
        Helpers.update(the_actor)
        return jsonify({
            'success': True,
            'actor': the_actor.short()
        }), 201
    except:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()



# ==========================================
# Error Handling
# ==========================================
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "UNPROCESSABLE"
    }), 422

@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "RECORD NOT FOUND"
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "SERVER ERROR"
    }), 500

@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

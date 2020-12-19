# ==========================================
# IMPORTS
# ==========================================import os
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
# SEEDING
# ==========================================

# ==========================================
# ROUTES
# ==========================================
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movies_short = [movie.short() for movie in movies]
    return jsonify({
        'success': True,
        'Movies': movies_short
    })

@app.route('/actors', methods=['GET'])
def get_actors():
    actors = Actor.query.all()
    actors_short = [actor.short() for actor in actors]
    return jsonify({
        'success': True,
        'Actors': actors_short
    })


# @app.route('/movies/<int:id>', methods=['DELETE'])
# # @requires_auth('delete:movies')
# def delete_actor(payload, id):
#     movie = Movie.query.filter_by(id=id).first()
#     if not movie:
#         return jsonify({'message': 'Movie not found.'})
#     movie.delete()
#     return jsonify({
#         'message': movie.id + ' Deleted.',
#         'success': True,
#     }), 200

    
# @app.route('/actors/<int:id>', methods=['DELETE'])
# # @requires_auth('delete:actors')
# def delete_actor(payload, id):
#     actor = Actor.query.filter_by(id=id).first()
#     if not actor:
#         return jsonify({'message': 'Actor not found.'})
#     actor.delete()
#     return jsonify({
#         'message': actor.id + ' Deleted.',
#         'success': True,
#     }), 200


# @app.route('/movies', methods=['POST'])
# # @requires_auth('post:movies')
# def add_actor(payload):
#     body = request.get_json()
#     new_actor = Actor(
#         name=body.get('name'),
#         title=body.get('age'),
#     )
#     new_actor.save()
#     return jsonify({
#         'actor': new_actor.to_json(),
#         'success': True
#     }), 201
    
# @app.route('/actors', methods=['POST'])
# # @requires_auth('post:actors')
# def add_actor(payload):
#     """Handles POST requests for actors.
#     returns:
#         - actor object
#         - success message
#     """
#     body = request.get_json()
#     new_actor = Actor(
#         name=body.get('name'),
#         bio=body.get('bio'),
#         age=body.get('age'),
#         gender=body.get('gender'),
#         movie=body.get('movie')
#     )
#     new_actor.save()
#     return jsonify({
#         'actor': new_actor.to_json(),
#         'success': True
#     }), 201


# @app.route('/drinks', methods=['POST'])
# # @requires_auth('post:drinks')
# def create_drinks():
#     try:
#         request_json = request.get_json()
#         new_drink = Drink(title=request_json['title'], recipe=json.dumps(
#             [request_json['recipe']]))
#         new_drink.insert()
#         drink = [new_drink.long()]
#         return jsonify({
#             'success': True,
#             'drinks': drink
#         })
#     except Exception:
#         abort(500)



# @app.route('/drinks/<int:id>', methods=['PATCH'])
# @requires_auth('patch:drinks')
# def update_drink(id):
#     the_drink = Drink.query.filter(Drink.id == id).one_or_none()
#     if the_drink is None:
#         abort(404)
#     the_drink.update()
#     drink = [the_drink.long()]
#     return jsonify({
#         'success': True,
#         'drinks': drink
#     })


# '''
# @TODOx implement endpoint
#     DELETE /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should delete the corresponding row for <id>
#         it should require the 'delete:drinks' permission
#     returns status code 200 and json {"success": True, "delete": id}
#     where id is the id of the deleted record
#         or appropriate status code indicating reason for failure
# '''


# @app.route('/drinks/<int:id>', methods=['DELETE'])
# @requires_auth('delete:drinks')
# def delete_drink(id):
#     drink = Drink.query.filter(Drink.id == id).one_or_none()
#     if drink is None:
#         abort(404)
#     drink.delete()
#     return jsonify({
#         'success': True,
#         'delete': id
#     })

# ==========================================
# Error Handling
# ==========================================
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
        jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
            }), 404

'''

'''
@TODOx implement error handler for 404
    error handler should conform to general task above
'''


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


'''
@TODOx implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code

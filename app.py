# ==========================================
# IMPORTS
# ==========================================import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from flask.cli import with_appcontext
from models import db_drop_and_create_all, setup_db, Movie, Actor, Helpers
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
@with_appcontext
def seed():
    """Seed the database."""
    movie1 = Movie(title = "First Movie", release_date = "10/10/2010").save()
    movie2 = Movie(title = "Second Movie", release_date = "1/12/2015").save()
    movie3 = Movie(title = "Final Movie", release_date = "1/10/2018").save()
    actor1 = Actor(name = "First", age = 18, gender = "male").save()
    actor2 = Actor(name = "Second", age = 25, gender = "male").save()
    actor3 = Actor(name = "Third", age = 40, gender = "male").save()
    actor4 = Actor(name = "Thirds", age = 13, gender = "female").save()
    actor5 = Actor(name = "wally", age = 16, gender = "femal").save()
    actor6 = Actor(name = "jhon", age = 20, gender = "male").save()

def register_commands(app):
    """Register CLI commands."""
    app.cli.add_command(seed)
    
register_commands(app)

Helpers.assign_actors_to_movie([1,2,3,4,5,6], 1)
Helpers.assign_actors_to_movie([2], 2)
Helpers.assign_actors_to_movie([5,6], 3)
Helpers.assign_movies_to_actor([2], 1)
Helpers.assign_movies_to_actor([2, 3], 3)
Helpers.assign_movies_to_actor([3], 4)



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


# '''
# @TODOx implement endpoint
#     GET /drinks-detail
#         it should require the 'get:drinks-detail' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drinks}
#     where drinks is the list of drinks
#         or appropriate status code indicating reason for failure
# '''


# @app.route('/drinks-detail', methods=['GET'])
# @requires_auth('get:drinks-detail')
# def get_drinks_detail():
#     try:
#         all_drinks = Drink.query.all()
#         drinks = [drink.short() for drink in all_drinks]
#         return jsonify({
#             'success': True,
#             'drinks': drinks
#         })
#     except Exception:
#         abort(500)


# '''
# @TODOx implement endpoint
#     POST /drinks
#         it should create a new row in the drinks table
#         it should require the 'post:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink}
#     where drink an array containing only the newly created drink
#         or appropriate status code indicating reason for failure
# '''


# @app.route('/drinks', methods=['POST'])
# @requires_auth('post:drinks')
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


# '''
# @TODOx implement endpoint
#     PATCH /drinks/<id>
#         where <id> is the existing model id
#         it should respond with a 404 error if <id> is not found
#         it should update the corresponding row for <id>
#         it should require the 'patch:drinks' permission
#         it should contain the drink.long() data representation
#     returns status code 200 and json {"success": True, "drinks": drink}
#     where drink an array containing only the updated drink
#         or appropriate status code indicating reason for failure
# '''


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

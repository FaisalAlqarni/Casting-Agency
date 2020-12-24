import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, Helpers

assistant_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRSVWFGTkNVSFppaE9laGNJTDEyMiJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbC1hbHFhcm5pLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGU5ZjU2ZTAwYTgzMDA2ZTg4ZjhlOSIsImF1ZCI6ImFnaW5jeSIsImlhdCI6MTYwODc3NjU2OSwiZXhwIjoxNjA4NzgzNzY5LCJhenAiOiJXQUExTWJWMXRaWTdRZFZ1VTB3ejdzUFppaGlvYWxLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Om28GqX2TdeA9b2_MWT82AAo7kgmkh_1Baf5EX82INooB1WKlLwOjALA6-x4DTjxqsuQHhFMqyMCI9z2rznS5-0Kg7fSfhI4d5xQcFvbH7R6R2OOD-E1SlKhEOPhxe-s1EdsaSf9QVNojEhXFUpRVgvYt3pV1DmgzvU081M-wH1zlmD4GL0XZ4MDOCesCPy8Es5NA_ttqHeLD69mG838KrZ-uA4f-RXVXS-fyUxCQXsarwvu3jdkMJ6OrIlfMsVL2hX0c83-aDOXfiasjAKwEzrmVFpD9t8dAu8V5hwq6BP6qLXxZ0D4lcTP4g1YOEbZ2d13DvB8Xm-19XGsyx_1Gg"
}

director_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRSVWFGTkNVSFppaE9laGNJTDEyMiJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbC1hbHFhcm5pLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGU5ZmI3ZTAwYTgzMDA2ZTg4ZjhlYyIsImF1ZCI6ImFnaW5jeSIsImlhdCI6MTYwODc3NjY1OSwiZXhwIjoxNjA4NzgzODU5LCJhenAiOiJXQUExTWJWMXRaWTdRZFZ1VTB3ejdzUFppaGlvYWxLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.O1PpYxNIy5vree-ebWqsU8f__ReAv4CUFWK6IQ8oPB7u8h8DGlvwIfHB1lRpcMDfSIsU4iD5xMOX3fVWU8XivWPjf3Btw2CBkLKnLi5bGANTofCM57ODnMvZdu9llSu5qPr-Ljm0rMCuaEgbgFYP02ICct2fRwHGhqIyk2mu4NKjdF9PF8rnt4KdX7Hk-sFClE8j1Cj0EeYZWHCHxJ4FnlGU30bxkkYGi9gq8I2tcpJbUXwr1B6sWqKT309uQYsVq4U3AfM1AtWfo5RnSLLBJp8-juN2gEXnAyLZJux2cukWJyJ-rjYNDY0PyO2dMTUGgu-Q7gUnbz7sS4FWbGEg3w"
}

producer_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRSVWFGTkNVSFppaE9laGNJTDEyMiJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbC1hbHFhcm5pLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGVhMGQxNzgyMzhiMDA3MTk2NTU4MCIsImF1ZCI6ImFnaW5jeSIsImlhdCI6MTYwODc3NjUwOCwiZXhwIjoxNjA4NzgzNzA4LCJhenAiOiJXQUExTWJWMXRaWTdRZFZ1VTB3ejdzUFppaGlvYWxLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.qsC32zQF9HWudmh75v4h3RcgwJopc-t9tGrZbOw-RMYKruMt5pjfEZQuDrDPXbokKttZexfsEPpCvdqoXxe6yJB9tnJfqmPy9s3N_-fJvZXQLrA227iS_K_v3Khyk7r3HfK9vRgQk34zwX_81oIo66eufGidp116yXrANwOfi7zClPB0J-OET6PuLsD1MUwwRXsE49sGY5OuN1ZULvxmlHXxnn26sSzW0dFvQZNSke-uqQfiQf5jjEsw3whnHVNDD0QpykIYIcpAX2vehfYOudfHVqjXPtZW0ZABrvFqglIrOT8w_-MxIWl4MUa6bx90b2Atajwc-zVzb0Mcgt73bg"
}


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://postgres:1111@localhost:5432/{}".format(
            self.database_name)
        setup_db(self.app, self.database_path)
        self.new_actor = {
            'name': 'test name',
            'age': 99,
            'gender': 'male'
        }
        self.new_movie = {
            'title': 'test Movie',
            'release_date': '10/10/2044'}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Success
    # Actors Endpoints
    def test_get_actors(self):
        """Test getting actors"""
        response = self.client().get('/actors', headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Actors'])
        self.assertTrue(len(data['Actors']))

    def test_get_actor_by_id(self):
        """Test get actor by id"""
        response = self.client().get('/actors/{}'.format(1), headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_delete_actor(self):
        """Test delete actor"""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Helpers.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def test_create_actors(self):
        """Test create actor"""

        actors_before = Actor.query.all()
        response = self.client().post('/actors', json=self.new_actor,
                                      headers=producer_auth_header)
        data = json.loads(response.data)
        actors_after = Actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(actors_after) == len(actors_before) + 1)

        # delete the actor to insure db consistency
        created_actor = Actor.query.order_by(Actor.id.desc()).first()
        Helpers.delete(created_actor)

    # Movies Endpoints
    def test_get_movies(self):
        """Test getting movies"""
        response = self.client().get('/movies', headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    def test_get_movie_by_id(self):
        """Test get movie by id"""
        response = self.client().get('/movies/{}'.format(1), headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['data'])

    def test_delete_movie(self):
        """Test delete movie"""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Helpers.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def test_create_movies(self):
        """Test create movie"""

        movies_before = Movie.query.all()
        response = self.client().post('/movies', json=self.new_movie,
                                      headers=producer_auth_header)
        data = json.loads(response.data)
        movies_after = Movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(movies_after) == len(movies_before) + 1)

        # delete the movie to insure db consistency
        created_movie = Movie.query.order_by(Movie.id.desc()).first()
        Helpers.delete(created_movie)

    # RBAC Tests
    # all the roles can see the movies

    def get_movies_as_assistant_successfully(self):
        """Test getting movies as assistant."""
        response = self.client().get('/movies', headers=assistant_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    def get_movies_as_director_successfully(self):
        """Test getting movies as director."""
        response = self.client().get('/movies', headers=director_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    def get_movies_as_producer_successfully(self):
        """Test getting movies as producer."""
        response = self.client().get('/movies', headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    # Only Casting Director and Excutive Producer can delete an actor
    def delete_actor_as_assistant_unsuccessfully(self):
        """Test delete actor as assistant."""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Helpers.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=assistant_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], 'false')
        self.assertEqual(data['message'], 'permission key not found')
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_actor_as_director_successfully(self):
        """Test delete actor as director."""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Helpers.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=director_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_actor_as_producer_successfully(self):
        """Test delete actor as producer."""

        actor = Actor(name=self.new_actor['name'],
                      age=self.new_actor['age'],
                      gender=self.new_actor['gender'])
        Helpers.insert(actor)
        old_total = actor.query.all()
        response = self.client().delete('/actors/{}'.format(int(actor.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    # Only Excutive Producer can delete a movie
    def delete_movie_as_assistant_unsuccessfully(self):
        """Test delete movie as assistant."""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Helpers.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=assistant_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], 'false')
        self.assertEqual(data['message'], 'permission key not found')
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_movie_as_director_unsuccessfully(self):
        """Test delete movie as director."""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Helpers.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=director_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], 'false')
        self.assertEqual(data['message'], 'permission key not found')
        self.assertTrue(len(new_total) == len(old_total) - 1)

    def delete_movie_as_producer_successfully(self):
        """Test delete movie as producer."""

        movie = Movie(title=self.new_movie['title'],
                      release_date=self.new_movie['release_date'])
        Helpers.insert(movie)
        old_total = movie.query.all()
        response = self.client().delete('/movies/{}'.format(int(movie.id)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)
        new_total = movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
        self.assertTrue(len(new_total) == len(old_total) - 1)

    # Error
    # Actors Endpoints
    def test_404_delete_actor(self):
        """Test delete non-existed actor"""

        response = self.client().delete('/actors/{}'.format(int(9999)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    def test_404_get_actor(self):
        """Test get non-existed actor"""

        response = self.client().get('/actors/{}'.format(int(9999)),
                                     headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_400_create_actor(self):
        """Test create actor with empty data"""

        response = self.client().post('/actors', json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'BAD REQUEST')

    def test_404_update_non_existed_actor(self):
        """Test update non-existed actor"""

        response = self.client().patch('/actors/{}'.format(int(9999)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_422_update_actor(self):
        """Test update actor with empty parmas"""

        response = self.client().patch('/actors/{}'.format(int(1)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    # Movies Endpoints
    def test_404_delete_movie(self):
        """Test delete non-existed movie"""

        response = self.client().delete('/movies/{}'.format(int(9999)),
                                        headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    def test_404_get_movie(self):
        """Test get non-existed movie"""

        response = self.client().get('/movies/{}'.format(int(9999)),
                                     headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_422_create_movie(self):
        """Test create movie with empty data"""

        response = self.client().post('/movies', json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')

    def test_404_update_non_existed_movie(self):
        """Test update non-existed movie"""

        response = self.client().patch('/movies/{}'.format(int(9999)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'RECORD NOT FOUND')

    def test_422_update_movie(self):
        """Test update movie with empty parmas"""

        response = self.client().patch('/movies/{}'.format(int(1)),
                                       json={}, headers=producer_auth_header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'UNPROCESSABLE')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

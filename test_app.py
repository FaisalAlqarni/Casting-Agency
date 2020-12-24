import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, Helpers

assistant_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRSVWFGTkNVSFppaE9laGNJTDEyMiJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbC1hbHFhcm5pLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGU5ZjU2ZTAwYTgzMDA2ZTg4ZjhlOSIsImF1ZCI6ImFnaW5jeSIsImlhdCI6MTYwODc1MzAzNSwiZXhwIjoxNjA4NzYwMjM1LCJhenAiOiJXQUExTWJWMXRaWTdRZFZ1VTB3ejdzUFppaGlvYWxLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.QERabspJMJEfWW-xspwtoVhtuaECULqUh3MX5t6TAgfonFT5vkTEZ69es6SUlNUFKsFDokziH28zCsAXgBNafoFru6apY5-d15TYTgaPEJqDcEmef5KtwkRBoRrey20Iny97nki0DBiW0YKogxM_ErX-w2OR6hM_M8zsf_mI0tRIkP9-vZHyk2XgETsWogC6beLmfYTEEwzzAIPJSowAUxru1QzC6DsbKbVXUg6UWkggRqXFbpqR0LiKeZdOAHZYsP2L-c2sKyC1BEWDV-AnZ4IV4N61IneFhum7q7OSHtPt7pKJfxet2zROKtJr4ayI4SgSIp3-H6W-1IgIGE2GWg"
}

director_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRSVWFGTkNVSFppaE9laGNJTDEyMiJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbC1hbHFhcm5pLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGU5ZmI3ZTAwYTgzMDA2ZTg4ZjhlYyIsImF1ZCI6ImFnaW5jeSIsImlhdCI6MTYwODc1MzEyMCwiZXhwIjoxNjA4NzYwMzIwLCJhenAiOiJXQUExTWJWMXRaWTdRZFZ1VTB3ejdzUFppaGlvYWxLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.BMfpqlMfcHiC3Su6P5s1R0z4aRdYfKtPo5m8B8xXNyyjjX6eAgtBOreK6z7ILa32SjNddqEpw_3nBWqOBS41YYtMBR6az2q-AG9Cgek7emXt3GCEvV7kA0bu0wBgGaEHldxJ39ig6ZpYOufLcY9_p7rdRNHT-YOnh7yR2pjfGTInPNjvufpRAt1FNlpha0MSTFahYDK9ob11P6GoISqu5nLeymFy7whznOLpGWh1_yTSL2YRascOxHRkuyp8_yoNyFfBJGii-DwC9GGxaZ5q4nVvHq9hR6BRogKYmzDrxPWmpIHWKpATyK7eNJhgTODAxopg3AzFrP3NJfuObbdshw"
}

producer_auth_header = {
    'Authorization': "Bearer " + "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InRSVWFGTkNVSFppaE9laGNJTDEyMiJ9.eyJpc3MiOiJodHRwczovL2ZhaXNhbC1hbHFhcm5pLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZGVhMGQxNzgyMzhiMDA3MTk2NTU4MCIsImF1ZCI6ImFnaW5jeSIsImlhdCI6MTYwODc1MzE3OSwiZXhwIjoxNjA4NzYwMzc5LCJhenAiOiJXQUExTWJWMXRaWTdRZFZ1VTB3ejdzUFppaGlvYWxLTSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.tftQmWcuNMSBCV0uLPLYebXEs1uHYLv8CzJ5XUa0T39l-P8U3gcFPaah9bpmkYyeHYngJ2GjtpyaJeFqflXf1gZM6bUO5dbUKYfr7q5uVn1ddBf9bjyCfvDyhRGzP3cRggIJ1KCOpbXXxPsIHrZcGn0FtC78FPdOnk3EPol3tGIC0b7n7Df5GY4fe8EshcRgPXkGK-K4GjlciQhAsr6xlPK6SFhMQEyTSlF75e6ZHnJ-i1Bmc2no3c-5cZQo8hC3b1I8a1_NjwgkHylaILvaj7b2mpSN5NCCBPw-uz3YzTY840VUnrA2cU10Yd1O6FQrVF7LdxbZX-u7aMpO25KXMw"
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

import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, Helpers


class CastingTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgres://postgres:1111@localhost:5432/{}".format(self.database_name)
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

    def test_get_actors(self):
        """Test getting actors"""
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Actors'])
        self.assertTrue(len(data['Actors']))

    def test_get_actor_by_id(self):
        """Test get actor by id"""
        response = self.client().get('/actors/{}'.format(1))
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
            response = self.client().delete('/actors/{}'.format(int(actor.id)))
            data = json.loads(response.data)
            new_total = actor.query.all()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], actor.id)
            self.assertTrue(len(new_total) == len(old_total) - 1)

    def test_create_actors(self):
        """Test create actor"""

        actors_before = Actor.query.all()
        response = self.client().post('/actors', json=self.new_actor)
        data = json.loads(response.data)
        actors_after = Actor.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(actors_after) == len(actors_before) + 1)

        # delete the actor to insure db consistency
        created_actor = Actor.query.order_by(Actor.id.desc()).first()
        Helpers.delete(created_actor)


    def test_get_movies(self):
        """Test getting movies"""
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['Movies'])
        self.assertTrue(len(data['Movies']))

    def test_get_movie_by_id(self):
        """Test get movie by id"""
        response = self.client().get('/movies/{}'.format(1))
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
            response = self.client().delete('/movies/{}'.format(int(movie.id)))
            data = json.loads(response.data)
            new_total = movie.query.all()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(data['deleted'], movie.id)
            self.assertTrue(len(new_total) == len(old_total) - 1)

    def test_create_movies(self):
        """Test create movie"""

        movies_before = Movie.query.all()
        response = self.client().post('/movies', json=self.new_movie)
        data = json.loads(response.data)
        movies_after = Movie.query.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(movies_after) == len(movies_before) + 1)

        # delete the movie to insure db consistency
        created_movie = Movie.query.order_by(Movie.id.desc()).first()
        Helpers.delete(created_movie)

    # # Error
    # def test_422_get_actors(self):
    #     """Tests actor pagination exceeding allowed pages"""

    #     response = self.client().get('/actors?page=9999')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')

    # def test_404_delete_actor(self):
    #     """Test delete non-existed actor"""

    #     response = self.client().delete('/actors/{}'.format(int(9999)))
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_400_create_actor(self):
    #     """Test create actor with empty data"""

    #     response = self.client().post('/actors', json={})
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'bad request')

    # def test_404_search_actors(self):
    #     """Test searching non-exist actor/s"""

    #     response = self.client().post(
    #         '/actors', json={'searchTerm': 'aaaaaaaaaaaaa'})
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_404_get_actors_on_category(self):
    #     """Tests getting no actors in category"""

    #     response = self.client().get('/categories/9999/actors')
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'resource not found')

    # def test_422_get_quiz_with_random_actors(self):
    #     """Test start quiz without passing quiz_category or previous_actors"""

    #     response = self.client().post('/quizzes', json={})
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 422)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

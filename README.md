# FSND-Casting-Agency
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This is a system to simplify and streamline the process.

## LIVE URL : https://capstone-misk.herokuapp.com/
use the live URL to see teh roles Credentials and sign in using them and getting the TOKEN afterwards, then use the token inside the postman collection with respected role in order to test the endpoints.

## Tech Used
- Python
- Flask with SQLAlchemy
- Postgres SQL
- Auth0
- Heroku
- Postman

### Installing Dependencies

#### Python 3.7.9
Preferrably install Python 3.7.9

##### Set up a Virtual Enviornment
To create a virtual environment, go to your project’s directory and run venv. If you are using Python 2, replace venv with virtualenv in the below commands.

On macOS and Linux:
```bash
python3 -m venv env
```
On Windows:
```bash
py -m venv env
```


##### Activate a Virtual Enviornment
On macOS and Linux:
```bash
source env/bin/activate
```
On Windows:
```bash
.\env\Scripts\activate
```

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the **root directory** and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.


### Setting Up Project Locally
After succesfully installing all requirements for the project. You can setup the project locally by following the steps below:

1. Create Databases. 
```
psql -c "CREATE DATABASE casting" "user=postgres dbname=postgres password=1111"
psql -c "CREATE DATABASE casting_test" "user=postgres dbname=postgres password=1111"
```

2. Configure the models.py / test_app.py with appropiate variables.
```
database_path ='postgresql://postgres:1111@localhost:5432/casting'
database_path ='postgresql://postgres:1111@localhost:5432/casting_test'
```

4. Run the application by using the command below
```
flask run
```

### API Endpoints
Listed below are the Endpoints in the system
- GET /
- GET /callback
- GET /actors
- GET /movies
- GET /actors/<int:id>
- GET /movies/<int:id>
- POST /actors
- POST /movies
- PATCH /actors/<int:id>
- PATCH /movies/<int:id>
- DELETE /actors/<int:id>
- DELETE /movies/<int:id>


#### Roles and Endpoints (RBAC Controls)
This API has Three Roles which have different differet access to endpoints. Listed below are the accesible and allowed endpoints for each user. Each request must be sent with an Authorization Header which is a Bearer Token
```
 "Authorization" : "Bearer (TOKEN)"
```

- Casting Assistant
  - GET /
  - GET /actors
  - GET /movies
  
- Casting Director
  - GET /
  - GET /actors
  - GET /movies
  - POST /actors
  - PATCH /actors/<int:id>
  - PATCH /movies/<int:id>
  - DELETE /actors/<int:id>
 
- Executive Director
  - GET /
  - GET /actors
  - GET /movies
  - POST /actors
  - POST /movies
  - PATCH /actors/<int:id>
  - PATCH /movies/<int:id>
  - DELETE /actors/<int:id>
  - DELETE /movies/<int:id>



### API Endpoints Behaviour


#### GET /actors
- Description: Return a list of all actors in the Database
- Request argument: None
- Example Response: 
```
{
    "Actors": [
        {
            "age": 18,
            "gender": "male",
            "id": 1,
            "name": "First"
        },
        {
            "age": 25,
            "gender": "male",
            "id": 2,
            "name": "Second"
        },
        {
            "age": 40,
            "gender": "male",
            "id": 3,
            "name": "Third"
        },
        {
            "age": 13,
            "gender": "female",
            "id": 4,
            "name": "Thirds"
        },
        {
            "age": 16,
            "gender": "femal",
            "id": 5,
            "name": "wally"
        },
        {
            "age": 20,
            "gender": "male",
            "id": 6,
            "name": "jhon"
        },
        {
            "age": 18,
            "gender": "male",
            "id": 7,
            "name": "First"
        },
        {
            "age": 25,
            "gender": "male",
            "id": 8,
            "name": "Second"
        },
        {
            "age": 40,
            "gender": "male",
            "id": 9,
            "name": "Third"
        },
        {
            "age": 13,
            "gender": "female",
            "id": 10,
            "name": "Thirds"
        },
        {
            "age": 16,
            "gender": "femal",
            "id": 11,
            "name": "wally"
        },
        {
            "age": 20,
            "gender": "male",
            "id": 12,
            "name": "jhon"
        }
    ],
    "success": true
}
```
#### GET /movies
- Description: Return a list of all movies in the Database
- Request argument: None
- Example Response:
```
{
    "Movies": [
        {
            "actors": [
                "First",
                "Second",
                "Third",
                "Thirds",
                "wally",
                "jhon"
            ],
            "id": 1,
            "release_date": "10/10/2010",
            "title": "First Movie"
        },
        {
            "actors": [
                "First",
                "Second",
                "Third"
            ],
            "id": 2,
            "release_date": "1/12/2015",
            "title": "Second Movie"
        },
        {
            "actors": [
                "Thirds",
                "wally",
                "jhon"
            ],
            "id": 3,
            "release_date": "1/10/2018",
            "title": "Final Movie"
        },
        {
            "actors": [
                "First",
                "Second",
                "Third",
                "Thirds",
                "wally",
                "jhon"
            ],
            "id": 4,
            "release_date": "10/10/2010",
            "title": "First Movie"
        },
        {
            "actors": [
                "First",
                "Second",
                "Third"
            ],
            "id": 5,
            "release_date": "1/12/2015",
            "title": "Second Movie"
        },
        {
            "actors": [
                "Thirds",
                "wally",
                "jhon"
            ],
            "id": 6,
            "release_date": "1/10/2018",
            "title": "Final Movie"
        }
    ],
    "success": true
}
```
#### GET /actors/<int:id>
- Description: Return actors by his id
- Request argument: ID 
- Example Response: 
```
{
    "data": {
        "age": 20,
        "gender": "male",
        "id": 6,
        "name": "jhon"
    },
    "success": true
}
```
#### GET /movies/<int:id>
- Description: Return a list of all movies in the Database
- Request argument: None
- Example Response:
```
{
    "data": {
        "actors": [
            "First",
            "Second",
            "Third"
        ],
        "id": 2,
        "release_date": "1/12/2015",
        "title": "Second Movie"
    },
    "success": true
}
```

#### POST /actors
- Description: Create a new Actor, Insert a new actor into the Database
- Request argument: None
- Request Body : 
```
{
	"name": "name",
	"age": 50,
	"gender": "male"
}
```
- Example Response:
```
{
    "actor": {
        "age": 50,
        "gender": "male",
        "id": 13,
        "name": "name"
    },
    "success": true
}
```

#### POST /movies
- Description: Create a new Movie, Insert a new movie into the Database
- Request argument: None
- Request Body :
```
{
	"title": "hh",
	"release_date": "1/1/2010"
}
```
- Example Response:
```
{
    "movie": {
        "actors": [],
        "id": 7,
        "release_date": "1/1/2010",
        "title": "hh"
    },
    "success": true
}
```

#### PATCH /movies/<int:id>
- Description: Update an existing Movie details
- Request argument: ID
- Request Body : the title or the release date, Any or Both of these fields can be updated
```
{
	"title": "changed"
}
```
- Example Response:
```
{
    "actor": {
        "actors": [
            "Thirds",
            "wally",
            "jhon"
        ],
        "id": 3,
        "release_date": "1/10/2018",
        "title": "changed"
    },
    "success": true
}
```

#### PATCH /actors/<int:id>
- Description: Update an existing Actor's Details using the Actor's ID
- Request argument: ID
- Request Body : the Name or the Age or the Gender, any or all of them can be updated
```
{
	"name": "changed"
}
```
- Example Response:
```
{
    "actor": {
        "age": 20,
        "gender": "male",
        "id": 6,
        "name": "changed"
    },
    "success": true
}
```

#### DELETE /actors/<int:id>
- Description: Delete an existing Actor using the Actor's ID
- Request argument: ID - Actor ID - 1
- Request Body : None
- Example Response:
```
{
  "deleted": 1,
  "success": true
}
```

#### DELETE /movies/<int:id>
- Description: Delete an existing Movie using the Movie's ID
- Request argument: 
- Request Body : None
- Example Response:
```
{
    "deleted": 6,
    "success": true
}
```
### Testing the Application Locally
You can carry out unit tests on the application by following the steps below:

1. Create Test Database- Skip this step if you already created and configured the test DB earlier

2. Run Test
```
python test_app.py
```

## Hosting
This Application is hosted on Heroku  
**Live URL** : http://capstone-misk.herokuapp.com/


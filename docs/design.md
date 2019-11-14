# Design Doc

### Raison D'être

There are a lot of variables to consider when baking your own bread: ingredient ratios, proof time, oven temperature, mixing technique - even whether you add water to flour or add flour to water. Each of these variables can have a significant impact on the final bread. When experimenting with new bread recipes, it is easy to lose track of what changes you have tried and what the result was of that change.

Bread app is a tool that allows you to easily record experiments in bread in a more-or-less scientific way, and to visualize how different ingredients and procedures interact with each-other.

### MVP Features

#### Core

**Client**

- Users - Register new user - Log in/log out - edit user data(email, password)
- Create new bread recipes
- Update, delete bread recipes
- View list of all bread recipes - filter by ingredients, other params - sort by various params(date created, rating)
- Generate scatter-plot charts from bread queries

**Recipes API**

- Create, Update, Delete recipes in document database
- Query recipes using query strings - by ingredients in that recipe - by creator - by rating - etc.

**Users API**

_While, by design, the application will only have one user - and as such not require login, logout, or authentication - I want to include a full authentication flow for practice._

- Create new users - Hash passwords with BCrypt
- Log in and log out with tokens

#### Optional

**Client**

- Plot multiple data sets on a single chart, to compare
- Export recipes to MyFitnessPal

### Architecture

#### Stack

##### Front-End

- **[Vue.js 2.0](https://vuejs.org/):** My prefered JavaScript framework for web apps

##### Back-End

- **[FastAPI](https://fastapi.tiangolo.com/):** Python RESTful API framework
- [pyArango](https://github.com/ArangoDB-Community/pyArango): Python driver for ArangoDB
- [passlib](https://passlib.readthedocs.io/en/stable/): Password hashing
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/): for generating tokens
- [python-multipart](https://andrew-d.github.io/python-multipart/): for accepting authentication credentials

###### _Dev Dependencies_

- [pre-commit](https://pre-commit.com/)
- [pipenv](https://pipenv.readthedocs.io/en/latest/)
- [black](https://github.com/psf/black)
- [iSort](https://github.com/timothycrosley/isort)
- [mypy](http://www.mypy-lang.org/)
- [flake8](http://flake8.pycqa.org/en/latest/index.html#)

###### Database

Data will be stored in a **document data-store** for the following reasons:

1.  There are no _intuitive_ relations between different data models. I tried to model a bread recipe using the relational model and it felt painfully contrived.
2.  Recipes, traditionally, are _documents_.
3.  Recipes can have different fields from each other.

I am evaluating **[ArangoDB](https://www.arangodb.com/)** as my document database for this project.

#### Data Models

<!-- TODO: REPLACE WITH REAL JSON -->

**RECIPE**

- `id`: \_key
- `creator`: \_key
- `dateCreated`: date
- `ingredients`: list
  - `ingredient`: obj
    - `name`: str
    - `quantity`: float
    - `unit`: str (or convert everything to g or mL before saving)
    - _nutritional macros_
- `procedures`: list
  - `procedure`: obj (options: mix, proof, bake)
    - `time`: int (min, required for bake and proof)
    - `temperature`: int (deg F, required for bake and proof)
    - `details`: str
- `shape`: str
- `yield`: int
- `results`: obj
  - `rating`: int (min=0, max=5)
  - `image`: url
  - `notes`: str

**USER**

- `id`: int
- `email`: str
- `hashedPassword)`: str (bcrypt)

### Views

> TODO: views

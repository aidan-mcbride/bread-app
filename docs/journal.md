# Development Journal

#### 10/30/19

Started project planning; began work on design document.

I spent way more time than I would have like to trying to find an ingress into this project. It's hard to start when you're looking at the proverbial blank page: Should I define my data models first? Should I do my views first? Should I define my tech stack? What depends on what? There must be some resource out there that outlines a workflow for the very beginning phases of planning a new project - though, in this case, I think some of the difficulty in planning my application is that many of the project's goals are based around learning specific technologies, rather than solving actual problems.

I decided to start with the data models since that's the core of the whole thing, and I have some existing data that I can anchor on.

> Data modeling resources:
>
> - https://www.arangodb.com/docs/stable/data-modeling.html
> - https://highlyscalable.wordpress.com/2012/03/01/nosql-data-modeling-techniques/
>
> Design doc resources:
>
> - https://www.khanacademy.org/computing/computer-programming/programming/good-practices/a/planning-a-programming-project
> - https://github.com/scottydocs/README-template.md/blob/master/README.md

**TODO TOMORROW:**

- [x] Data models: take sketches and turn into real, arangodb models(see resource above)
- [x] Design doc: describe data models/schemas
- [x] Design doc: describe interactions/flows/features of app (things it will do, high level)
- [x] Design doc: describe technologies that will be used in project and why.

---

#### 10/31/19

> Problem: A `recipe` can contain a list of `ingredient`s; One `ingredient` can be included in multiple `recipe`s. How do I create this relationship in ArangoDB?

> Problem: A `recipe` can contain a list of `procedure`s; procedures can be one of a finite number of types(e.g. mix, proof, bake) - how do I enforce this, and disallow arbitrary new procedure types?

I found two articles yesterday that looked like they may provide some insight into how to solve these problems, which I then read today. Neither was all that helpful. I tried to find some more information about modeling relationships in a NOSQL database, but didn't really find anything useful. I've learned that sometimes, if you don't find any answers, it's because you are asking the wrong question. I think that these problems may be application-level problems rather than database-level problems.

I found these two resources in the FastAPI documentation:

- https://fastapi.tiangolo.com/tutorial/body-nested-models/
- https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values

I think I will be able to constrain my `procedure` types using `Enum`, so that only certain types of procedures can be created, and then I can do something to restrict what fields are available for each type (e.g. a bake time doesn't make sense as a field unless the procedure type is bake)

I think i can define `ingredients` simply as a nested pydantic model. I'm not sure how this will translate into the database, but I'll cross that bridge when I come to it.

_(several hours later...)_

After thinking about it some more, I don't think that there will be a problem with `ingredients`. My initial concern was: if an ingredient is updated, how will those updates be propogated to all recipes using that ingredient so that data integrity is maintained? Here's what I realized:

1. While I want to be able to query recipes by the ingredients within them, the _quantity_ of an ingredient within a recipe is specific to that recipe. What I really wanted to avoid was, for example, having a recipe that had `yeast` as an ingredient, and another recipe that had `active dry yeast` as an ingredient, and not being able to retrieve both of those recipes when querying for recipes containing yeast; The solution to this is to retrieve a list of all unique ingredients used in all recipes, and then use this list when adding ingredients to new recipes.
2. Suppose that, at some point, I change the brand of flour that I am using, and want to update my `flour` document with the new brand. While all future recipes would use the new brand, _old recipes would still have used the old brand_. Therefor, I would not want to update any recipes' ingredients if an ingredient was changed.

It occurs to me now that these problems were never really problems, but were actually features of a document data-store over a relational database. I think I just need more time to get into the mindset of working with document data-stores.

I found [this excellent article on Dev.to](https://dev.to/guin/a-plan-for-planning-your-first-side-project-2b2l) about planning a side project. I am using it for writing the rest of the design doc.

I moved this dev journal, as well as the design doc, to their own files; the `README` will be a traditional readme with information that is more relevant to the end user and outside parties.

---

#### 11/1/19

> TODO
>
> - [x] README-Driven Development: sketch in as much of a README as you can
> - [x] Prepare python development environment: decide on CI tools, linters, etc. (document in design doc)
> - [ ] Add cards to GitHub project board for REST API
> - [ ] Start coding: TDD based on cards

> **Python tooling:**
>
> - https://sourcery.ai/blog/python-best-practices/
> - https://realpython.com/python-continuous-integration
> - https://realpython.com/python-code-quality/
> - https://realpython.com/documenting-python-code/
> - https://realpython.com/python-comments-guide/
> - https://hackernoon.com/setting-up-a-python-development-environment-in-atom-466d7f48e297

Readme template generator: https://github.com/kefranabg/readme-md-generator

There wasn't a whole lot I could add to the readme at this stage. I will add instructions for installing and running as soon as I know how those will be done.

Added cards for setting up CI; this needs to be done before going into the API

To set pipenv to put the virtual enviornment in the project directory:

```sh
export PIPENV_VENV_IN_PROJECT=true
```

see: https://pipenv.readthedocs.io/en/latest/advanced/#custom-virtual-environment-location

I found this article that has more options for python tooling, if there is a need for more later:
https://medium.com/georgian-impact-blog/python-tooling-makes-a-project-tick-181d567eea44

I used the [sourcery article](https://sourcery.ai/blog/python-best-practices/) to set up my tooling. I'm almost certain that my config for these will break once I get some code in there. In retrospect, I should have coded a hello-world or something to test my tools on first.

I tried doing a PR today - I won't be doing them for the rest of the project; they take too much time and are unnecessary for a project like this.

**Travis-CI for bread app:**
https://travis-ci.org/aidan-mcbride/bread-app

I decided to use travis because I am already somewhat familiar with it.

---

#### 11/2/19

**PROBLEM: pytest can't find module**

when running `pipenv run pytest` the following error occurs:

```
_____________________ ERROR collecting tests/test_main.py ______________________
ImportError while importing test module '/mnt/DATA/Code/bread-app/tests/test_main.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
tests/test_main.py:3: in <module>
    from api.main import app
E   ModuleNotFoundError: No module named 'api'
```

when running **`pipenv run python -m pytest`**, tests run fine.

**SOLUTION:**

https://docs.pytest.org/en/latest/usage.html#calling-pytest-through-python-m-pytest

the problem is caused by the project directory not being added to the `sys.path`

there are several solutions:

1.  [add `conftest.py` to project root directory](https://stackoverflow.com/a/50610630)
2.  [`export PYTHONPATH=.`](https://stackoverflow.com/a/10253916)
3.  [run pytest with `pipenv run python -m pytest`, which will add the current working directory to the `sys.path`](https://docs.pytest.org/en/latest/usage.html#calling-pytest-through-python-m-pytest)

Merged dev branch back into master once I got a working hello-world with tooling config. This will be my jumping-off point for the app.

> Eric Elliott's 5 questions every unit test must answer:
>
> 1. What are you testing?
> 2. What should it do?
> 3. What is the _expected_ output?
> 4. What is the _actual_ output?
> 5. How can the test be reproduced? _(answered implicitly in > test structure by the code used to produce the `actual` > value)_
>
> ```python
> def test_some_component():
>   actual = 'what is the expected output?'
>   expected = 'what is the expected output?'
>
>   assert expected == actual
> ```
>
> example:
>
> ```python
> def test_hello_world():
>   response = client.get("/")
>
>   # test for status code
>   actual = response.status_code
>   expected = 200
>   assert expected == actual
>
>   # test for response content
>   actual = response.json()
>   expected = {"msg": "Hello World"}
>   assert expected == actual
> ```

I'm going to start into my app by following along to the [fastapi tutorial](https://fastapi.tiangolo.com/tutorial/first-steps/), but substituting my needs.

Barring the parts about SQLAlchemy, [this section of the FastAPI docs has a good workflow for organizing api code into files](https://fastapi.tiangolo.com/tutorial/sql-databases/)

to run pre-commit hook without actually committing:

```sh
pipenv run pre-commit run --all-files
```

to commit without running pytest hook

```sh
SKIP=pytest git commit
```

See here for explanation of `recipe = Recipe(**recipe_in.dict())` in `recipes.py`
https://fastapi.tiangolo.com/tutorial/extra-models/#about-user_indict

---

#### 11/3/19

**PROBLEM: How to add a testing database? Specifically, how to use ArangoDB in continuous integration?**

In the final application, ArangoDB will be a docker container, but I don't know if that is feasible for running CI tests.

I found [this Travis-CI documentation](https://docs.travis-ci.com/user/database-setup/) which explains how to use various databases with Travis-CI, though ArangoDB is not one of them.

I found [this GitHub repo](https://github.com/brennv/arangodb-travis) that looks promising for learning how to integrate ArangoDB into Travis-CI.

I found [This Travis-CI documentation on using docker](https://docs.travis-ci.com/user/docker/), and it may be that the best solution is to use the docker version of ArangoDB.

The problem is, though, that I barely know how to just use ArangoDB in a python application; therefor, this is the path forward as I see it:

1. Create a [spike](https://stackoverflow.com/questions/249969/why-are-tdd-spikes-called-spikes) on a new branch, Integrate local ArangoDB into existing endpoints _(GET, POST for collection)_.
2. Set up tests to use separate test database locally
3. Add database to Travis-CI config.

---

#### 11/4/19

> **TODO:**
>
> - [x] Get database working at all

**WHAT'S GOING ON IN [THIS EXAMPLE](https://fastapi.tiangolo.com/tutorial/nosql-databases/)**

- `get_bucket()` initializes a database connection and returns a database that can be operated upon.
  - this function is called anywhere that needs a database connection. _Can it be abstracted into a dependency or something?_
- `get_user()` is a _db_op_, and the `bucket` is passed as a variable. It is unclear if a Couchbase `bucket` is equivalent to an ArangoDB `db` or `collection`.
- `read_user()` is the _route_, and it is where `get_bucket()` is called, and the result of that is passed to `get_user()`

**[PYARANGO FLOW](https://www.arangodb.com/tutorials/tutorial-python/)**

1. initialize database connection
2. create database if not exist
3. create collection if not exist
4. operate on collection

pyArango's [method for converting a document to JSON](https://bioinfo.iric.ca/~daoudat/pyArango/document.html#pyArango.document.Document.toJson) is bugged, so in the `read_recipes()` function in `db_ops.py` are some work-arounds until that is fixed.

---

#### 11/5/19

> **TODO:**
> In spike:
>
> - [x] Add test db as override dependency in tests
> - [x] Get both dbs using correct credentials
> - [ ] See about giving breadapp user the power to create datbases.
>
> In `develop`:
>
> - [x] Rebuild spike with TDD (GET, POST to database)
> - [x] Add ArangoDB Docker to travis config

- [Using **Docker** in **Travis-CI**](https://docs.travis-ci.com/user/docker/)
- [Using **ArangoDB** in **Docker**](https://www.arangodb.com/download-major/docker/)

possible scripts for arango test db, if you don't want to just use root/no auth:

```Travis
  - docker run -d -p 8529:8529 -e ARANGO_NO_AUTH=1 arangodb/arangodb:3.5.1
  - arangosh --server.authentication false
  - db._createDatabase("breadapp_testing");
  - var users = require("@arangodb/users");
  - users.save("breadapp", "breadapp")
  - users.grantDatabase("breadapp", "breadapp_testing");
  - exit
```

---

#### 11/6/19

[Documentation for arangodb docker container](https://hub.docker.com/r/arangodb/arangodb/)

[This version of the documentation - which includes the `document.toJson()` method](https://bioinfo.iric.ca/~daoudat/pyArango/index.html) is outdated. I don't even know how I found my way to that version of the docs. **[This is the up-to-date documentation.](https://pyarango.readthedocs.io/en/latest/)** This version includes the `document.getStore()` method, which returns a dictionary of the document.

---

#### 11/9/19

[Python 'f-string' literal interpolation](https://www.python.org/dev/peps/pep-0498/), an alternative way to format strings.

I see the term `skip` used consistently in place of `offset` when discussing NOSQL databases, so I am using `skip` in my code for now.

**[ArangoDB Array operators](https://www.arangodb.com/docs/stable/aql/operators.html#array-comparison-operators)** - I am using the `ALL IN` operator to query for ingredients in a recipe.

The ArangoDB **[`[*]` operator](https://www.arangodb.com/docs/stable/aql/advanced-array-operators.html#array-expansion)** iterates over all elements in an array.

---

#### 11/10/19

**General steps to add users:**

1. Get users working on their own

- Pydantic schemas with password hashing
- db ops with password hashing
- endpoints: POST `/`, GET `/`, `/id`, PUT `/id`, DELETE `/id`

2. Add authentication

- log in, log out, verify with JWT
- require authentication for some endpoints

3. Add user id to recipes created by that user.

---

#### 11/11/19

[FastAPI docs on implementing security with OAuth2](https://fastapi.tiangolo.com/tutorial/security/first-steps/)

**Password flow:**

1. user(client) submits a `username` and `password` to a specific url on the API
2. api verifies `username` and `password`, responds with a `token`
3. client stores `token`, sends in header of all future requests.

routes that require authentication have a _dependency_ of `get_current_user()`, which in turn has a _dependency_ of `get_token()`.

#### 11/12/19

_If I were to use ArangoDB again in the future for a real project, I would perhaps use the user's `email` as the `_key` in the database. I think this would implicitly validate for unique email addresses, while also removing the need to be able to query users by both `_key` and `email`. The downside to this would be that a user may be unable to change the email address associated with their account._

_I think the real best solution would be to embrace NOSQL and store users in an SQL database, while storing recipes in a document database._

**Total Authentication Flow:**

1. client submits `username` and `password` to `/login` API endpoint. `/login` function does:
   1. use `db_ops` to get user data from database, using `username`(email) as query parameter.
      1. If no user found with matching `username`(email), raise `HTTPException(400)` _(See FastAPI example)_
      2. `db_ops` must return a `hashed_password`, though it is important that this hashed password never finds its way into any response bodies.
   2. use passlib to verify that the client's `password` matches the one stored in the database
      1. If password does not check out, raise `HTTPException(400)`
   3. Generate JWT Token
   4. **return a `JWT Token`** to client.
   5. _Client stores token somewhere, send in header of future requests_
2. Client attempts to access a secure endpoint, and includes the `token` in the header of their request.
3. Secure endpoint has a **_dependency_** of `get_current_active_user`
   1. _`get_current_active_user` inherits from `get_current_user`, and additionally validates that the user's account is active._
   2. `get_current_user` in turn has a _dependency_ of **`get_token`**
      1. `get_token` is assigned to FastAPI's `OAuth2PasswordBearer`, with `tokenUrl="/login"` as a parameter.
      2. Decode JWT token, verify user identity from token data.
         1. If verification fails, raise exception
      3. get the user from the db using the token data.
      4. return user.

#### 11/13/19

> **TODO:**
>
> - [x] Refactor user models: see diagram
> - [x] Refactor db_ops to return raw data to endpoint functions, which in turn return cleaned data to client
> - [x] Implement authentication function in user db_ops
> - continue implementing authentication
> - make a diagram of how authentication works when done.

I noticed in the FastAPI example project - which I am using as a reference - that the `User` in their `crud.py` file, which I assumed was a pydantic model, _is actually an SQLAlchemy model_.

**NEW USERS SCHEMA FLOW:**

![New Users Schema Flow](docs/diagrams/user-schema-flow.svg)

#### 11/14/19

I know it is silly that any user can get all the data for all other users via `GET:/users/`, and yet is prevented from getting data on other users when using `GET:/users/{id}`, and I would not do this on a real app. In the case of breadapp, however, the entire idea of authentication is silly, and was done entirely as a proof-of-concept.

To solve this in a real app, you would restrict access to `GET:/users` to _superusers_, and regular users could only retrieve data about their user via `GET:/users/{id}`. Or, you would simply not have a `GET:/users` endpoint if you did not need it.

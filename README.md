# Bread App

Use data to scientifically iterate your bread recipes and procedures!

---

## Design Doc?

<!-- raison d'être -->

There are a lot of variables to consider when baking your own bread: ingredient ratios, proof time, oven temperature, mixing technique - even whether you add water to flour or add flour to water. Each of these variables can have a significant impact on the final bread. When experimenting with new bread recipes, it is easy to lose track of what changes you have tried and what the result was of that change.

Bread app is a tool that allows you to easily record experiments in bread in a more-or-less scientific way, and to visualize how different ingredients and procedures interact with each-other.


#### Features

**recipes api**
* Add new recipes to the database
* Update recipes in DB
* Delete recipes from DB
* Query recipes on various parameters:
	* by ingredients in that recipe
	* by creator
	* by rating
	* etc.

**users api**
*While by design the application will only have one user, I want to include a total authentication flow - for practice.*
* Create new users securely
	* hash passwords
* Login and log out with tokens

#### Stack

##### Front-End

* **[Vue.js 2.0](https://vuejs.org/):** JavaScript framework

##### Back-End

* **[FastAPI](https://fastapi.tiangolo.com/):** Python RESTful API framework
* **[ArangoDB](https://www.arangodb.com/):** Multi-model NOSQL database



#### Data

Data will be stored in a **document data-store** for the following reasons:

1.  There are no _intuitive_ relations between different data models. I tried to model a bread recipe using the relational model and it felt painfully contrived.
2.  Recipes, traditionally, are _documents_.
3.  Recipes can have different fields from each other.

I am evaluating **[ArangoDB](https://www.arangodb.com/)** as my document database for this project.

**RECIPE SCHEMA**

- `id`: _key
- `creator`: _key
- `dateCreated`: date
- `ingredients`: list
  - `ingredient`: obj<sup>1</sup>
    - `name`: str
    - `quantity`: float
    - `unit`: str (or convert everything to g or mL before saving)
    - _nutritional macros_
- `procedures`: list
  - `procedure`: obj (options: mix, proof, bake)<sup>2</sup>
    - `time`: int (min, required for bake and proof)
    - `temperature`: int (deg F, required for bake and proof)
    - `details`: str
- `shape`: str
- `yield`: int
- `results`: obj
  - `rating`: int (min=0, max=5)
  - `image`: url
  - `notes`: str

**<sup>1</sup>ingredient:**
nested schema - describes a single ingredient.
MANY-TO-MANY: one recipe can have many ingredients, one ingredient can be used in many recipes
_Optionally_, include basic macro-nutrient information, such as calories, **or** a link to connect this ingredient to some external nutritional database.

**<sup>2</sup>procedure:**
nested schema - describes a step for making the bread.
there are several types of procedure, including _mixing_ the dough, _proofing_, and _baking_. Maybe each type of procedure is also a schema?
Each procedure type has its own required fields.
either ONE-TO-MANY or MANY-TO-MANY: one recipe will always have many procedures, but idk if a single procedure will be used in many recipes, or if each recipe's procedures are unique.

**USER SCHEMA**

- `id`: int
- `email`: str
- `hashedPassword)`: str (bcrypt)



---

## Development Journal

#### 10/30/19

Started project planning; began work on design document.

I spent way more time than I would have like to trying to find an ingress into this project. It's hard to start when you're looking at the proverbial blank page: Should I define my data models first? Should I do my views first? Should I define my tech stack? What depends on what? There must be some resource out there that outlines a workflow for the very beginning phases of planning a new project - though, in this case, I think some of the difficulty in planning my application is that many of the project's goals are based around learning specific technologies, rather than solving actual problems.

I decided to start with the data models since that's the core of the whole thing, and I have some existing data that I can anchor on.


> Data modeling resources:
> 
> * https://www.arangodb.com/docs/stable/data-modeling.html
> * https://highlyscalable.wordpress.com/2012/03/01/nosql-data-modeling-techniques/
> 
> Design doc resources:
> 
> * https://www.khanacademy.org/computing/computer-programming/programming/good-practices/a/planning-a-programming-project
> * https://github.com/scottydocs/README-template.md/blob/master/README.md


**TODO TOMORROW:**
* [x] Data models: take sketches and turn into real, arangodb models(see resource above)
* [x] Design doc: describe data models/schemas
- [ ] Design doc: describe interactions/flows/features of app (things it will do, high level)
- [ ] Design doc: describe technologies that will be used in project and why.


#### 10/31/19

> Problem: A `recipe` can contain a list of `ingredient`s; One `ingredient` can be included in multiple `recipe`s. How do I create this relationship in ArangoDB?

> Problem: A `recipe` can contain a list of `procedure`s; procedures can be one of a finite number of types(e.g. mix, proof, bake) - how do I enforce this, and disallow arbitrary new procedure types?

I found two articles yesterday that looked like they may provide some insight into how to solve these problems, which I then read today. Neither was all that helpful. I tried to find some more information about modeling relationships in a NOSQL database, but didn't really find anything useful. I've learned that sometimes, if you don't find any answers, it's because you are asking the wrong question. I think that these problems may be application-level problems rather than database-level problems.

I found these two resources in the FastAPI documentation:
* https://fastapi.tiangolo.com/tutorial/body-nested-models/
* https://fastapi.tiangolo.com/tutorial/path-params/#predefined-values

I think I will be able to constrain my `procedure` types using `Enum`, so that only certain types of procedures can be created, and then I can do something to restrict what fields are available for each type (e.g. a bake time doesn't make sense as a field unless the procedure type is bake)

I think i can define `ingredients` simply as a nested pydantic model. I'm not sure how this will translate into the database, but I'll cross that bridge when I come to it.

*(several hours later...)*

After thinking about it some more, I don't think that there will be a problem with `ingredients`. My initial concern was: if an ingredient is updated, how will those updates be propogated to all recipes using that ingredient so that data integrity is maintained? Here's what I realized:

1. While I want to be able to query recipes by the ingredients within them, the *quantity* of an ingredient within a recipe is specific to that recipe. What I really wanted to avoid was, for example, having a recipe that had `yeast` as an ingredient, and another recipe that had `active dry yeast` as an ingredient, and not being able to retrieve both of those recipes when querying for recipes containing yeast; The solution to this is to retrieve a list of all unique ingredients used in all recipes, and then use this list when adding ingredients to new recipes.
2. Suppose that, at some point, I change the brand of flour that I am using, and want to update my `flour` document with the new brand. While all future recipes would use the new brand, *old recipes would still have used the old brand*. Therefor, I would not want to update any recipes' ingredients if an ingredient was changed.

It occurs to me now that these problems were never really problems, but were actually features of a document data-store over a relational database. I think I just need more time to get into the mindset of working with document data-stores.
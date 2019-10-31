# Bread App

Use data to scientifically iterate your bread recipes and procedures!

---

## Design Doc?

<!-- raison d'être -->

There are a lot of variables to consider when baking your own bread: ingredient ratios, proof time, oven temperature, mixing technique - even whether you add water to flour or add flour to water. Each of these variables can have a significant impact on the final bread. When experimenting with new bread recipes, it is easy to lose track of what changes you have tried and what the result was of that change.

Bread app is a tool that allows you to easily record experiments in bread in a more-or-less scientific way, and to visualize how different ingredients and procedures interact with each-other.


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
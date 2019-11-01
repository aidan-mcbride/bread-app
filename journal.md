# Development Journal

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
* [x] Design doc: describe interactions/flows/features of app (things it will do, high level)
* [x] Design doc: describe technologies that will be used in project and why.

---

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


I found [this excellent article on Dev.to](https://dev.to/guin/a-plan-for-planning-your-first-side-project-2b2l) about planning a side project. I am using it for writing the rest of the design doc.

I moved this dev journal, as well as the design doc, to their own files; the `README` will be a traditional readme with information that is more relevant to the end user and outside parties.

---

#### 11/1/19

> TODO  
> - [x] README-Driven Development: sketch in as much of a README as you can
> - [ ] Prepare python development environment: decide on CI tools, linters, etc. (document in design doc)
> - [ ] Add cards to GitHub project board for REST API
> - [ ] Start coding: TDD based on cards

> **Python tooling:**  
> * https://sourcery.ai/blog/python-best-practices/
> * https://realpython.com/python-continuous-integration
> * https://realpython.com/python-code-quality/
> * https://realpython.com/documenting-python-code/
> * https://realpython.com/python-comments-guide/
> * https://hackernoon.com/setting-up-a-python-development-environment-in-atom-466d7f48e297

Readme template generator: https://github.com/kefranabg/readme-md-generator

There wasn't a whole lot I could add to the readme at this stage. I will add instructions for installing and running as soon as I know how those will be done.


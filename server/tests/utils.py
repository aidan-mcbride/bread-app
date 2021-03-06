import random
import string
from typing import Optional

from pydantic import EmailStr
from starlette.testclient import TestClient

from api import db_ops
from api.database import get_test_db
from api.main import app
from api.schemas.recipe import Ingredient, Procedure, Recipe, RecipeCreate, Unit
from api.schemas.user import UserCreate, UserInDB

client = TestClient(app)

"""
User data for creating a non-random test user
"""
TESTING_USER_EMAIL = "test@example.io"
TESTING_USER_PASSWORD = "password123"


def random_lower_string(length: int = 32) -> str:
    return str().join(random.choices(string.ascii_lowercase, k=length))


def random_email_address() -> str:
    return random_lower_string(random.randint(6, 10)) + "@email.io"


def random_ingredient() -> Ingredient:
    ingredient_names = [
        "flour",
        "water",
        "salt",
        "yeast",
        random_lower_string(length=12),
    ]
    ingredient = Ingredient(
        name=random.choice(ingredient_names),
        quantity=random.uniform(1, 10),
        unit=random.choice(list(Unit)),
    )
    return ingredient


def random_procedure() -> Procedure:
    procedure = Procedure(
        name=random_lower_string(length=12),
        time=random.randint(5, 120),
        temperature=random.randint(10, 600),
        details=random_lower_string(length=random.randint(24, 300)),
    )
    return procedure


def random_recipe() -> RecipeCreate:
    """
    return a randomized recipe as if sent from client
    """
    recipe = RecipeCreate(
        shape=random_lower_string(),
        servings=random.randint(1, 24),
        rating=random.randint(1, 5),
        notes=random_lower_string(length=300),
    )
    for _ in range(random.randint(1, 12)):
        recipe.ingredients.append(random_ingredient())
    for _ in range(random.randint(1, 12)):
        recipe.procedures.append(random_procedure())
    return recipe


def create_random_recipe(creator_id: Optional[int] = None) -> Recipe:
    recipe_in = random_recipe()
    if not creator_id:
        creator_id = create_random_user().id
    db = get_test_db()
    return db_ops.recipes.create(db=db, recipe_in=recipe_in, creator_id=creator_id)


def random_user() -> UserCreate:
    user = UserCreate(email=random_email_address(), password=random_lower_string())
    return user


def create_random_user() -> UserInDB:
    user_in = random_user()
    db = get_test_db()
    return db_ops.users.create(db=db, user_in=user_in)


# ----
def create_test_user():
    user_in = {"email": TESTING_USER_EMAIL, "password": TESTING_USER_PASSWORD}
    return client.post("/users/", json=user_in)


def get_test_user() -> Optional[UserInDB]:
    email = EmailStr(TESTING_USER_EMAIL)
    return db_ops.users.read_by_email(db=get_test_db(), email=email)


def get_test_user_token_headers():
    user_in = {"email": TESTING_USER_EMAIL, "password": TESTING_USER_PASSWORD}
    client.post("/users/", json=user_in)
    # log in and get token
    credentials = {"username": TESTING_USER_EMAIL, "password": TESTING_USER_PASSWORD}
    response = client.post("/login", data=credentials)
    access_token = response.json()["access_token"]
    token_headers = {"Authorization": "Bearer {token}".format(token=access_token)}
    return token_headers

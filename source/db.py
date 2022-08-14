import sqlalchemy as sa
import databases

from source.settings import settings


database = databases.Database(settings.database_url)
metadata = sa.MetaData()

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
    sa.Column("username", sa.String(50), unique=True),
    sa.Column("user_status", sa.String(50)),
    sa.Column("created_at", sa.Date),
    sa.Column("updated_at", sa.Date),
    sa.Column("hashed_password", sa.String),
    sa.Column("recipes_quantity", sa.Integer),
)

recipes = sa.Table(
    "recipes",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("author", sa.Integer, sa.ForeignKey('users.id')),
    sa.Column("created_at", sa.Date),
    sa.Column("updated_at", sa.Date),
    sa.Column("name", sa.String(50)),
    sa.Column("kind", sa.String(50)),
    sa.Column("description", sa.String),
    sa.Column("cooking_steps", sa.String),
    sa.Column("photo", sa.String),
    sa.Column("likes", sa.Integer),
    sa.Column("recipe_status", sa.String(50)),
)

favorites = sa.Table(
    "favorites",
    metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey('users.id')),
    sa.Column("recipe_id", sa.Integer, sa.ForeignKey('recipes.id')),
)

hashtags = sa.Table(
    "hashtags",
    metadata,
    sa.Column("recipe_id", sa.Integer, sa.ForeignKey('recipes.id')),
    sa.Column("hashtag", sa.String(50)),
)


engine = sa.create_engine(settings.database_url, echo=True)
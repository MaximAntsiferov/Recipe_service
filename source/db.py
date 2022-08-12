import sqlalchemy as sa
import databases
from source.settings import settings


database = databases.Database(settings.database_url)
metadata = sa.MetaData()

user = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("nickname", sa.String(50), unique=True),
    sa.Column("status", sa.String(50)),
    sa.Column("created_at", sa.Date),
    sa.Column("updated_at", sa.Date),
)

recipe = sa.Table(
    "recipe",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("author", sa.Integer, sa.ForeignKey('user.id')),
    sa.Column("created_at", sa.Date),
    sa.Column("updated_at", sa.Date),
    sa.Column("name", sa.String(50)),
    sa.Column("kind", sa.String(50)),
    sa.Column("description", sa.String),
    sa.Column("cooking_steps", sa.String),
    sa.Column("photo", sa.String),
    sa.Column("likes", sa.Integer, default=0),
    sa.Column("status", sa.String(50)),
)

favorite = sa.Table(
    "favorite",
    metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey('user.id')),
    sa.Column("recipe_id", sa.Integer, sa.ForeignKey('recipe.id')),
)

hashtag = sa.Table(
    "hashtag",
    metadata,
    sa.Column("recipe_id", sa.Integer, sa.ForeignKey('recipe.id')),
    sa.Column("hashtag", sa.String(50)),
)

engine = sa.create_engine(settings.database_url)
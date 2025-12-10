from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from sqlalchemy.engine.url import make_url

from app.core.database import Base, DATABASE_URL


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Parse the DATABASE_URL to handle the 'schema' parameter
db_url = make_url(DATABASE_URL)
schema_name = db_url.query.get("schema") # Get schema without removing it

if schema_name:
    # If schema is present, set it in the config for use by context.configure
    config.set_main_option("sqlalchemy.default_schema_name", schema_name)

# Create a mutable copy of the query parameters and remove 'schema'
mutable_query = dict(db_url.query)
mutable_query.pop("schema", None)

from sqlalchemy.engine import URL

# Reconstruct the URL without the schema parameter for psycopg2
alembic_config_url = URL.create(
    drivername=db_url.drivername,
    username=db_url.username,
    password=db_url.password,
    host=db_url.host,
    port=db_url.port,
    database=db_url.database,
    query=mutable_query,
).render_as_string(hide_password=False)

config.set_main_option("sqlalchemy.url", str(alembic_config_url).replace("%", "%%"))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

def include_object_for_schema(schema_name):
    def include_object(object, name, type_, reflected, compare_to):
        if type_ == "table" and object.schema != schema_name:
            return False
        return True
    return include_object

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    schema_name = config.get_main_option("sqlalchemy.default_schema_name")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        version_table_schema=schema_name,
        include_object=include_object_for_schema(schema_name) if schema_name else None,
    )

    with context.begin_transaction():
        context.run_migrations()


from sqlalchemy import create_engine


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # Get the modified URL from the config
    url = config.get_main_option("sqlalchemy.url")
    connectable = create_engine(url, poolclass=pool.NullPool)

    schema_name = config.get_main_option("sqlalchemy.default_schema_name")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            version_table_schema=schema_name,
            include_object=include_object_for_schema(schema_name) if schema_name else None,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# Project Commands

This file contains common commands for running and managing the application.

## Running the Application

To run the application, which will use the `PORT` defined in your `.env` file:

```bash
python app/main.py
```

For development with auto-reload, you can still use the `uvicorn` command. Note that this will default to port 8000 unless you specify the port manually.

```bash
uvicorn app.main:app --reload --port 9000
```

## API Documentation (Swagger)

Once the application is running, you can access the automatically generated API documentation.

- **Interactive API Docs (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Schema (JSON):** [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

You can save the `openapi.json` file and import it into API clients like Postman.

## Database Migrations

This project uses Alembic for database migrations.

### Create a new migration

To automatically generate a new migration script based on model changes:

```bash
alembic revision --autogenerate -m "Your migration message"
```

### Apply migrations

To apply all pending migrations to the database:

```bash
alembic upgrade head
```

## Seeding the Database

To populate the database with initial data, run the seed script:

```bash
python scripts/seed.py
```

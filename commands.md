# Project Commands

This file contains common commands for running and managing the application.

## Running the Application

To run the application in development mode with auto-reload:

```bash
uvicorn app.main:app --reload
```

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

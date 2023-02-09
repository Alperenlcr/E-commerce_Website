from app import app
from app.db_models import *
from sqlalchemy import create_engine


@app.cli.command()
def create_database():
    try:
        engine = create_engine('mysql://root:467843.@127.0.0.1')
        with engine.connect() as conn:
            conn.execute(f"CREATE DATABASE IF NOT EXISTS computer_db;")
        print(f"A database named computer_db has been created. Now creates the tables. . .")
    except Exception as e:
        print("Error detail:", e)

    try:
        db.create_all()
        print("All tables created successfully.")
    except Exception as e:
        print("Error detail:", e)
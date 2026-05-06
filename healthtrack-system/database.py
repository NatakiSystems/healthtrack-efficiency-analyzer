# This file handles the connection to the SQLite database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import DBModelBase # Imports the anchor from your models file

# This is the path to your database file
DATABASE_URL = "sqlite:///healthtrack.db"

# The engine is the connection to the database
engine = create_engine(DATABASE_URL)

# This function tells SQLAlchemy to create the tables defined in models.py
def create_db():
    DBModelBase.metadata.create_all(engine)

# This is the "command" that runs the function above
if __name__ == "__main__":
    create_db()

# SessionLocal is how we will open database sessions later
SessionLocal = sessionmaker(bind=engine)
import os
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration from environment variables
# First searches .env file, it not exists then search Docker CI/CD etc...
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Asynchronous database URL for PostgreSQL
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create connection between FastAPI and PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a configured "SessionLocal" class. it will create a new Session object when called.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Creates a new database session for each request and ensures it's closed after the request is done.
def get_db():
    db = SessionLocal() # Create a new database session
    try:
        yield db
    finally:
        db.close()


try:
    with engine.connect() as conn:
        print("Connected successfully")
except Exception as e:
    print(f"Error connecting to the database: {e}")

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database Configuration
DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi_db" # db name = fastapi_db, password = password
engine = create_engine(DATABASE_URL, echo=True) # this creates a database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # this creates a session factory so we can have session in a controlled and transactional manner
#bind=engine - just letting the app know which database our session is connected to
#autoCommit=False - changes we make to the session will not automatically get saved to our database
#autoFlush=False - applies the changes to the database, but they are not yet permanent, allowing us to perform additional steps or checks before finalizing
#session.commit() - makes the changes permanent in the database
Base = declarative_base()  # Create a base class for declarative ORM models
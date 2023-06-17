import sqlalchemy

DATABASE_URL = "mysql://gpttools:password@127.0.0.1:3306/gpttools"

engine = sqlalchemy.create_engine(DATABASE_URL)

Base = sqlalchemy.orm.declarative_base()

SessionLocal = sqlalchemy.orm.sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

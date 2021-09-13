from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Database:
    def __init__(self, database_url, logger):
        self.logger = logger
        self.engine = create_engine(database_url, echo=True)
        session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.session_factory = scoped_session(session_maker)

    def create_database(self, metadata):
        metadata.create_all(self.engine)

    @contextmanager
    def new_session(self):
        session = self.session_factory()
        try:
            yield session
        except Exception:
            self.logger.exception('Session rollback because of exception')
            session.rollback()
            raise
        finally:
            session.close()

import pytest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy.orm.session import Session
import importlib
import sys

DATABASE_MODULE = "app.database"

@pytest.fixture
def mock_settings(monkeypatch):
    """Fixture to mock the settings.DATABASE_URL before app.database is imported."""
    mock_url = "postgresql://user:password@localhost:5432/test_db"
    mock_settings = MagicMock()
    mock_settings.DATABASE_URL = mock_url
    # Ensure 'app.database' is not loaded
    if DATABASE_MODULE in sys.modules:
        del sys.modules[DATABASE_MODULE]
    # Patch settings in 'app.database'
    monkeypatch.setattr(f"{DATABASE_MODULE}.settings", mock_settings)
    return mock_settings

def reload_database_module():
    """Helper function to reload the database module after patches."""
    if DATABASE_MODULE in sys.modules:
        del sys.modules[DATABASE_MODULE]
    return importlib.import_module(DATABASE_MODULE)

def test_base_declaration(mock_settings):
    """Test that Base is an instance of declarative_base."""
    database = reload_database_module()
    Base = database.Base
    assert isinstance(Base, database.declarative_base().__class__)

def test_get_engine_success(mock_settings):
    """Test that get_engine returns a valid engine."""
    database = reload_database_module()
    engine = database.get_engine()
    assert isinstance(engine, Engine)

def test_get_engine_failure(mock_settings):
    """Test that get_engine raises an error if the engine cannot be created."""
    database = reload_database_module()
    with patch("app.database.create_engine", side_effect=SQLAlchemyError("Engine error")):
        with pytest.raises(SQLAlchemyError, match="Engine error"):
            database.get_engine()

def test_get_sessionmaker(mock_settings):
    """Test that get_sessionmaker returns a valid sessionmaker."""
    database = reload_database_module()
    engine = database.get_engine()
    SessionLocal = database.get_sessionmaker(engine)
    assert isinstance(SessionLocal, sessionmaker)


    # Mock the SessionLocal to return a mock session
    mock_session = MagicMock(spec=Session)
    mock_sessionmaker = MagicMock(return_value=mock_session)
    
    with patch.object(database, 'SessionLocal', mock_sessionmaker):
        # Call get_db and iterate through the generator
        db_generator = database.get_db()
        
        # Get the yielded session
        db = next(db_generator)
        
        # Verify we got the mock session
        assert db is mock_session
        
        # Verify SessionLocal was called to create the session
        mock_sessionmaker.assert_called_once()
        
        # Complete the generator to trigger the finally block
        try:
            next(db_generator)
        except StopIteration:
            pass
        
        # Verify the session was closed
        mock_session.close.assert_called_once()

    # Mock the SessionLocal to return a mock session
    mock_session = MagicMock(spec=Session)
    mock_sessionmaker = MagicMock(return_value=mock_session)
    
    with patch.object(database, 'SessionLocal', mock_sessionmaker):
        db_generator = database.get_db()
        
        # Get the yielded session
        db = next(db_generator)
        assert db is mock_session
        
        # Simulate an exception by throwing an error into the generator
        try:
            db_generator.throw(Exception("Test exception"))
        except Exception:
            pass
        
        # Verify the session was still closed despite the exception
        mock_session.close.assert_called_once()

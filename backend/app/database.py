"""CognoDB database connection management using the official Neo4j Python driver."""
import logging
from contextlib import contextmanager
from typing import Generator, Optional

from neo4j import GraphDatabase, Driver, Session
from neo4j.exceptions import ServiceUnavailable, AuthError

from app.config import get_settings

logger = logging.getLogger(__name__)

# Module-level driver singleton — created once, reused for every request.
_driver: Optional[Driver] = None


def get_driver() -> Driver:
    """Return the module-level Neo4j driver, initialising it on first call."""
    global _driver
    if _driver is None:
        settings = get_settings()
        logger.info("Initialising CognoDB driver (uri=%s, user=%s)", settings.cognodb_uri, settings.cognodb_username)
        _driver = GraphDatabase.driver(
            settings.cognodb_uri,
            auth=(settings.cognodb_username, settings.cognodb_password),
            max_connection_pool_size=10,
            connection_timeout=10,
        )
    return _driver


def close_driver() -> None:
    """Close the driver and release all connections."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None
        logger.info("CognoDB driver closed.")


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager that yields a database session and handles cleanup."""
    driver = get_driver()
    with driver.session() as session:
        yield session


def check_connectivity() -> bool:
    """Return True if the database is reachable, False otherwise."""
    try:
        driver = get_driver()
        driver.verify_connectivity()
        return True
    except (ServiceUnavailable, AuthError, Exception) as exc:
        logger.warning("Database connectivity check failed: %s", exc)
        return False

from unittest.mock import MagicMock, patch
import sqlite3

from src.infrastructure.db.connection import get_connection
from src.core.settings                import database_settings


@patch("src.infrastructure.db.connection.sqlite3.connect")
@patch("src.infrastructure.db.connection.Path")
def test_get_connection_unit(PathMock, connect_mock):
    # Arrange
    fake_path = MagicMock()
    fake_parent = MagicMock()

    PathMock.return_value = fake_path
    fake_path.parent = fake_parent

    fake_conn = MagicMock(spec=sqlite3.Connection)
    connect_mock.return_value = fake_conn

    database_settings.SQLITE_DB_PATH = "/fake/path/db.sqlite"

    # Act
    conn = get_connection()

    # Assert: directory creation
    fake_parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    # Assert: sqlite connection
    connect_mock.assert_called_once_with("/fake/path/db.sqlite")

    # Assert: row factory set
    assert conn.row_factory == sqlite3.Row

    # Assert: returned object
    assert conn is fake_conn

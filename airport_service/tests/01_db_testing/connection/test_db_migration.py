import tempfile
from pathlib import Path
from src.infrastructure.db.migrate import run_migrations
from unittest.mock import patch, MagicMock

def test_run_migrations_unit(tmp_path):
    # Create fake SQL files in tmp_path
    sql1 = tmp_path / "001_create_table.sql"
    sql1.write_text("CREATE TABLE test1();")

    sql2 = tmp_path / "002_create_table.sql"
    sql2.write_text("CREATE TABLE test2();")

    with patch("src.infrastructure.db.migrate.get_connection") as mock_get_conn, \
         patch("src.infrastructure.db.migrate.MIGRATIONS_DIR", tmp_path):

        # Mock connection and cursor
        fake_cursor = MagicMock()
        fake_conn = MagicMock()
        fake_conn.cursor.return_value = fake_cursor
        mock_get_conn.return_value = fake_conn

        # Run migrations
        run_migrations()

        # Assert scripts executed
        fake_cursor.executescript.assert_any_call("CREATE TABLE test1();")
        fake_cursor.executescript.assert_any_call("CREATE TABLE test2();")

        # Assert commit & close
        fake_conn.commit.assert_called_once()
        fake_conn.close.assert_called_once()

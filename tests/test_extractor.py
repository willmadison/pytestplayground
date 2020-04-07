import unittest
from yoyo import read_migrations
from yoyo import get_backend
import sqlite3
from extraction import extractor

SQLITE_DB_LOCATION = 'databases/test.db'


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(SQLITE_DB_LOCATION)
        print(sqlite3.version)
    except Exception as e:
        raise e

    return conn


class TestSqlLiteExtraction(unittest.TestCase):
    def setUp(self):
        self.backend = get_backend(f"sqlite:///{SQLITE_DB_LOCATION}")
        self.migrations = read_migrations('./migrations')

        with self.backend.lock():
            self.backend.apply_migrations(self.backend.to_apply(self.migrations))

    def tearDown(self):
        import os
        os.remove(SQLITE_DB_LOCATION)

    def test_it_should_find_users_by_last_name(self):
        conn = create_connection()
        users = extractor.find_users_by_lastname(conn, 'Madison')
        conn.close()
        self.assertEqual(5, len(users), "Expected 5 Users with last_name = Madison")
        users_with_short_first_names = [user for user in users if len(user.first_name) <= 5]
        self.assertEqual(2, len(users_with_short_first_names),
                         "There should only be 2 users with short (i.e. < 6 characters) first names")


if __name__ == '__main__':
    unittest.main()

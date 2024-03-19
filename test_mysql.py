#!/usr/bin/python3
import unittest
import MySQLdb


class TestMySQLInteractions(unittest.TestCase):
    def setUp(self):
        # Connect to the test database
        self.db = MySQLdb.connect(
            host="localhost", user="testuser", passwd="testpass", db="testdb"
        )
        self.cursor = self.db.cursor()

    def tearDown(self):
        # Clean up test data
        self.cursor.execute("DELETE FROM states WHERE name = 'California'")
        self.db.commit()
        self.db.close()

    def test_insert_state(self):
        # Get the initial count of records
        initial_count = self._get_record_count()

        # Insert a new record
        self.cursor.execute("INSERT INTO states (name) VALUES ('California')")
        self.db.commit()

        # Get the count of records after insertion
        final_count = self._get_record_count()

        # Assert that the final count is greater than initial count by 1
        self.assertEqual(final_count, initial_count + 1)

    def _get_record_count(self):
        # Helper method to get the count of records in the states table
        self.cursor.execute("SELECT COUNT(*) FROM states")
        return self.cursor.fetchone()[0]


if __name__ == "__main__":
    unittest.main()

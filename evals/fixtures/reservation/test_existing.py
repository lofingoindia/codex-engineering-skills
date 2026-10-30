import sqlite3
import unittest
from service import initialize, reserve


class ExistingClientTest(unittest.TestCase):
    def test_reserve_and_replay(self):
        conn = sqlite3.connect(':memory:')
        self.addCleanup(conn.close)
        initialize(conn)
        conn.execute("INSERT INTO stock VALUES ('a', 'book', 5)")
        conn.commit()
        first = reserve(conn, 'a', 'request-1', 'book', 2)
        self.assertEqual(first['status'], 201)
        self.assertEqual(first['body']['quantity'], 2)
        self.assertEqual(reserve(conn, 'a', 'request-1', 'book', 2), first)


if __name__ == '__main__':
    unittest.main()

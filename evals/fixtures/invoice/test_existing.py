import sqlite3
import unittest
from service import initialize, patch_invoice


class ExistingClientTest(unittest.TestCase):
    def test_legacy_title_edit(self):
        conn = sqlite3.connect(':memory:')
        self.addCleanup(conn.close)
        initialize(conn)
        conn.execute("INSERT INTO invoices VALUES (1, 'a', 'u', 'Before', 'draft', 1)")
        conn.commit()
        result = patch_invoice(conn, {'tenant_id': 'a', 'user_id': 'u', 'role': 'member'}, 1, {'title': 'After', 'unused': True})
        self.assertEqual(result, {'status': 200, 'body': {'id': 1, 'title': 'After', 'version': 2}, 'headers': {'ETag': '"2"'}})


if __name__ == '__main__':
    unittest.main()

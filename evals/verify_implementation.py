"""Held-out semantic checks for disposable artifacts; executes artifact code.

Concurrency cases use timing-widened stress, not deterministic scheduling.
Run only after an evaluation agent has finished in an isolated environment.

python verify_implementation.py invoice PATH_TO_ARTIFACT
python verify_implementation.py reservation PATH_TO_ARTIFACT
"""
import importlib.util
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest


def load(path):
    spec = importlib.util.spec_from_file_location('evaluated_service', Path(path) / 'service.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def connect(path):
    return sqlite3.connect(path, timeout=10)


class SlowSelectConnection(sqlite3.Connection):
    """Expose read/check/write races by widening the interleaving window."""
    def execute(self, sql, parameters=()):
        cursor = super().execute(sql, parameters)
        if sql.lstrip().upper().startswith('SELECT'):
            time.sleep(0.15)
        return cursor


if len(sys.argv) > 1 and sys.argv[1] == '--worker':
    _, _, kind, module_path, db_path, operation, start = sys.argv
    service = load(module_path)
    conn = sqlite3.connect(db_path, timeout=10, factory=SlowSelectConnection)
    while time.time() < float(start):
        time.sleep(0.005)
    try:
        if kind == 'invoice':
            answer = service.patch_invoice(conn, {'tenant_id': 'a', 'user_id': 'u', 'role': 'member'}, 1, {'title': operation}, '"1"')
        else:
            answer = service.reserve(conn, 'a', operation, 'book', 1)
        print(json.dumps(answer))
    except Exception as exc:
        print(json.dumps({'exception': type(exc).__name__, 'message': str(exc)}))
    finally:
        conn.close()
    raise SystemExit(0)

if len(sys.argv) < 3 or sys.argv[1] not in ('invoice', 'reservation'):
    raise SystemExit('Usage: verify_implementation.py invoice|reservation ARTIFACT [--pattern TEST_NAME]')
kind, artifact = sys.argv[1:3]
pattern = None
if len(sys.argv) > 3:
    if len(sys.argv) != 5 or sys.argv[3] != '--pattern':
        raise SystemExit('Expected --pattern TEST_NAME')
    pattern = sys.argv[4]
service = load(artifact)


class DatabaseCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = str(Path(self.temp.name) / 'fixture.db')
        self.conn = connect(self.path)
        self.addCleanup(self.conn.close)
        service.initialize(self.conn)

    def workers(self, operations):
        start = str(time.time() + 1.5)
        workers = []
        try:
            for operation in operations:
                workers.append(subprocess.Popen(
                    [sys.executable, str(Path(__file__).resolve()), '--worker', kind,
                     str(Path(artifact).resolve()), self.path, operation, start],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8'))
            results = []
            for worker in workers:
                stdout, stderr = worker.communicate(timeout=20)
                self.assertEqual(worker.returncode, 0, stderr)
                results.append(json.loads(stdout))
            return results
        finally:
            # These are owned worker processes, including siblings after a failed wait.
            for worker in workers:
                if worker.poll() is None:
                    worker.terminate()
            for worker in workers:
                try:
                    worker.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    worker.kill()
                    worker.communicate()



class InvoiceChecks(DatabaseCase):
    def setUp(self):
        super().setUp()
        self.conn.execute("INSERT INTO invoices VALUES (1, 'a', 'u', 'Before', 'draft', 1)")
        self.conn.commit()
        self.actor = {'tenant_id': 'a', 'user_id': 'u', 'role': 'member'}

    def row(self):
        return self.conn.execute('SELECT tenant_id, owner_id, title, status, version FROM invoices WHERE id=1').fetchone()

    def test_legacy_response_and_unknown_field(self):
        result = service.patch_invoice(self.conn, self.actor, 1, {'title': 'After', 'ignored': 10})
        self.assertEqual(result, {'status': 200, 'body': {'id': 1, 'title': 'After', 'version': 2}, 'headers': {'ETag': '"2"'}})

    def test_tenant_and_object_permissions_have_no_effects(self):
        before = self.row()
        for tenant, user, role in [('b', 'u', 'admin'), ('a', 'another', 'member')]:
            result = service.patch_invoice(self.conn, {'tenant_id': tenant, 'user_id': user, 'role': role}, 1, {'title': 'Forbidden'})
            self.assertIn(result['status'], [403, 404])
            self.assertEqual(self.row(), before)

    def test_same_tenant_admin(self):
        result = service.patch_invoice(self.conn, {'tenant_id': 'a', 'user_id': 'admin', 'role': 'admin'}, 1, {'title': 'Approved'})
        self.assertEqual(result['status'], 200)

    def test_protected_fields_ignored(self):
        result = service.patch_invoice(self.conn, self.actor, 1, {'title': 'After', 'tenant_id': 'b', 'owner_id': 'attacker', 'status': 'paid', 'version': 900})
        self.assertEqual(result['status'], 200)
        self.assertEqual(self.row(), ('a', 'u', 'After', 'draft', 2))

    def test_invalid_inputs_and_validators_have_no_effects(self):
        before = self.row()
        for body in [None, [], {}, {'title': None}, {'title': True}, {'title': ' '}, {'title': 'x' * 121}]:
            self.assertEqual(service.patch_invoice(self.conn, self.actor, 1, body)['status'], 400)
            self.assertEqual(self.row(), before)
        for etag in ['"0"', 'W/"1"', '1', '*', '"1", "2"']:
            self.assertIn(service.patch_invoice(self.conn, self.actor, 1, {'title': 'After'}, etag)['status'], [400, 412])
            self.assertEqual(self.row(), before)

    def test_separate_processes_one_etag_winner(self):
        results = self.workers(['Edit-' + str(i) for i in range(8)])
        self.assertEqual(sum(x.get('status') == 200 for x in results), 1, results)
        self.assertEqual(sum(x.get('status') == 412 for x in results), 7, results)
        self.assertEqual(self.row()[4], 2)


class ReservationChecks(DatabaseCase):
    def setUp(self):
        super().setUp()
        self.conn.executemany('INSERT INTO stock VALUES (?, ?, ?)', [('a', 'book', 5), ('a', 'pen', 5), ('b', 'book', 5)])
        self.conn.commit()

    def effects(self):
        return self.conn.execute('SELECT COUNT(*) FROM reservations').fetchone()[0], self.conn.execute("SELECT available FROM stock WHERE tenant_id='a' AND sku='book'").fetchone()[0]

    def test_replay_after_connection_restart(self):
        first = service.reserve(self.conn, 'a', 'key', 'book', 2)
        with closing(connect(self.path)) as another, another:
            second = service.reserve(another, 'a', 'key', 'book', 2)
        self.assertEqual(first, second)
        self.assertEqual(first['status'], 201)
        self.assertEqual(self.effects(), (1, 3))

    def test_payload_binding(self):
        service.reserve(self.conn, 'a', 'key', 'book', 1)
        for sku, quantity in [('pen', 1), ('book', 2)]:
            self.assertEqual(service.reserve(self.conn, 'a', 'key', sku, quantity)['status'], 409)
        self.assertEqual(self.effects(), (1, 4))

    def test_tenant_key_isolation(self):
        a = service.reserve(self.conn, 'a', 'key', 'book', 1)
        b = service.reserve(self.conn, 'b', 'key', 'book', 1)
        self.assertEqual(a['status'], 201)
        self.assertEqual(b['status'], 201)
        self.assertNotEqual(a['body']['reservationId'], b['body']['reservationId'])

    def test_validation_no_effects(self):
        for key, sku, quantity in [('', 'book', 1), ('x'*129, 'book', 1), ('k', '', 1), ('k', 'x'*65, 1), ('k', 'book', 0), ('k', 'book', -1), ('k', 'book', True), ('k', 'book', 1.5), ('k', 'book', '1')]:
            self.assertEqual(service.reserve(self.conn, 'a', key, sku, quantity)['status'], 400)
            self.assertEqual(self.effects(), (0, 5))

    def test_insufficient_stock_no_effects(self):
        self.assertEqual(service.reserve(self.conn, 'a', 'key', 'book', 6)['status'], 409)
        self.assertEqual(self.effects(), (0, 5))

    def test_concurrent_same_key_single_effect(self):
        results = self.workers(['same-key'] * 8)
        self.assertTrue(all(x.get('status') == 201 for x in results), results)
        self.assertTrue(all(x == results[0] for x in results), results)
        self.assertEqual(self.effects(), (1, 4))

    def test_concurrent_distinct_keys_stock_invariant(self):
        results = self.workers(['key-' + str(i) for i in range(8)])
        self.assertEqual(sum(x.get('status') == 201 for x in results), 5, results)
        self.assertEqual(sum(x.get('status') == 409 for x in results), 3, results)
        self.assertEqual(self.effects(), (5, 0))


selected = InvoiceChecks if kind == 'invoice' else ReservationChecks
suite = (unittest.TestSuite([selected(pattern)]) if pattern else unittest.defaultTestLoader.loadTestsFromTestCase(selected))
result = unittest.TextTestRunner(verbosity=2).run(suite)
print(json.dumps({'kind': kind, 'tests': result.testsRun, 'failures': len(result.failures), 'errors': len(result.errors), 'pass': result.wasSuccessful()}))
raise SystemExit(0 if result.wasSuccessful() else 1)

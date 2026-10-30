import sqlite3


def initialize(conn):
    conn.execute('CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, tenant_id TEXT NOT NULL, owner_id TEXT NOT NULL, title TEXT NOT NULL, status TEXT NOT NULL, version INTEGER NOT NULL)')
    conn.commit()


def response(status, body, headers=None):
    return {'status': status, 'body': body, 'headers': headers or {}}


def patch_invoice(conn, actor, invoice_id, body, if_match=None):
    row = conn.execute('SELECT id, tenant_id, owner_id, title, status, version FROM invoices WHERE id = ?', (invoice_id,)).fetchone()
    if row is None:
        return response(404, {'code': 'not_found', 'message': 'Invoice not found'})
    if not isinstance(body, dict) or not isinstance(body.get('title'), str) or not body['title'].strip() or len(body['title']) > 120:
        return response(400, {'code': 'invalid_input', 'message': 'Invalid title'})
    if if_match is not None and if_match != '"' + str(row[5]) + '"':
        return response(412, {'code': 'precondition_failed', 'message': 'Invoice changed'})
    changes = {k: v for k, v in body.items() if k in {'title', 'status', 'tenant_id', 'owner_id'}}
    fields = ', '.join(k + ' = ?' for k in changes)
    conn.execute('UPDATE invoices SET ' + fields + ', version = version + 1 WHERE id = ?', (*changes.values(), invoice_id))
    conn.commit()
    updated = conn.execute('SELECT title, version FROM invoices WHERE id = ?', (invoice_id,)).fetchone()
    return response(200, {'id': invoice_id, 'title': updated[0], 'version': updated[1]}, {'ETag': '"' + str(updated[1]) + '"'})

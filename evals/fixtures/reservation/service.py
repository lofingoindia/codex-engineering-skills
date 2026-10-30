import json


def initialize(conn):
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS stock (tenant_id TEXT, sku TEXT, available INTEGER NOT NULL, PRIMARY KEY (tenant_id, sku));
        CREATE TABLE IF NOT EXISTS reservations (id INTEGER PRIMARY KEY AUTOINCREMENT, tenant_id TEXT NOT NULL, sku TEXT NOT NULL, quantity INTEGER NOT NULL);
        CREATE TABLE IF NOT EXISTS requests (tenant_id TEXT NOT NULL, key TEXT NOT NULL, fingerprint TEXT NOT NULL, response TEXT NOT NULL, PRIMARY KEY (tenant_id, key));
    ''')
    conn.commit()


def reserve(conn, tenant_id, key, sku, quantity):
    fingerprint = json.dumps([sku, quantity])
    saved = conn.execute('SELECT fingerprint, response FROM requests WHERE tenant_id = ? AND key = ?', (tenant_id, key)).fetchone()
    if saved:
        return json.loads(saved[1])
    stock = conn.execute('SELECT available FROM stock WHERE tenant_id = ? AND sku = ?', (tenant_id, sku)).fetchone()
    if stock is None or stock[0] < quantity:
        return {'status': 409, 'body': {'code': 'out_of_stock', 'message': 'Insufficient stock'}}
    conn.execute('UPDATE stock SET available = available - ? WHERE tenant_id = ? AND sku = ?', (quantity, tenant_id, sku))
    cursor = conn.execute('INSERT INTO reservations (tenant_id, sku, quantity) VALUES (?, ?, ?)', (tenant_id, sku, quantity))
    conn.commit()
    result = {'status': 201, 'body': {'reservationId': cursor.lastrowid, 'sku': sku, 'quantity': quantity}}
    conn.execute('INSERT INTO requests VALUES (?, ?, ?, ?)', (tenant_id, key, fingerprint, json.dumps(result)))
    conn.commit()
    return result

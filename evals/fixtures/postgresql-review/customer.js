export async function getOrCreateCustomer(pool, tenantId, email, displayName) {
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    await client.query("SELECT set_config('app.tenant_id', $1, false)", [tenantId]);
    const result = await pool.query(`
      WITH inserted AS (
        INSERT INTO customers (tenant_id, email, display_name)
        VALUES ($1, $2, $3)
        ON CONFLICT (tenant_id, email) DO NOTHING
        RETURNING id
      )
      SELECT id FROM inserted
      UNION ALL
      SELECT id FROM customers WHERE tenant_id = $1 AND email = $2
      LIMIT 1
    `, [tenantId, email, displayName]);
    await client.query('COMMIT');
    return result.rows[0]?.id;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}

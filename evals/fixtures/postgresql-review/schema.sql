CREATE ROLE app_runtime LOGIN;
CREATE TABLE customers (
  id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  tenant_id uuid NOT NULL,
  email text NOT NULL,
  display_name text NOT NULL,
  UNIQUE (tenant_id, email)
);
ALTER TABLE customers OWNER TO app_runtime;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_customers ON customers
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);

# Invoice API fixture

This disposable Python/SQLite module represents a framework-independent HTTP handler. There is no production access and no third-party dependency.

Run local tests with `python -m unittest discover -v`. Identity is already verified by middleware. Actor contains tenant_id, user_id, and role (member/admin). Members may edit their own invoice only; admins may edit any invoice within their tenant. Object IDs are global here. Only title is writable through this operation; other fields are ignored for compatibility. Title must be a nonblank string at most 120 characters. Preserve the existing response object with status, body and headers and the error envelope {code,message}.

The optional If-Match argument is a strong quoted integer ETag. A supplied stale/invalid validator must not mutate state. Legacy callers omitting it must still be able to edit. A valid supplied version is a concurrency precondition: at most one edit based on that version can win. A successful edit increments version and returns the current ETag. Keep schema and signature unchanged. Do not modify this policy file.

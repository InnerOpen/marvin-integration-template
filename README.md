# marvin-integration-template

A copyable skeleton for building a [Marvin](https://claude.ai/code) integration. Clone it, rename,
implement, publish — an installed Marvin discovers your provider through its `marvin.integrations`
entry point, with **no changes to Marvin core or its frontend**.

## Make your own

1. **Copy** this repo and rename:
   - distribution: `marvin-integration-example` → `marvin-integration-<service>`
   - package dir: `src/marvin_integration_example/` → `src/marvin_integration_<service>/`
   - provider: `ExampleProvider` / `slug = "example"` → your names
2. **Point the entry point** at your class in `pyproject.toml`:
   ```toml
   [project.entry-points."marvin.integrations"]
   <service> = "marvin_integration_<service>:<Service>Provider"
   ```
3. **Implement** `provider.py`:
   - `category` — `source` (pulls content in), `destination` (reacts on publish), `notify`, `capability`
   - `credentials` — what secret(s) the create form asks for (stored securely; you receive the value as `ctx.secret`)
   - `config_schema` — JSON schema for non-secret settings; the form is generated from it
   - `check()` — health probe → `(status, error)`
   - `run_action()` — outbound actions; return a result dict
   - `poll()` / `on_webhook()` — for sources: return `PolledEvent`s; the core dispatches them
4. **Test** (`uv run --extra dev pytest`) — your provider depends only on `marvin-integration-sdk`,
   so tests run without Marvin.
5. **Publish**, then on a Marvin host: `uv pip install marvin-integration-<service>` → restart → done.

## The contract in one screen

```python
from marvin_integration_sdk import (
    CATEGORY_DESTINATION,
    CredentialField,
    ProviderAction,
    IntegrationProvider,
    register_provider,
)


@register_provider
class MyProvider(IntegrationProvider):
    slug = "my_service"
    name = "My Service"
    category = CATEGORY_DESTINATION
    credentials = (CredentialField(key="api_key", label="API Key"),)
    actions = (ProviderAction(key="ping", label="Ping"),)

    def check(self, ctx):  # ctx has: config, secret, logger, http
        r = ctx.http.get("https://api.example.com/health")
        return ("ok", None) if r.ok else ("error", f"HTTP {r.status_code}")

    def run_action(self, key, args, ctx):
        r = ctx.http.post("https://api.example.com/ping", json=args)
        return {"status": r.status_code}
```

`ctx.http` is the core-supplied client (timeouts, size cap, SSRF guard) — prefer it over rolling
your own. See `marvin-integration-slack` for a real, published example.

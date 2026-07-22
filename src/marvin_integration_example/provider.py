"""Template provider. Copy this file, rename the class/slug, and implement your logic.

A provider is pure with respect to Marvin: it gets ``config``, the resolved ``secret``, a ``logger``,
and a safe ``http`` client via ``ctx``, and it returns results/events. It never touches the database
or the event bus — the core owns persistence and dispatch.
"""

from marvin_integration_sdk import (
    CATEGORY_DESTINATION,
    CredentialField,
    IntegrationContext,
    IntegrationProvider,
    ProviderAction,
    register_provider,
)


@register_provider
class ExampleProvider(IntegrationProvider):
    # --- identity (change these) ---
    slug = "example"  # unique key; the automation/action reference
    name = "Example Integration"
    description = "A starting point — copy this package, rename it, and implement your provider."
    category = CATEGORY_DESTINATION  # source | destination | capability | notify

    # --- what the create form asks for ---
    credentials = (CredentialField(key="api_key", label="API Key", help="Your service's API key."),)
    config_schema = {
        "type": "object",
        "properties": {"base_url": {"type": "string", "format": "uri", "title": "Base URL"}},
        "required": ["base_url"],
        "additionalProperties": False,
    }

    # --- what it can do ---
    actions = (
        ProviderAction(
            key="ping",
            label="Ping",
            description="Call the base URL and report the HTTP status.",
            input_schema={"type": "object", "properties": {}, "additionalProperties": False},
        ),
    )

    def check(self, ctx: IntegrationContext) -> tuple[str, str | None]:
        base = (ctx.config or {}).get("base_url")
        if not base:
            return ("unconfigured", "Missing base URL.")
        try:
            resp = ctx.http.get(base)
        except Exception as e:  # noqa: BLE001
            return ("error", str(e))
        return ("ok", None) if resp.ok else ("error", f"HTTP {resp.status_code}")

    def run_action(self, key: str, args: dict, ctx: IntegrationContext) -> dict:
        if key != "ping":
            raise NotImplementedError(f"example has no action '{key}'")
        base = (ctx.config or {}).get("base_url")
        if not base:
            raise ValueError("No base URL configured.")
        resp = ctx.http.get(base)
        return {"status_code": resp.status_code}

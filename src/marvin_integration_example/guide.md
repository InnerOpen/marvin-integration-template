# Example Integration

<!-- Your integration's how-to (SDK 0.9.0). Marvin's agents read it when they build workflows in a workspace where
this integration is connected, and Marvin's manual search finds it. Write it for a person; keep it under 16 KB. -->

Calls your service's base URL and reports the HTTP status — a starting point for your own integration.

## Connect it

1. In your service, create an API key.
2. In Marvin: **Settings → Integrations → Example Integration**, set **Base URL** and paste the key.

## Actions

- **Ping** (`ping`) — calls the base URL; the output is `{status_code}`.

## What it can't do

Say plainly what people might expect and won't get.

## When it fails

List the errors people will see and what each means.

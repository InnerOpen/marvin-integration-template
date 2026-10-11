"""The SDK's conformance kit (marvin_integration_sdk.testing): what Marvin relies on, checked without Marvin —
the catalog entry serialises, keys are unique, recipes are well formed, the guide loads. Keep it when you copy."""

import pytest
from marvin_integration_sdk.testing import IntegrationContract

from marvin_integration_example import ExampleProvider


class TestExampleContract(IntegrationContract):
    @pytest.fixture
    def provider(self):
        return ExampleProvider()

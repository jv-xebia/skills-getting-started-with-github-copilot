from copy import deepcopy
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Provide a TestClient and restore in-memory state after each test.

    Uses AAA pattern in tests; this fixture ensures tests are isolated by
    deep-copying and restoring `src.app.activities`.
    """
    import importlib
    app_module = importlib.import_module('src.app')

    # Arrange: snapshot current activities
    original = deepcopy(app_module.activities)

    # Act: create TestClient
    client = TestClient(app_module.app)

    try:
        yield client
    finally:
        # Assert/Teardown: restore original activities to avoid cross-test state
        app_module.activities = original

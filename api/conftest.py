"""
Pytest fixtures for API tests.
"""
import pytest
import random
from api.pet_client import PetClient, create_pet_payload


@pytest.fixture(scope="session")
def pet_client():
    """Create a PetClient instance for the test session."""
    return PetClient()


@pytest.fixture
def unique_pet_id():
    """Generate a unique pet ID for testing."""
    return random.randint(100000, 999999)


@pytest.fixture
def sample_pet(unique_pet_id):
    """Create a sample pet payload."""
    return create_pet_payload(
        pet_id=unique_pet_id,
        name="TestDog",
        status="available",
        category_id=1,
        category_name="Dogs"
    )


@pytest.fixture
def created_pet(pet_client, sample_pet):
    """Create a pet and return it for testing. Cleanup after test."""
    response = pet_client.add_pet(sample_pet)
    assert response.status_code == 200
    pet_data = response.json()
    
    yield pet_data
    
    # Cleanup: Delete the pet after test
    try:
        pet_client.delete_pet(pet_data["id"])
    except Exception:
        pass  # Ignore cleanup errors


@pytest.fixture
def pet_statuses():
    """Valid pet statuses."""
    return ["available", "pending", "sold"]

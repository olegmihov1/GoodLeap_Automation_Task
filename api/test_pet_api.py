"""
API Tests for Swagger Petstore - Pet Endpoints.

Test Coverage:
- POST /pet - Create a new pet
- GET /pet/{petId} - Get pet by ID
- PUT /pet - Update an existing pet
- DELETE /pet/{petId} - Delete a pet
- GET /pet/findByStatus - Find pets by status
- POST /pet/{petId} - Update pet with form data

Target API: https://petstore.swagger.io/
"""
import pytest
import random
from api.pet_client import PetClient, create_pet_payload


class TestCreatePet:
    """Tests for POST /pet - Add a new pet."""
    
    @pytest.mark.api
    @pytest.mark.critical
    def test_create_pet_success(self, pet_client: PetClient, unique_pet_id):
        """
        Test: Successfully create a new pet.
        
        Steps:
        1. Send POST /pet with valid pet data
        
        Expected: 200 OK with pet data returned.
        """
        pet_data = create_pet_payload(
            pet_id=unique_pet_id,
            name="Buddy",
            status="available"
        )
        
        response = pet_client.add_pet(pet_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == unique_pet_id
        assert response_data["name"] == "Buddy"
        assert response_data["status"] == "available"
        
        # Cleanup
        pet_client.delete_pet(unique_pet_id)
    
    @pytest.mark.api
    def test_create_pet_with_all_fields(self, pet_client: PetClient, unique_pet_id):
        """
        Test: Create pet with all optional fields.
        
        Steps:
        1. Send POST /pet with complete pet data including tags and photos
        
        Expected: 200 OK with all fields returned.
        """
        pet_data = create_pet_payload(
            pet_id=unique_pet_id,
            name="Max",
            status="pending",
            category_id=2,
            category_name="Cats",
            photo_urls=["https://example.com/cat1.jpg", "https://example.com/cat2.jpg"],
            tags=[{"id": 1, "name": "cute"}, {"id": 2, "name": "playful"}]
        )
        
        response = pet_client.add_pet(pet_data)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["category"]["name"] == "Cats"
        assert len(response_data["photoUrls"]) == 2
        assert len(response_data["tags"]) == 2
        
        # Cleanup
        pet_client.delete_pet(unique_pet_id)
    
    @pytest.mark.api
    def test_create_pet_status_sold(self, pet_client: PetClient, unique_pet_id):
        """
        Test: Create pet with 'sold' status.
        
        Expected: Pet created with status 'sold'.
        """
        pet_data = create_pet_payload(
            pet_id=unique_pet_id,
            name="Charlie",
            status="sold"
        )
        
        response = pet_client.add_pet(pet_data)
        
        assert response.status_code == 200
        assert response.json()["status"] == "sold"
        
        # Cleanup
        pet_client.delete_pet(unique_pet_id)
    
    @pytest.mark.api
    def test_create_pet_minimal_data(self, pet_client: PetClient):
        """
        Test: Create pet with minimal required data.
        
        Expected: Pet created successfully.
        """
        pet_id = random.randint(100000, 999999)
        minimal_pet = {
            "id": pet_id,
            "name": "SimplePet",
            "photoUrls": []
        }
        
        response = pet_client.add_pet(minimal_pet)
        
        assert response.status_code == 200
        assert response.json()["name"] == "SimplePet"
        
        # Cleanup
        pet_client.delete_pet(pet_id)


class TestGetPet:
    """Tests for GET /pet/{petId} - Find pet by ID."""
    
    @pytest.mark.api
    @pytest.mark.critical
    def test_get_pet_by_id_success(self, pet_client: PetClient, created_pet):
        """
        Test: Get existing pet by ID.
        
        Steps:
        1. Create a pet (via fixture)
        2. GET /pet/{petId}
        
        Expected: 200 OK with correct pet data.
        """
        pet_id = created_pet["id"]
        
        response = pet_client.get_pet_by_id(pet_id)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["id"] == pet_id
        assert response_data["name"] == created_pet["name"]
    
    @pytest.mark.api
    @pytest.mark.critical
    def test_get_pet_not_found(self, pet_client: PetClient):
        """
        Test: Get non-existent pet.
        
        Steps:
        1. GET /pet/{non-existent-id}
        
        Expected: 404 Not Found.
        """
        non_existent_id = 99999999999
        
        response = pet_client.get_pet_by_id(non_existent_id)
        
        assert response.status_code == 404
    
    @pytest.mark.api
    def test_get_pet_invalid_id(self, pet_client: PetClient):
        """
        Test: Get pet with invalid ID format.
        
        Steps:
        1. GET /pet/invalid-string
        
        Expected: 400 or 404 error.
        """
        # Using string "invalid" as ID
        response = pet_client.session.get(f"{pet_client.BASE_URL}/pet/invalid")
        
        # API returns 404 for invalid format
        assert response.status_code in [400, 404]


class TestUpdatePet:
    """Tests for PUT /pet - Update an existing pet."""
    
    @pytest.mark.api
    @pytest.mark.critical
    def test_update_pet_name(self, pet_client: PetClient, created_pet):
        """
        Test: Update pet name.
        
        Steps:
        1. Create a pet (via fixture)
        2. Update pet with new name
        3. Verify update
        
        Expected: Pet name is updated.
        """
        updated_pet = created_pet.copy()
        updated_pet["name"] = "UpdatedBuddy"
        
        response = pet_client.update_pet(updated_pet)
        
        assert response.status_code == 200
        assert response.json()["name"] == "UpdatedBuddy"
        
        # Verify by getting the pet
        verify_response = pet_client.get_pet_by_id(created_pet["id"])
        assert verify_response.json()["name"] == "UpdatedBuddy"
    
    @pytest.mark.api
    @pytest.mark.critical
    def test_update_pet_status(self, pet_client: PetClient, created_pet):
        """
        Test: Update pet status.
        
        Steps:
        1. Create an 'available' pet
        2. Update status to 'sold'
        
        Expected: Status is updated to 'sold'.
        """
        updated_pet = created_pet.copy()
        updated_pet["status"] = "sold"
        
        response = pet_client.update_pet(updated_pet)
        
        assert response.status_code == 200
        assert response.json()["status"] == "sold"
    
    @pytest.mark.api
    def test_update_pet_category(self, pet_client: PetClient, created_pet):
        """
        Test: Update pet category.
        
        Steps:
        1. Create a pet with category 'Dogs'
        2. Update category to 'Cats'
        
        Expected: Category is updated.
        """
        updated_pet = created_pet.copy()
        updated_pet["category"] = {"id": 3, "name": "Birds"}
        
        response = pet_client.update_pet(updated_pet)
        
        assert response.status_code == 200
        assert response.json()["category"]["name"] == "Birds"


class TestDeletePet:
    """Tests for DELETE /pet/{petId} - Delete a pet."""
    
    @pytest.mark.api
    @pytest.mark.critical
    def test_delete_pet_success(self, pet_client: PetClient, sample_pet):
        """
        Test: Successfully delete a pet.
        
        Steps:
        1. Create a pet
        2. Delete the pet
        3. Verify deletion
        
        Expected: Pet is deleted (404 on subsequent GET).
        """
        # Create pet first
        create_response = pet_client.add_pet(sample_pet)
        assert create_response.status_code == 200
        pet_id = create_response.json()["id"]
        
        # Delete the pet
        delete_response = pet_client.delete_pet(pet_id)
        assert delete_response.status_code == 200
        
        # Verify deletion
        get_response = pet_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 404
    
    @pytest.mark.api
    def test_delete_pet_not_found(self, pet_client: PetClient):
        """
        Test: Delete non-existent pet.
        
        Expected: 404 Not Found.
        """
        response = pet_client.delete_pet(99999999999)
        
        assert response.status_code == 404
    
    @pytest.mark.api
    def test_delete_pet_with_api_key(self, pet_client: PetClient, sample_pet):
        """
        Test: Delete pet with API key header.
        
        Steps:
        1. Create a pet
        2. Delete with api_key header
        
        Expected: Pet is deleted successfully.
        """
        create_response = pet_client.add_pet(sample_pet)
        pet_id = create_response.json()["id"]
        
        delete_response = pet_client.delete_pet(pet_id, api_key="special-key")
        
        assert delete_response.status_code == 200


class TestFindPetsByStatus:
    """Tests for GET /pet/findByStatus - Find pets by status."""
    
    @pytest.mark.api
    @pytest.mark.critical
    def test_find_pets_by_status_available(self, pet_client: PetClient):
        """
        Test: Find all available pets.
        
        Steps:
        1. GET /pet/findByStatus?status=available
        
        Expected: Returns list of pets with status 'available'.
        """
        response = pet_client.find_pets_by_status(["available"])
        
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
        # Verify all returned pets have correct status
        for pet in pets[:10]:  # Check first 10
            if "status" in pet:
                assert pet["status"] == "available"
    
    @pytest.mark.api
    def test_find_pets_by_status_pending(self, pet_client: PetClient):
        """
        Test: Find all pending pets.
        
        Expected: Returns list of pets with status 'pending'.
        """
        response = pet_client.find_pets_by_status(["pending"])
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    @pytest.mark.api
    def test_find_pets_by_status_sold(self, pet_client: PetClient):
        """
        Test: Find all sold pets.
        
        Expected: Returns list of pets with status 'sold'.
        """
        response = pet_client.find_pets_by_status(["sold"])
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    @pytest.mark.api
    def test_find_pets_by_multiple_statuses(self, pet_client: PetClient):
        """
        Test: Find pets by multiple statuses.
        
        Steps:
        1. GET /pet/findByStatus?status=available&status=pending
        
        Expected: Returns pets with either status.
        """
        response = pet_client.find_pets_by_status(["available", "pending"])
        
        assert response.status_code == 200
        pets = response.json()
        assert isinstance(pets, list)
    
    @pytest.mark.api
    def test_find_pets_invalid_status(self, pet_client: PetClient):
        """
        Test: Find pets with invalid status.
        
        Expected: Returns empty list or error.
        """
        response = pet_client.find_pets_by_status(["invalid_status"])
        
        # API may return empty list or error for invalid status
        assert response.status_code in [200, 400]


class TestUpdatePetWithForm:
    """Tests for POST /pet/{petId} - Update pet with form data."""
    
    @pytest.mark.api
    def test_update_pet_name_with_form(self, pet_client: PetClient, created_pet):
        """
        Test: Update pet name using form data.
        
        Steps:
        1. POST /pet/{petId} with name in form data
        
        Expected: Pet name is updated.
        """
        response = pet_client.update_pet_with_form(
            pet_id=created_pet["id"],
            name="FormUpdatedName"
        )
        
        assert response.status_code == 200
    
    @pytest.mark.api
    def test_update_pet_status_with_form(self, pet_client: PetClient, created_pet):
        """
        Test: Update pet status using form data.
        
        Steps:
        1. POST /pet/{petId} with status in form data
        
        Expected: Pet status is updated.
        """
        response = pet_client.update_pet_with_form(
            pet_id=created_pet["id"],
            status="pending"
        )
        
        assert response.status_code == 200
    
    @pytest.mark.api
    def test_update_nonexistent_pet_with_form(self, pet_client: PetClient):
        """
        Test: Update non-existent pet with form.
        
        Expected: 404 Not Found.
        """
        response = pet_client.update_pet_with_form(
            pet_id=99999999999,
            name="Ghost"
        )
        
        assert response.status_code == 404


class TestPetApiEdgeCases:
    """Edge case and boundary tests for Pet API."""
    
    @pytest.mark.api
    def test_create_pet_with_special_characters_name(self, pet_client: PetClient):
        """
        Test: Create pet with special characters in name.
        """
        pet_id = random.randint(100000, 999999)
        pet_data = create_pet_payload(
            pet_id=pet_id,
            name="Buddy's Pet #1!",
            status="available"
        )
        
        response = pet_client.add_pet(pet_data)
        
        assert response.status_code == 200
        pet_client.delete_pet(pet_id)
    
    @pytest.mark.api
    def test_create_pet_with_unicode_name(self, pet_client: PetClient):
        """
        Test: Create pet with unicode characters in name.
        """
        pet_id = random.randint(100000, 999999)
        pet_data = create_pet_payload(
            pet_id=pet_id,
            name="Собака",  # Russian for "dog"
            status="available"
        )
        
        response = pet_client.add_pet(pet_data)
        
        assert response.status_code == 200
        pet_client.delete_pet(pet_id)
    
    @pytest.mark.api
    def test_create_pet_with_long_name(self, pet_client: PetClient):
        """
        Test: Create pet with very long name.
        """
        pet_id = random.randint(100000, 999999)
        long_name = "A" * 500
        pet_data = create_pet_payload(
            pet_id=pet_id,
            name=long_name,
            status="available"
        )
        
        response = pet_client.add_pet(pet_data)
        
        assert response.status_code == 200
        pet_client.delete_pet(pet_id)
    
    @pytest.mark.api
    def test_concurrent_pet_operations(self, pet_client: PetClient):
        """
        Test: Create and immediately get a pet.
        Verifies data consistency.
        """
        pet_id = random.randint(100000, 999999)
        pet_data = create_pet_payload(
            pet_id=pet_id,
            name="ConcurrencyTest",
            status="available"
        )
        
        # Create
        create_response = pet_client.add_pet(pet_data)
        assert create_response.status_code == 200
        
        # Immediately get
        get_response = pet_client.get_pet_by_id(pet_id)
        assert get_response.status_code == 200
        assert get_response.json()["name"] == "ConcurrencyTest"
        
        # Cleanup
        pet_client.delete_pet(pet_id)

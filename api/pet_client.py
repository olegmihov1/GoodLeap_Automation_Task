"""
Pet API Client for Swagger Petstore.
Handles all HTTP requests to Pet endpoints.
"""
import requests
from typing import Optional, List, Dict, Any


class PetClient:
    """Client for interacting with Petstore Pet API endpoints."""
    
    BASE_URL = "https://petstore.swagger.io/v2"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    # ============== Pet Endpoints ==============
    
    def add_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """
        POST /pet - Add a new pet to the store.
        
        Args:
            pet_data: Pet object with id, name, category, photoUrls, tags, status
        """
        return self.session.post(f"{self.BASE_URL}/pet", json=pet_data)
    
    def update_pet(self, pet_data: Dict[str, Any]) -> requests.Response:
        """
        PUT /pet - Update an existing pet.
        
        Args:
            pet_data: Updated pet object
        """
        return self.session.put(f"{self.BASE_URL}/pet", json=pet_data)
    
    def get_pet_by_id(self, pet_id: int) -> requests.Response:
        """
        GET /pet/{petId} - Find pet by ID.
        
        Args:
            pet_id: ID of pet to retrieve
        """
        return self.session.get(f"{self.BASE_URL}/pet/{pet_id}")
    
    def delete_pet(self, pet_id: int, api_key: Optional[str] = None) -> requests.Response:
        """
        DELETE /pet/{petId} - Delete a pet.
        
        Args:
            pet_id: Pet ID to delete
            api_key: Optional API key header
        """
        headers = {}
        if api_key:
            headers["api_key"] = api_key
        return self.session.delete(f"{self.BASE_URL}/pet/{pet_id}", headers=headers)
    
    def find_pets_by_status(self, status: List[str]) -> requests.Response:
        """
        GET /pet/findByStatus - Find pets by status.
        
        Args:
            status: List of statuses (available, pending, sold)
        """
        params = {"status": status}
        return self.session.get(f"{self.BASE_URL}/pet/findByStatus", params=params)
    
    def find_pets_by_tags(self, tags: List[str]) -> requests.Response:
        """
        GET /pet/findByTags - Find pets by tags.
        
        Args:
            tags: List of tag names
        """
        params = {"tags": tags}
        return self.session.get(f"{self.BASE_URL}/pet/findByTags", params=params)
    
    def update_pet_with_form(self, pet_id: int, name: Optional[str] = None, 
                             status: Optional[str] = None) -> requests.Response:
        """
        POST /pet/{petId} - Update a pet with form data.
        
        Args:
            pet_id: Pet ID to update
            name: Updated name
            status: Updated status
        """
        data = {}
        if name:
            data["name"] = name
        if status:
            data["status"] = status
        
        return self.session.post(
            f"{self.BASE_URL}/pet/{pet_id}",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
    
    def upload_pet_image(self, pet_id: int, file_path: str, 
                         additional_metadata: Optional[str] = None) -> requests.Response:
        """
        POST /pet/{petId}/uploadImage - Upload an image for a pet.
        
        Args:
            pet_id: Pet ID
            file_path: Path to image file
            additional_metadata: Additional data to pass
        """
        with open(file_path, "rb") as f:
            files = {"file": f}
            data = {}
            if additional_metadata:
                data["additionalMetadata"] = additional_metadata
            return self.session.post(
                f"{self.BASE_URL}/pet/{pet_id}/uploadImage",
                files=files,
                data=data
            )


def create_pet_payload(
    pet_id: int,
    name: str,
    status: str = "available",
    category_id: int = 1,
    category_name: str = "Dogs",
    photo_urls: Optional[List[str]] = None,
    tags: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Helper function to create a pet payload.
    
    Args:
        pet_id: Unique ID for the pet
        name: Name of the pet
        status: Pet status (available, pending, sold)
        category_id: Category ID
        category_name: Category name
        photo_urls: List of photo URLs
        tags: List of tag objects
    
    Returns:
        Dict representing a pet object
    """
    return {
        "id": pet_id,
        "category": {
            "id": category_id,
            "name": category_name
        },
        "name": name,
        "photoUrls": photo_urls or ["https://example.com/photo.jpg"],
        "tags": tags or [{"id": 1, "name": "friendly"}],
        "status": status
    }

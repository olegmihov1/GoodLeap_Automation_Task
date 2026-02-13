# API Automation Tests - Swagger Petstore

## Target API
**Swagger Petstore**: https://petstore.swagger.io/

## Tools/Frameworks Used

| Tool/Framework | Version | Purpose |
|---------------|---------|---------|
| Python | 3.10+ | Programming language |
| pytest | 8.3.4 | Test framework |
| requests | 2.32.3 | HTTP client for API calls |
| pytest-html | 4.1.1 | HTML test reports |
| pytest-xdist | 3.5.0 | Parallel test execution |

## How to Run

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt
```

### Run All API Tests
```bash
pytest api/ -v
```

### Run with HTML Report
```bash
pytest api/ -v --html=reports/api-report.html
```

### Run Specific Test Class
```bash
pytest api/test_pet_api.py::TestCreatePet -v
```

### Run Tests by Marker
```bash
# Run only critical API tests
pytest api/ -v -m "api and critical"
```

## Endpoints Covered

| Method | Endpoint | Description | Test Coverage |
|--------|----------|-------------|---------------|
| POST | /pet | Add a new pet | ✅ 4 tests |
| GET | /pet/{petId} | Find pet by ID | ✅ 3 tests |
| PUT | /pet | Update an existing pet | ✅ 3 tests |
| DELETE | /pet/{petId} | Delete a pet | ✅ 3 tests |
| GET | /pet/findByStatus | Find pets by status | ✅ 5 tests |
| POST | /pet/{petId} | Update pet with form data | ✅ 3 tests |

## Test Classes and Coverage

### TestCreatePet (POST /pet)
| Test Name | Priority | Description |
|-----------|----------|-------------|
| test_create_pet_success | CRITICAL | Create pet with valid data |
| test_create_pet_with_all_fields | HIGH | Create pet with all optional fields |
| test_create_pet_status_sold | MEDIUM | Create pet with 'sold' status |
| test_create_pet_minimal_data | MEDIUM | Create pet with minimum required data |

### TestGetPet (GET /pet/{petId})
| Test Name | Priority | Description |
|-----------|----------|-------------|
| test_get_pet_by_id_success | CRITICAL | Get existing pet by ID |
| test_get_pet_not_found | CRITICAL | Get non-existent pet (404) |
| test_get_pet_invalid_id | MEDIUM | Get pet with invalid ID format |

### TestUpdatePet (PUT /pet)
| Test Name | Priority | Description |
|-----------|----------|-------------|
| test_update_pet_name | CRITICAL | Update pet name |
| test_update_pet_status | CRITICAL | Update pet status |
| test_update_pet_category | MEDIUM | Update pet category |

### TestDeletePet (DELETE /pet/{petId})
| Test Name | Priority | Description |
|-----------|----------|-------------|
| test_delete_pet_success | CRITICAL | Delete existing pet |
| test_delete_pet_not_found | MEDIUM | Delete non-existent pet |
| test_delete_pet_with_api_key | MEDIUM | Delete with API key header |

### TestFindPetsByStatus (GET /pet/findByStatus)
| Test Name | Priority | Description |
|-----------|----------|-------------|
| test_find_pets_by_status_available | CRITICAL | Find available pets |
| test_find_pets_by_status_pending | MEDIUM | Find pending pets |
| test_find_pets_by_status_sold | MEDIUM | Find sold pets |
| test_find_pets_by_multiple_statuses | HIGH | Find by multiple statuses |
| test_find_pets_invalid_status | LOW | Invalid status handling |

### TestUpdatePetWithForm (POST /pet/{petId})
| Test Name | Priority | Description |
|-----------|----------|-------------|
| test_update_pet_name_with_form | MEDIUM | Update name via form data |
| test_update_pet_status_with_form | MEDIUM | Update status via form data |
| test_update_nonexistent_pet_with_form | MEDIUM | Update non-existent pet |

### TestPetApiEdgeCases
| Test Name | Priority | Description |
|-----------|----------|-------------|
| test_create_pet_with_special_characters_name | LOW | Special characters in name |
| test_create_pet_with_unicode_name | LOW | Unicode characters in name |
| test_create_pet_with_long_name | LOW | Very long pet name |
| test_concurrent_pet_operations | MEDIUM | Create and get consistency |

## Test Summary

| Category | Total Tests | Critical | High | Medium | Low |
|----------|-------------|----------|------|--------|-----|
| Create Pet | 4 | 1 | 1 | 2 | 0 |
| Get Pet | 3 | 2 | 0 | 1 | 0 |
| Update Pet | 3 | 2 | 0 | 1 | 0 |
| Delete Pet | 3 | 1 | 0 | 2 | 0 |
| Find by Status | 5 | 1 | 1 | 2 | 1 |
| Update with Form | 3 | 0 | 0 | 3 | 0 |
| Edge Cases | 4 | 0 | 0 | 1 | 3 |
| **TOTAL** | **25** | **7** | **2** | **12** | **4** |

## Design Decisions

### Why These Endpoints?
- **Pet endpoints** represent core CRUD operations
- **findByStatus** is a commonly used query endpoint
- These endpoints demonstrate various HTTP methods and parameter types

### Test Strategy
1. **Happy Path Tests**: Verify expected behavior with valid inputs
2. **Error Handling**: Test 404 responses, invalid inputs
3. **Boundary Tests**: Special characters, unicode, long strings
4. **Data Consistency**: Verify create/read/update/delete cycles

### Fixtures
- `pet_client`: Reusable API client for all tests
- `created_pet`: Creates and cleans up test data automatically
- `unique_pet_id`: Generates unique IDs to avoid conflicts

## Notes
- The Petstore API is a demo API and may have occasional availability issues
- Some tests create temporary data and clean up after execution
- Random pet IDs are used to avoid conflicts with other testers

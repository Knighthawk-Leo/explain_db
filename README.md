# Explain DB

A Django package that provides an API to expose Django model metadata and structure information.

## Installation

Install the package via pip:

```bash
pip install explain_db
```

## Setup

1. Add `explain_db` to your Django project's `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... your other apps
    'explain_db',
]
```

2. Include the explain_db URLs in your project's main `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... your other URL patterns
    path('api/explain/', include('explain_db.urls')),
]
```

## Usage

The package exposes one API endpoint that returns metadata for a specified Django model:

```
GET /api/explain/<model_name>/
```

### Example

If you have a model named `User`, you can get its metadata by making a GET request to:

```
GET /api/explain/User/
```

### Response Format

The API returns detailed information about the model including:

- Table name and description
- Column details (name, type, description, relationships, etc.)
- Foreign key relationships
- Field constraints (nullable, blank, default values)

```json
[
    {
        "table_name": "auth_user",
        "table_description": "User model description",
        "columns": [
            {
                "name": "id",
                "type": "AutoField",
                "description": "",
                "is_relation": false,
                "nullable": false,
                "blank": false,
                "default": null,
            },
            // ... more columns
        ]
    }
]
```

## Requirements

- Django >= 3.2
- Django REST Framework >= 3.12.0
- Python >= 3.8

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. 
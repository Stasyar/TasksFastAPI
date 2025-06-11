from datetime import datetime, UTC
from uuid import UUID

now = datetime.now(UTC)

USERS = (
    {
        "id": UUID('3d3e784f-646a-4ad4-979c-dca5dcea2a28'),
        "full_name": "Alice Example",
        "email": "alice@example.com",
    },
    {
        "id": UUID('bb929d29-a8ef-4a8e-b998-9998984d8fd6'),
        "full_name": "Bob Example",
        "email": "bob@example.com",
    },
)
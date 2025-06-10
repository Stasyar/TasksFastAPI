import uuid

from src.schemas.tasks_schema import TaskStatus

TEST_USERS_GET_MOCK = [
    (
        uuid.uuid4(),
        "John Doe",
        "john@example.com"
    ),
    (
        uuid.uuid4(),
        "Jane Doe",
        "jane@example.com"
    ),
]

TEST_USERS_CREATE_MOCK = [
    (
        "John Doe",
        "john@example.com"
    ),
    (
        "Jane Doe",
        "jane@example.com"
    ),
]


TEST_TASKS_GET_MOCK = [
    (
        uuid.uuid4(),
        "Task title",
        "Task description",
        TaskStatus.TODO
    )
]

TEST_TASKS_CREATE_MOCK = [
    (
        "Task title",
        "Task description",
        TaskStatus.TODO,
        uuid.uuid4()
    )
]
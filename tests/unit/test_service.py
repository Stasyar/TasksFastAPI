import pytest
from unittest.mock import AsyncMock, MagicMock

from src.schemas.tasks_schema import CreateTaskSchema
from src.schemas.users_schemas import CreateUserSchema
from src.services.tasks import TaskService
from src.services.users import UserService
from src.models import User, Task
from tests import test_cases


@pytest.fixture
def mock_uow():
    mock = MagicMock()
    mock.user = AsyncMock()
    mock.task = AsyncMock()
    mock.is_open = True
    return mock


@pytest.fixture
def user_service(mock_uow):
    return UserService(uow=mock_uow)


@pytest.fixture
def task_service(mock_uow):
    return TaskService(uow=mock_uow)


@pytest.mark.parametrize(
    "user_id, full_name, email",
    test_cases.TEST_USERS_GET_MOCK
)
async def test_get_user(user_id, full_name, email, mock_uow, user_service):
    mock_user_obj = User(
        id=user_id,
        full_name=full_name,
        email=email
    )
    mock_uow.user.get_by_id_one_or_none.return_value = mock_user_obj

    result = await user_service.get_user(user_id)

    mock_uow.user.get_by_id_one_or_none.assert_called_once_with(user_id)
    assert result == mock_user_obj


@pytest.mark.parametrize(
    "full_name, email",
    test_cases.TEST_USERS_CREATE_MOCK
)
async def test_create_user_with_correct_data(full_name, email, user_service, mock_uow):
    data = CreateUserSchema(full_name=full_name, email=email)
    fake_user = User(full_name=data.full_name, email=data.email)
    mock_uow.user.add_one_and_get_obj.return_value = fake_user

    result = await user_service.create_user(data)

    mock_uow.user.add_one_and_get_obj.assert_called_once_with(data.model_dump())
    assert result == fake_user


@pytest.mark.parametrize(
    "task_id, title, description, status",
    test_cases.TEST_TASKS_GET_MOCK
)
async def test_create_task_with_correct_data(task_id, title, description, status, task_service, mock_uow):
    mock_task = Task(task_id=task_id, title=title, description=description, status=status)
    mock_uow.task.get_by_id_one_or_none.return_value = mock_task

    result = await task_service.get_task(task_id)

    mock_uow.task.get_by_id_one_or_none.assert_called_once_with(task_id)
    assert result == mock_task


@pytest.mark.parametrize(
    "title, description, status, author_id",
    test_cases.TEST_TASKS_CREATE_MOCK
)
async def test_create_task_with_correct_data(title, description, status, author_id, task_service, mock_uow):
    data = CreateTaskSchema(title=title, description=description, status=status, author_id=author_id,)
    fake_task = Task(title=title, description=description, status=status, author_id=author_id)
    mock_uow.task.add_one_and_get_obj.return_value = fake_task

    result = await task_service.create_task(data)

    mock_uow.task.add_one_and_get_obj.assert_called_once_with(data.model_dump())
    assert result == fake_task

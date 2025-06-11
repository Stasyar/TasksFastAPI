from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.utils import RequestTestCase

TEST_USER_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'/users/',
        headers={},
        data={
            "full_name": "Ivan Ivanov",
            "email": "ivan@example.com"
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            "success": True,
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'/users/',
        headers={},
        data={
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    )
]

TEST_USER_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'/users/3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            "full_name": "Alice Example",
            "email": "alice@example.com",
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'/users/1',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid user id',
    ),
    RequestTestCase(
        url=f'/users/4d3e784f-646a-4ad4-979c-dca5dcea2a29',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent user',
    ),
]
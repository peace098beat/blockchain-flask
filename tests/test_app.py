import json
import pytest

from fiblockchain.application import application

import sys


def test_version():
    assert sys.version_info.major == 3


@pytest.fixture
def client():
    return application.test_client()


def test_test_get(client):
    result = client.get("/test")

    response_body = json.loads(result.get_data())
    assert result.status_code == 200
    assert result.headers['Content-Type'] == 'application/json'
    assert response_body['Output'] == 'Hello Test'


def test_test_post(client):
    result = client.post("/test",
                         content_type='application/json',
                         follow_redirects=True)

    response_body = json.loads(result.get_data())
    assert result.status_code == 200
    assert result.headers['Content-Type'] == 'application/json'
    assert response_body['Output'] == 'Hello Test'


def test_new(client):
    data = {
        "sender": "1234567890",
        "recipient": "0987654321",
        "amount": 1000}

    result = client.post("/transactions/new",
                         json=data,
                         content_type='application/json',
                         follow_redirects=True)
    result_data = result.get_data()
    response_body = json.loads(result_data)
    assert result.status_code == 200
    assert result.headers['Content-Type'] == 'application/json'
    # assert response_body['Output'] == 'Hello Test'


# def test_mine(client):
#     result = client.get("/mine")
#     response_body = json.loads(result.get_data())
#     assert result.status_code == 200
#     assert result.headers['Content-Type'] == 'application/json'
#     # assert response_body['Output'] == 'Hello Test'


# def test_chain(client):
#     result = client.get("/chain")
#     data = json.loads(result.get_data())

#     with open("chains", "w") as fp:
#         json.dump(data, fp, indent=4)

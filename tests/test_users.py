import json

import pytest
from api.db import get_db
from api.users import get_users
from flask import jsonify


def test_get_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert len(response.json["users"]) == 2


def test_get_user(client):
    response = client.get('/users/1')
    assert response.status_code == 200


def test_delete_user(client):
    response = client.delete('/users/1')
    assert response.status_code == 200


def test_create_user_empty(client):
    response = client.post('/users/')
    assert response.status_code == 400


def test_create_user(client):
    data = {"first_name": "Fred"}
    response = client.post('/users/', json=json.dumps(data))
    assert response.status_code == 400

    data["last_name"] = "fredderton"
    response = client.post('/users/', json=json.dumps(data))
    assert response.status_code == 400

    data["email"] = "fred@fred.com"
    response = client.post('/users/', json=json.dumps(data))
    assert response.status_code == 200


def test_update_user(client):
    data = {"first_name": "Robert", "last_name": "Robertington"}
    response = client.put('/users/1', json=json.dumps(data))
    assert response.status_code == 200






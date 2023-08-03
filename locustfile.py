import json

from locust import HttpUser, task


class LoadTestUsers(HttpUser):
    @task
    def load_test_get_users(self):
        self.client.get("/users/")

    @task
    def load_test_get_user(self):
        self.client.get("/users/1")

    @task
    def test_update_user(self):
        data = {"first_name": "Robert", "last_name": "Robertington"}
        self.client.put('/users/1', json=json.dumps(data))



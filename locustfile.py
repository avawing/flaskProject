from locust import HttpUser, task


class LoadTestUsers(HttpUser):
    @task
    def load_test_get_users(self):
        self.client.get("/users/")

    @task
    def load_test_get_user(self):
        self.client.get("/users/1")

from locust import HttpUser, task

class HelloWorldUser(HttpUser):
    @task
    def hello_world(self):
        self.client.get("http://127.0.0.1:8000/ru/list")
        self.client.get("http://127.0.0.1:8000/ru/details/2070")
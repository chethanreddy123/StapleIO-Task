from locust import HttpUser, task, between

class MyUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between requests (in seconds)

    @task
    def openai_completion(self):
        payload = {"user_id": "chethanreddy", "prompt": "hi, how are you?"}
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/ai_services/openai-completion", json=payload, headers=headers)
        print(response.text)

    @task
    def add_user(self):
        payload = {"username": "chethanreddy"}
        headers = {"Content-Type": "application/json"}
        response = self.client.post("/users/add-user", json=payload, headers=headers)
        print(response.text)

    @task
    def get_user_logs(self):
        user_id = "chethanreddy"
        response = self.client.get(f"/users/user-logs/{user_id}")
        print(response.text)

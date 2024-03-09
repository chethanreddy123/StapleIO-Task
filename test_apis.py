import unittest
import requests

class TestOpenAICompletionAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:5000"

    def test_openai_completion_valid_request(self):
        payload = {"user_id": "chethanreddy", "prompt": "hi, how are you?"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/ai_services/openai-completion", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_openai_completion_missing_user_id(self):
        payload = {"prompt": "Test prompt"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/ai_services/openai-completion", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_openai_completion_missing_prompt(self):
        payload = {"user_id": "123"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/ai_services/openai-completion", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_openai_completion_invalid_user_id(self):
        payload = {"user_id": "invalid_id", "prompt": "Test prompt"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/ai_services/openai-completion", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_openai_completion_long_prompt(self):
        payload = {"user_id": "123", "prompt": "A" * 2000}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/ai_services/openai-completion", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)


class TestAddUserAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:5000"

    def test_add_user_valid_request(self):
        payload = {"username": "testuser"}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/users/add-user", json=payload, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_add_user_missing_username(self):
        payload = {}  # Missing 'username' field
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/users/add-user", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_add_user_empty_username(self):
        payload = {"username": ""}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/users/add-user", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_add_user_existing_username(self):
        existing_username = "existing_user"
        # Adding a user with existing username first
        requests.post(f"{self.base_url}/users/add-user", json={"username": existing_username}, headers={"Content-Type": "application/json"})

        # Trying to add a user with the same username again
        payload = {"username": existing_username}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{self.base_url}/users/add-user", json=payload, headers=headers)
        self.assertEqual(response.status_code, 400)


class TestGetUserLogsAPI(unittest.TestCase):
    base_url = "http://127.0.0.1:5000"

    def test_get_user_logs_valid_request(self):
        user_id = "chethanreddy"
        response = requests.get(f"{self.base_url}/users/user-logs/{user_id}")
        self.assertEqual(response.status_code, 200)

    def test_get_user_logs_empty_user_id(self):
        user_id = ""
        response = requests.get(f"{self.base_url}/users/user-logs/{user_id}")
        self.assertEqual(response.status_code, 400)

    def test_get_user_logs_invalid_user_id(self):
        invalid_user_id = "invalid_id"
        response = requests.get(f"{self.base_url}/users/user-logs/{invalid_user_id}")
        self.assertEqual(response.status_code, 400)

    def test_get_user_logs_nonexistent_user_id(self):
        nonexistent_user_id = "nonexistent_id"
        response = requests.get(f"{self.base_url}/users/user-logs/{nonexistent_user_id}")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()

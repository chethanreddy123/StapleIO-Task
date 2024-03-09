# OpenAI Chat Assistant with Flask API

Welcome to the OpenAI Chat Assistant project! This application leverages the OpenAI Chat API to provide a conversational interface. Users can interact with the system by sending prompts, and the application generates responses using OpenAI's powerful language model.

## Introduction

This project aims to provide a seamless interface for users to interact with OpenAI's language model. Users can submit prompts, and the system generates responses based on previous interactions stored in a SQLite database.

## Setup

### Prerequisites

Before running the application, ensure you have the necessary dependencies installed. Use the following command:

```bash
pip install -r requirements.txt
```

## Usage

To start the application, use the following command:

```bash
python main.py
```

This will launch the Flask API, and the application will be accessible at `http://127.0.0.1:5000`.

## API Endpoints

### OpenAI Completion Service

#### `/openai-completion` (POST)

Endpoint for OpenAI completion service.

- **Request Payload:**
  ```json
  {
    "user_id": "chethanreddy",
    "prompt": "hi, how are you?"
  }
  ```
- **Response:**
  ```json
  {
    "completion": "OpenAI completion response"
  }
  ```

### User Routes

#### `/add-user` (POST)

Endpoint for adding a user.

- **Request Payload:**
  ```json
  {
    "username": "chethanreddy"
  }
  ```
- **Response:**
  ```json
  {
    "user_id": 123
  }
  ```

#### `/user-logs/<user_id>` (GET)

Endpoint for retrieving logs for a specific user.

- **Response:**
  ```json
  {
    "logs": [
      {
        "user": "Prompt",
        "assistant": "Completion",
        "time": "Timestamp"
      },
      ...
    ]
  }
  ```

  ![Screenshot 2024-03-09 at 2 49 57 PM](https://github.com/chethanreddy123/StapleIO-Task/assets/69640722/59a582c8-6946-4f5a-9348-b67d084b5630)


## Testing

This project includes both load testing and unit testing to ensure the robustness and reliability of the application.

### Load Testing with Locust

To perform load testing using Locust, follow these steps:

1. Install Locust using the following command:
   ```bash
   pip install locust
   ```

2. Navigate to the project directory and run the Locust command:
   ```bash
   locust -f locustfile.py
   ```

3. Open your web browser and go to `http://localhost:8089` to access the Locust web interface.

4. Enter the desired number of users, spawn rate, and other parameters.

5. Click "Start Swarming" to initiate the load testing.

Locust will simulate user behavior and generate a report detailing the application's performance under various loads.

![Screenshot 2024-03-09 at 2 50 44 PM](https://github.com/chethanreddy123/StapleIO-Task/assets/69640722/7b4a9e93-01db-439b-9e0b-bb68608afeb1)

![Screenshot 2024-03-09 at 2 50 52 PM](https://github.com/chethanreddy123/StapleIO-Task/assets/69640722/37638598-3c24-44a1-967d-5c5d4499a11b)


### Unit Testing with unittest

Unit tests are implemented using the `unittest` framework. To run the unit tests, execute the following command:

```bash
python test_apis.py
```

This command will execute the test cases defined in the `test_apis.py` file. Feel free to add more test cases to cover additional scenarios.

### Running Specific Test Cases

If you want to run specific test cases or a specific test suite, you can use the following command:

```bash
python -m unittest test_apis.TestOpenAICompletionAPI
```

Replace `TestOpenAICompletionAPI` with the desired test class or module.

### Generating Test Coverage Report

To generate a test coverage report, you can use the `coverage` tool. First, install it:

```bash
pip install coverage
```

Then, run your tests with coverage:

```bash
coverage run -m unittest test_apis.py
```

Finally, generate the coverage report:

```bash
coverage report -m
```

This report will show the percentage of code coverage for your unit tests.


## License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code as per the terms of the license.

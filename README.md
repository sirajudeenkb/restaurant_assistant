# AI Receptionist

## Description
This project involves setting up an ngrok domain, configuring a Colab notebook, using Ollama model, and setting up a Qdrant vector DB container with Docker to build an AI recetptionist for interaction eg: receptionist at a restaurant.

## Prerequisites
- Python 3.x
- pip
- ngrok account
- Git
- Docker

## Setup Instructions

### 1. Get a ngrok domain and authtoken
1. Sign up or log in to your [ngrok account](https://ngrok.com/).
2. Navigate to the [dashboard](https://dashboard.ngrok.com/) to find your authtoken.
3. Note down your authtoken for later use.

### 2. Open the Colab Notebook
1. Open the Colab notebook provided in the project.
2. Replace the placeholder with your ngrok authtoken.
3. Run all cells in the notebook.
4. In the xterm terminal cell, run the following command:
    ```sh
    ollama pull llama3.1
    ```

### 3. Clone the Repository
1. Open a terminal or command prompt.
2. Clone the repository using Git:
    ```sh
    git clone https://github.com/sirajudeenkb/restaurant_assistant.git
    ```
3. Navigate into the project directory:
    ```sh
    cd restaurant_assistant
    ```

### 4. Create Virtual Environment
1. Create a virtual environment using `pip`:
    ```sh
    python -m venv venv
    ```
2. Activate the virtual environment:
    - On Windows:
        ```sh
        .\venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```sh
        source venv/bin/activate
        ```

### 5. Install Packages from `requirements.txt`
1. Ensure the virtual environment is activated.
2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

### 6. Set Up Qdrant Vector DB with Docker
1. Install Docker from [here](https://www.docker.com/products/docker-desktop).
2. Pull Qdrant container image using:
  ```sh
  docker pull qdrant/qdrant
  ```
3. Run the following command to start the Qdrant vector DB container and configure storage on Windows:
    ```sh
    docker run -d -p 6333:6333 -p 6334:6334 -v C:\qdrant_storage:/qdrant/storage qdrant/qdrant
    ```

### 7. Run the `live_transcription.py` File
1. Ensure the virtual environment is activated.
2. Run the `live_transcription.py` file:
    ```sh
    python live_transcription.py
    ```
from locust import HttpUser, task, between

class MoocMavenUser(HttpUser):
    wait_time = between(1, 5)  # Wait time between task execution (in seconds)

    @task
    def perform_search(self):
        # Define the search query and language for the search
        query = "machine learning"
        lang = "english"

        # Make a POST request to the /search endpoint with the search query and language
        self.client.post("/search", json={"query": query, "lang": lang})

    @task
    def get_providers(self):
        # Define the language for which providers are requested
        lang = "english"

        # Make a GET request to the /providers/{lang} endpoint
        self.client.get(f"/providers/{lang}")

    # Add more tasks as needed, simulating different user actions on the API


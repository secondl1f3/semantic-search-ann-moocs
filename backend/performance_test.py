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

    @task
    def download_csv(self):
        # Replace "english" with the desired language you want to download
        language = "arabic"
        url = f"/download/{language}"

        # Make a GET request to download the CSV file
        response = self.client.get(url, headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJyeXV1a3VzbyIsImV4cCI6MTY5MDAyNzIxMX0.kfAVCt9vv5K0xbOEQquZP-4-Ql4WhAk5OpjEYNTZGSA"})

        # Check if the request was successful
        if response.status_code == 200:
            print(f"Downloaded CSV for language: {language}")
        else:
            print(f"Failed to download CSV for language: {language} - Status Code: {response.status_code}")


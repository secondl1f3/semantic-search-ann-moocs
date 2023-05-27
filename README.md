# semantic-search-ann-moocs

# Semantic Search Unified MOOCs

This repository contains the source code for a semantic search application for Unified MOOCs (Massive Open Online Courses). The application allows users to search for MOOCs based on their query and retrieve relevant results using semantic search techniques.

## Features

- Perform semantic search on MOOCs data
- Retrieve relevant search results based on user queries
- Pagination support for displaying search results
- Download MOOCs data in CSV format for a specific language

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/semantic-search-moocs.git
   cd semantic-search-moocs

2. Set up the environment:
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

I'm use mamba for library. Please read more about mamba here https://mamba.readthedocs.io/en/latest/

# Install the required dependencies
pip install -r requirements.txt

3. Run the application:

    ```shell
    uvicorn main:app --reload
  

The application will start running on http://127.0.0.1:8000.

## API Endpoints
POST /search: Perform a semantic search for MOOCs based on a user query.
GET /providers/{lang}: Get the list of MOOC providers for a specific language.
GET /download/{language}: Download the MOOCs data in CSV format for a specific language.

For detailed API documentation, you can refer to the API Documentation file: https://api.moocmaven.com/docs

## Contribution
Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.


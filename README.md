# Cat-Diary

Cat Diary is a Django Rest Framework (DRF) project that allows users to upload a photo of their cat along with a daily diary entry. Users can view all diary entries, retrieve entries for a specific date, and receive an email containing the diary entry from the exact same day a year ago. This project leverages Redis for caching, and Celery with Redis for handling email tasks.
# Features

    1. Upload a cat photo and diary entry for the day.
    2. Retrieve all diary entries.
    3. Retrieve a diary entry for a specific date.
    4. Receive an email with the diary entry from the same date a year ago.

# Endpoints

    1. Upload Diary Entry
        URL: api/create_diary/
        Method: POST
        Description: Upload a photo of your cat and a diary entry.
        Parameters:
            photo: Image file of the cat.
            entry: Text of the diary entry.
            date: Date of the diary entry (optional, defaults to today).

    2. Get All Diary Entries
        URL: api/list_diary/
        Method: GET
        Description: Retrieve all diary entries.

    3. Get Diary Entry for Specific Date
        URL: /diary/date/<date>/
        Method: GET
        Description: Retrieve the diary entry for a specific date.
        Parameters:
            date: Date of the desired diary entry in YYYY-MM-DD format.

    4. Get Email with Diary Entry from a Year Ago
        URL: api/diary_by_date/
        Method: POST
        Description: Receive an email containing the diary entry from the same date a year ago.
        Parameters:
            email: Email address to send the diary entry to.

# Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/cat-diary.git
    cd cat-diary
    ```

2. Create a virtual environment and activate it:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Set up Redis:
    Follow the instructions on Redis's official site to install and run Redis on your machine.

## Configure Celery:
    In your project settings, configure Celery to use Redis as the message broker.

# Configuration

    Update the settings.py file with your configurations, especially for Redis and email settings.

# Usage

    Use a tool like Postman or cURL to interact with the API endpoints.
    Ensure Redis and Celery are running to handle caching and email tasks.

# License

    This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgements

    Django Rest Framework
    Redis
    Celery


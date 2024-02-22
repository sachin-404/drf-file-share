# DRF File Share

This project is a Django-based file sharing application with REST API endpoints. It allows users to upload, list, and download files. Additionally, it includes user authentication features such as signup, login, logout, and email verification.

## Getting Started
To get started with this project, follow these instructions:

1. Clone the repository to your local machine:
    ```
    git clone <repository-url>
    ```
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

3. Apply migrations to create the necessary database schema:
    ```
    python manage.py migrate
    ```

4. Run the development server:
    ```
    python manage.py runserver
    ```

5. Access the API endpoints using the provided URLs.

## API Endpoints
- **Upload File:**

    **POST /upload-file/**

    Endpoint for uploading files. Requires authentication.

- **List Files:**

    **GET /list-files/**

    Endpoint for listing all files. Requires authentication.

- **Download File:**

    **GET /download-file/<file-id>/**

    Endpoint for downloading a specific file by its ID. Requires authentication.

- **User Signup:**

    **POST /signup/**

    Endpoint for user signup. No authentication required.

- **User Login:**

    **POST /login/**

    Endpoint for user login. No authentication required.

- **User Logout:**
    **POST /logout/**

    Endpoint for user logout. Requires authentication.

- **Verify Email:**

    **GET /verify-email/<uidb64>/<token>/**

    Endpoint for verifying user email. No authentication required.

## Technologies Used
- Django
- Django REST Framework

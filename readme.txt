
    Backend Documentation for Sandak App

This document provides an overview of the API endpoints for the Sandak app backend. Each endpoint is described with its purpose, required parameters, and expected responses.



    API Endpoints

1. User Registration
- Endpoint:`/auth/registration/`
- Method: `POST`
- Purpose:Register a new user in the system.
- Parameters:
  - `email` (string): The user's email address.
  - `username` (string): The desired username.
  - `first_name` (string): The desired first name.
  - `last_name` (string): The desired last name.
  - `password` (string): The user's password.
  - `password2` (string): Confirmation of the password (must match `password`).
  -'date of birth' (int): user date of birth 
  -'personal_image' (image): users image
  -'gender' (string) a user chnose between two options male represinted as M female represinted as F

the age will be sectracted form the user date of birth

-Notes:

  - Passwords must match (`password` and `password2`).

- Response:
  - On success:
    ```json
    {
    "id": 6,
    "response": "Successfully registered new user.",
    "email": "elderly2@example.com",
    "username": "elderly2_user",
    "first_name": "John2",
    "last_name": "Doe2",
    "gender": "F",
    "age": 60,
    "token": "003bb925382076ce341bb6c3d26c8907a234eaae"
}
    ```
  - On failure:
    ```json
    {
      "error": "Passwords must match."
    }
    ```

---

2. User Login
- Endpoint: `/auth/login/`
- Method:`POST`
- Purpose:Authenticate a user and generate a token for session management.
- Parameters:
  - `username` (string): The user's email address (passed as `username` due to Django's built-in authentication system).
  - `password` (string): The user's password.
- Response:
  - On success:
    ```json
    {
      "token": "81432311835d53018cf9d8bd355ce1dcf0fa6c78"
    }
    ```
  - On failure:
    ```json
    {
      "error": "Invalid credentials."
    }
    ```

---

3. User Logout
- Endpoint: `/auth/logout/`
- Method: `POST`
- Purpose: Log out the user by deleting their authentication token.
- Authentication:
  - Include the user's token in the request headers under the `Authorization` label.
  - Format: `Token {user_token}` (replace `{user_token}` with the actual token).
- Response:
  - On success:
    ```json
    {
      "message": "Logged out successfully."
    }
    ```
  - If the user is already logged out (no token exists):
    ```json
    {
      "message": "User is already logged out."
    }
    ```

---

Example Workflow

1. Register a New User
- Request:
  ```json
  POST /auth/registration/
 
{
  "username": "elderly_user",
    "email": "elderly@example.com",
    "password": "StrongPass123",
    "password2": "StrongPass123",
    "first_name": "John",
    "last_name": "Doe",
    "age":60,
    "gender": "M"
    "date of birth":"2000-03-2"
    "personal_image" users image

}
  ```
- Response:
  ```json
{
    "id": 6,
    "response": "Successfully registered new user.",
    "email": "elderly2@example.com",
    "username": "elderly2_user",
    "first_name": "John2",
    "last_name": "Doe2",
    "gender": "F",
    "age": 60,
    "token": "003bb925382076ce341bb6c3d26c8907a234eaae"
}
  ```

2. Log In
- Request:
  ```json
  POST /auth/login/
  {
    "username": "user@example.com",
    "password": "securepassword123"
  }
  ```
- Response:
  ```json
  {
    "token": "81432311835d53018cf9d8bd355ce1dcf0fa6c78"
  }
  ```

3. Log Out
- Request:
    json
  POST /auth/logout/
  Headers:
    Authorization: Token 81432311835d53018cf9d8bd355ce1dcf0fa6c78
  ```
- Response:
    json
  {
    "message": "Logged out successfully."
  }

4. Add Family Member

Endpoint: /auth/family-members/

Method: POST

Purpose: Add a family member to the user's account.

Authentication: Required (Token-based authentication).

Parameters:

family_member_username (string): The username of the family member to be added.

relationship_type (string): The relationship (e.g., Brother, Sister, Parent).

Response:

On success:
{
    "id": 4,
    "user_id": 4,
    "user_username": "elderly_user",
    "family_member_id": 5,
    "family_member_username_display": "young_user",
    "relationship_type": "son",
    "added_at": "2025-03-15T13:46:56.634710Z"
}
On failure:
{
  "error": "User not found."
}

{
  "error": "you can not add your self as family member."
}
5.remove Family Member

Endpoint: /auth/family-members/<int:pk>/remove/

Method: POST

Purpose: remove a family member from to the user's account.

Authentication: Required (Token-based authentication).

the <int:pk> parameter is the id of the relationship between the user and the family member


6.list family members
request:GET
list all family members 
Endpoint: /auth/family-members/


7. search for a user 
Endpoint:/auth/search-for-a-user/<str:username>/
Method: GET
Authentication: Required (Token-based authentication).
Parameters: 
  none
  the username of the user we want to qury is added in the <str:username>
On success:
{
    "id": 6,
    "username": "elderly2_user"
}

On failure:
{
  "error": "User not found."
}


medication with crud operations 

8.adding medication 

endpoint: /m/medications/medications/add/

Method: POST

Purpose: Allows a user to add medications for themselves or for an elderly family member.

Parameters:

elderly_user_id (int, optional): The ID of the elderly user for whom the medication is being added.

name (string): Name of the medication.

storage (int): Total quantity of the medication in stock.

dosage (string): Dosage details (e.g., 500mg).

time_in_a_day (JSON object): Specifies the times the medication should be taken (e.g., { "morning": "07:00", "night": "21:00" }).

pills_in_a_time (int): Number of pills to be taken at each scheduled time.

start_date (string, format: YYYY-MM-DD): Date when medication should start.

end_date (string, format: YYYY-MM-DD): Date when medication should end.
to be used by: the username of the user who will use them 

if the user tried to add a medication which iteract with other medication the endpoint will return an error like this  Duloxetine + NSAIDs: Increased risk of bleeding

Behavior:

If elderly_user_id is provided, the medication will be assigned to the user with the specified ID.

If elderly_user_id is not provided, the medication will be added to the authenticated user making the request.

Response:
On success:
{
  "id": 10,
  "user": 4,
  "name": "Metformin",
  "storage": 50,
  "dosage": "500mg",
  "time_in_a_day": { "morning": "07:00", "night": "21:00" },
  "pills_in_a_time": 1,
  "start_date": "2025-03-20",
  "end_date": "2025-06-20",
  "message": "Medication successfully added."
}
on failure
{
  "error": "Elderly user not found."
}


{
  "error": "you do not have permission to delete this medication."
}

9. Add an MRI Record
Endpoint: /mri-records/add/

Method: POST

Purpose: Add a new MRI record for a user or their family member.

Authentication: Required (Token-based authentication).

Parameters:

user_id (int, optional): ID of the elderly user for whom the MRI record is being added. If not provided, the record is added for the authenticated user.

scan_type (string): Type of MRI scan (e.g., Brain MRI, Spine MRI).

scan_date (string, format: YYYY-MM-DD): Date when the scan was performed.

image (file, required): The MRI scan image (uploaded as a file).

report (string, optional): Radiologist's report.

notes (string, optional): Additional notes related to the MRI scan.

doctor_name (string, optional): Name of the doctor who conducted the scan.

doctor_phone (string, optional): Contact number of the doctor.
to be used by: the username of the user who will use them 
On success:

json
{
  "id": 15,
  "user": 4,
  "scan_type": "Brain MRI",
  "scan_date": "2025-03-20",
  "image": "https://example.com/media/mri_scans/brain_mri_15.jpg",
  "report": "MRI scan indicates normal brain structure.",
  "notes": "No abnormalities detected.",
  "doctor_name": "Dr. Ahmed Al-Saadi",
  "doctor_phone": "+966123456789"
}


9.. Retrieve MRI Records
Endpoint: /mri-records/

Method: GET

Purpose: Fetch all MRI records associated with the authenticated user or their family members.

Authentication: Required (Token-based authentication).

10.Retrieve a Single MRI Record
Endpoint: /mri-records/<int:pk>/

Method: GET

Purpose: Fetch a specific MRI record by its ID.

Authentication: Required (Token-based authentication).


11.. Update an MRI Record
Endpoint: /mri-records/<int:pk>/

Method: PUT

Purpose: Update an existing MRI record.

Authentication: Required (Token-based authentication).

Parameters: (Same as the "Add MRI Record" endpoint)


12. Delete an MRI Record
Endpoint: /mri-records/<int:pk>/delete/

Method: DELETE

Purpose: Remove an MRI record.

Authentication: Required (Token-based authentication).





 Base URL: `/HealthRecords/`

 Immunization Endpoints

- List Immunizations
  - `GET /HealthRecords/immunizations/`
  - Response: List of all immunizations

- Retrieve Immunization
  - `GET /HealthRecords/immunizations/{id}/`
  - Response: Details of a specific immunization record

- Create Immunization
  - `POST /HealthRecords/immunizations/add/`
  - Request Body:
    ```json
    {
      "vaccine_name": "string",
      "date": "YYYY-MM-DD",
      "next_dose_reminder": "YYYY-MM-DD"
    }
    ```

- update Immunization
  - `PUT /HealthRecords/immunizations/{id}/update/`
  - Request Body: Same as Create

- Delete Immunization
  - `DELETE /HealthRecords/immunizations/{id}/delete/`

Blood Test Endpoints

- List Blood Tests
  - `GET /HealthRecords/blood-tests/`
  - Response: List of all blood tests

- Retrieve Blood Test
  - `GET /HealthRecords/blood-tests/{id}/`
  - Response: Details of a specific blood test record

- Create Blood Test
  - `POST /HealthRecords/blood-tests/add/`
  - Request Body:
    ```json
    {
      "test_name": "string",
      "test_date": "YYYY-MM-DD",
      "test_results": {},
      "notes": "string (optional)"
    }
    ```

- Update Blood Test
  - `PUT /HealthRecords/blood-tests/{id}/update/`
  - Request Body: Same as Create

- Delete Blood Test
  - `DELETE /HealthRecords/blood-tests/{id}/delete/`

 Disease Endpoints

- List Diseases
  - `GET /HealthRecords/diseases/`
  - Response: List of all diseases

- Retrieve Disease
  - `GET /HealthRecords/diseases/{id}/`
  - Response: Details of a specific disease record

- Create Disease
  - `POST /HealthRecords/diseases/add/`
  - Request Body:
    ```json
    {
      "name": "string",
      "diagnosis_date": "YYYY-MM-DD",
      "severity": "Mild | Moderate | Severe | Chronic",
      "notes": "string (optional)",
      "is_active": true,
      "doctor_name": "string (optional)",
      "doctor_phone": "string (optional)"
    }
    ```

- Update Disease
  - `PUT /HealthRecords/diseases/{id}/update/`
  - Request Body: Same as Create

- Delete Disease
  - `DELETE /HealthRecords/diseases/{id}/delete/`
 MRI Record Endpoints

- List MRI Records
  - `GET /HealthRecords/mri-records/`
  - Response: List of all MRI records

- Retrieve MRI Record
  - `GET /HealthRecords/mri-records/{id}/`
  - Response: Details of a specific MRI record

- Create MRI Record
  - `POST /HealthRecords/mri-records/add/`
  - Request Body:
    ```json
    {
      "scan_type": "string",
      "scan_date": "YYYY-MM-DD",
      "image": "file",
      "report": "string (optional)",
      "notes": "string (optional)",
      "doctor_name": "string (optional)",
      "doctor_phone": "string (optional)"
    }
    ```

- Update MRI Record
  - `PUT /HealthRecords/mri-records/{id}/update/`
  - Request Body: Same as Create

- Delete MRI Record
  - `DELETE /HealthRecords/mri-records/{id}/delete/`


Notes
1. Token-Based Authentication:
   - All authenticated endpoints require the user's token in the `Authorization` header.
   - Format: `Token {user_token}`.

2. Error Handling:
   - If a request fails, the API will return an error message with an appropriate HTTP status code (e.g., `400 Bad Request`, `401 Unauthorized`).

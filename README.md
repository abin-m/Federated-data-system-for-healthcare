# Hospital Management System API

A Django REST Framework-based project for managing hospitals, patient records, user authentication, and aggregated data fetching. This system is designed to handle hospital data efficiently, allowing users to fetch patient records from multiple hospitals through aggregated endpoints.

---

## Features

- Hospital management with CRUD operations.
- Patient record management linked to respective hospitals.
- JWT-based user authentication with role-based access control.
- Aggregated patient record fetching from multiple hospital endpoints.
- Filtering patient records based on dynamic query parameters.
- Mock API for testing hospital endpoints.
- **Filter Metadata API for dynamic filtering options.**

---

## Project Architecture

### Models

1. **Hospital**  
   Represents a hospital with fields for:

   - `name`: Name of the hospital.
   - `location`: Location of the hospital.
   - `api_endpoint`: URL endpoint for fetching hospital data.

2. **PatientRecord**  
   Represents patient data linked to a hospital:

   - `hospital`: Foreign key linking to the `Hospital` model.
   - `patient_id`: Unique identifier for the patient.
   - `name`: Name of the patient.
   - `age`: Age of the patient.
   - `diagnosis`: Medical condition or diagnosis.
   - `created_at`: Timestamp of record creation.

3. **CustomUser**  
   A custom user model with role-based access:
   - `email`: Unique email for login.
   - `username`: Username for the user.
   - `role`: User role (`admin`, `doctor`, `researcher`, or `official`).

---

### Views

1. **HospitalViewSet**  
   Provides CRUD operations for hospitals.  
   Custom action:

   - `fetch_records`: Fetches patient records from a hospital's `api_endpoint`.

2. **PatientRecordViewSet**  
   Provides CRUD operations for patient records.  
   Supports filtering based on query parameters such as `age`, `diagnosis`, and `created_at`.  
   Example:

   ```http
   GET /api/patient-records/?age=30&diagnosis=Flu
   ```

3. **UserSignupView**  
   Handles user registration.

4. **UserLoginView**  
   Handles user login and returns JWT tokens.

5. **CustomTokenRefreshView**  
   Refreshes JWT tokens.

6. **aggredgated_data**  
   Fetches aggregated patient records from all hospital endpoints.

7. **MockHospitalEndpoint**  
   Simulates a hospital API endpoint for testing purposes.

8. **FilterMetadataView**  
   Provides metadata about the available filtering options for patient records.

---

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:

   ```bash
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### Authentication

1. **Sign Up**  
   `POST /api/signup/`  
   Request Body:

   ```json
   {
     "email": "user@example.com",
     "username": "user1",
     "password": "password123",
     "role": "doctor"
   }
   ```

2. **Login**  
   `POST /api/login/`  
   Request Body:

   ```json
   {
     "email": "user@example.com",
     "password": "password123"
   }
   ```

3. **Token Refresh**  
   `POST /api/token/refresh/`  
   Request Body:
   ```json
   {
     "refresh": "<refresh_token>"
   }
   ```

---

### Hospital Endpoints

1. **List Hospitals**  
   `GET /api/hospitals/`

2. **Create Hospital**  
   `POST /api/hospitals/`  
   Request Body:

   ```json
   {
     "name": "Example Hospital",
     "location": "City Center",
     "api_endpoint": "http://example.com/api/"
   }
   ```

3. **Fetch Hospital Records**  
   `GET /api/hospitals/{id}/fetch_records/`  
   Fetches patient records from the specified hospital.

---

### Patient Record Endpoints

1. **List Patient Records**  
   `GET /api/patient-records/`
   Supports filtering based on query parameters. Examples:

   ```http
   GET /api/patient-records/?age=45&diagnosis=Flu
   GET /api/patient-records/?created_at__gte=2024-01-01&created_at__lte=2024-12-31
   GET /api/patient-records/?name__icontains=John
   ```

2. **Create Patient Record**  
   `POST /api/patient-records/`  
   Request Body:

   ```json
   {
     "hospital": 1,
     "patient_id": "P12345",
     "name": "John Doe",
     "age": 45,
     "diagnosis": "Flu"
   }
   ```

3. **Aggregated Data**  
   `GET /api/aggregated-data/`  
   Fetches patient records from all hospital endpoints.

4. **Filter Metadata**  
   `GET /api/filter-metadata/`  
   Provides metadata about available filters for patient records.
   Example Response:
   ```json
   {
     "filters": {
       "age": {
         "type": "integer",
         "description": "Filter patient records by age."
       },
       "diagnosis": {
         "type": "string",
         "description": "Filter patient records by diagnosis."
       },
       "created_at": {
         "type": "date",
         "description": "Filter patient records by creation date."
       }
     }
   }
   ```

---

### Filtering and Query Parameters

The API supports advanced filtering for patient records. The following query parameters can be used:

1. **By Age**  
   Retrieve records for patients of a specific age:

   ```http
   GET /api/patient-records/?age=30
   ```

2. **By Diagnosis**  
   Retrieve records for a specific diagnosis:

   ```http
   GET /api/patient-records/?diagnosis=Flu
   ```

3. **By Name (Case-insensitive)**  
   Retrieve records for patients whose names contain a specific substring:

   ```http
   GET /api/patient-records/?name__icontains=smith
   ```

4. **By Date Range**  
   Retrieve records created within a specific date range:

   ```http
   GET /api/patient-records/?created_at__gte=2024-01-01&created_at__lte=2024-12-31
   ```

5. **Combination of Filters**  
   Filters can be combined to narrow down results:
   ```http
   GET /api/patient-records/?age=45&diagnosis=Flu&name__icontains=John
   ```

---

### Mock API

1. **Mock Hospital Data**  
   `GET /api/mock_hospital_data/`  
   Example Response:
   ```json
   {
     "hospital_name": "Example Hospital",
     "location": "City Center",
     "records": [
       { "patient_id": 1, "name": "John Doe", "age": 45, "condition": "Flu" },
       {
         "patient_id": 2,
         "name": "Jane Smith",
         "age": 34,
         "condition": "Cough"
       }
     ]
   }
   ```

---

## License

This project is open-source and available under the MIT License.

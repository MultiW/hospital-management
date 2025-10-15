# Backend

## Setup Instructions

### Environment Setup
[Install Python 3](https://www.python.org/downloads/)

### Building and Running
#### 1. Activate Python virtual environment
```
cd backend
python3 -m venv venv
source venv/bin/activate
```

#### 2. Install dependencies
```
pip install -r requirements.txt
```

#### 4. Apply the database schemas

*Pre-requisite: make sure your database is created: [Database Setup](../DATABASE.md#setup-instructions).*

Apply the database schema (defined in migrations, which is generated from models) to your local Postgres database.
```
python manage.py migrate
```

Check that the SQL tables were created
```
psql -U postgres -d hospital_management  # open psql terminal
# check tables exist
\d patient
\d bed
\d admission
```

#### 3. Run backend
```
cd backend
python manage.py runserver
```
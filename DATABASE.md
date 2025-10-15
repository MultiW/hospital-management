# Database

## Database Schema Overview

The database consists of three main tables:

### 1. **patient**
Stores patient demographic information.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(255) | Patient's full name |
| mrn | VARCHAR(50) | Medical Record Number (unique identifier) |
| created_at | TIMESTAMP | Record creation timestamp |

### 2. **bed**
Stores hospital bed inventory.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| name | VARCHAR(100) | Bed identifier |
| created_at | TIMESTAMP | Record creation timestamp |

### 3. **admission**
Tracks patient admissions and discharges.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| patient_id | INTEGER | Foreign key to patient table |
| bed_id | INTEGER | Foreign key to bed table |
| admitted_timestamp | TIMESTAMP | When the patient was admitted |
| discharge_timestamp | TIMESTAMP | When the patient was discharged (NULL if still admitted) |

## Setup Instructions

### 1. Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Other platforms:** Download and install from [PostgreSQL official website](https://www.postgresql.org/download/)

### 2. Create ```postgres``` user
1. Connect to postgres from your command line:

    ```psql postgres```

2. Create postgres role:

    ```CREATE ROLE postgres WITH SUPERUSER LOGIN PASSWORD 'postgres';```

### 3. Create Database

Connect to PostgreSQL and create the database:

```bash
# Connect to PostgreSQL (default user is usually 'postgres')
psql -U postgres

# Create the database
CREATE DATABASE hospital_management;

# Connect to the new database
\c hospital_management
```

### 4. Applying the database schema

The database schema will be applied using Django's ORM tools. We will wait until the backend is set up.
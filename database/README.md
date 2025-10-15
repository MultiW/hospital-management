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

### 2. Create Database

Connect to PostgreSQL and create the database:

```bash
# Connect to PostgreSQL (default user is usually 'postgres')
psql -U postgres

# Create the database
CREATE DATABASE hospital_management;

# Connect to the new database
\c hospital_management
```

### 3. Run Schema Script

Execute the schema script to create tables and views:

```bash
# From the database directory
psql -U postgres -d hospital_management -f schema.sql
```

### 4. Verify Installation

Check that tables were created successfully:

```sql
-- List all tables
\dt
```
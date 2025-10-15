-- ============================================
-- Hospital Management System - Database Schema
-- ============================================
-- Description: PostgreSQL schema for managing patients, beds, and admissions
-- in a hospital management system.

-- ============================================
-- Table: patient
-- ============================================
CREATE TABLE patient (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    mrn VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT patient_name_not_empty CHECK (LENGTH(TRIM(name)) > 0),
    CONSTRAINT patient_mrn_not_empty CHECK (LENGTH(TRIM(mrn)) > 0)
);

-- ============================================
-- Table: bed
-- ============================================
CREATE TABLE bed (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT bed_name_not_empty CHECK (LENGTH(TRIM(name)) > 0)
);

-- ============================================
-- Table: admission
-- ============================================
CREATE TABLE admission (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    bed_id INTEGER NOT NULL,
    admitted_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    discharge_timestamp TIMESTAMP NULL,  -- NULL indicates patient is still admitted
    
    -- Foreign key constraints
    CONSTRAINT fk_admission_patient 
        FOREIGN KEY (patient_id) 
        REFERENCES patient(id) 
        ON DELETE RESTRICT,
        ON UPDATE CASCADE
    
    CONSTRAINT fk_admission_bed 
        FOREIGN KEY (bed_id) 
        REFERENCES bed(id) 
        ON DELETE RESTRICT,
        ON UPDATE CASCADE
);
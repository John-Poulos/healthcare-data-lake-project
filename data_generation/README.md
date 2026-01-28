# Phase 1: Data Generation

## Overview
This phase generates realistic synthetic healthcare data for two systems:
1. **Pharmacy System**: Patient demographics, prescriptions, insurance, transactions
2. **EHR System**: Clinical notes, lab results, diagnoses, immunizations

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Generate Data
```bash
# Step 1: Generate pharmacy data
python generate_pharmacy_data.py

# Step 2: Generate EHR data (uses pharmacy patients for consistency)
python generate_ehr_data.py
```

## Output Files

### Pharmacy System Files
- `pharmacy_patients.csv` - Patient demographics (250 patients)
- `pharmacy_insurance.csv` - Insurance profiles (BIN/PCN/Group)
- `pharmacy_prescriptions.csv` - Prescription history (~3,000 prescriptions)
- `pharmacy_transactions.csv` - Insurance adjudication records

### EHR System Files
- `ehr_patients.csv` - Patient demographics (matching pharmacy)
- `ehr_diagnoses.csv` - ICD-10 coded diagnoses
- `ehr_labs.csv` - Laboratory results with reference ranges
- `ehr_clinical_notes.csv` - SOAP notes, progress notes, consultations
- `ehr_immunizations.csv` - Immunization records per ACIP guidelines

## Data Characteristics

### Realism Features

**Demographics**:
- Age distribution matches US population
- Gender representation: ~90% binary (M/F), ~10% other
- Geographic diversity across all US states
- SSN format validation (not real SSNs)

**Disease States** (21 conditions):
- Common: Hypertension (29%), Hyperlipidemia (39%), Diabetes (11%)
- Mental Health: Depression (21%), Anxiety (19%)
- Chronic: COPD, Heart Failure, Rheumatoid Arthritis
- Rare: Multiple Sclerosis (0.03%), Schizophrenia (1%)
- Age-adjusted prevalence

**REMS Medications** (~10% of prescriptions):
- Opioid analgesics (Hydrocodone, Oxycodone, Morphine ER)
- Isotretinoin (Accutane) for severe acne
- Clozapine for schizophrenia
- Fingolimod for multiple sclerosis
- Tracked with special flags and documentation

**Clinical Data**:
- 5% aberrant medication dosing (intentional errors)
- 5-20% abnormal lab values (condition-dependent)
- Realistic lab reference ranges
- Age-appropriate immunization coverage

**Insurance**:
- 10 major carriers (Express Scripts, CVS Caremark, OptumRx, etc.)
- Realistic BIN/PCN numbers
- 15% claim rejection rate
- 9 common rejection codes (Prior Auth, Refill Too Soon, etc.)

### Data Relationships

```
Pharmacy Patient ←→ EHR Patient (matching on patient_id, demographics)
    ↓                        ↓
Prescriptions           Diagnoses
    ↓                        ↓
Transactions            Lab Results
    ↓                        ↓
Insurance               Clinical Notes
                             ↓
                        Immunizations
```

## Data Dictionary

### Pharmacy Patients
| Field | Type | Description |
|-------|------|-------------|
| patient_id | String | Unique identifier (PT00001) |
| first_name | String | Patient first name |
| last_name | String | Patient last name |
| date_of_birth | Date | YYYY-MM-DD format |
| age | Integer | Calculated age |
| gender | String | M, F, or X |
| ssn | String | XXX-XX-XXXX format |
| phone | String | (XXX) XXX-XXXX format |
| email | String | Valid email format |
| address | String | Street address |
| city | String | City name |
| state | String | 2-letter state code |
| zip_code | String | 5-digit ZIP code |
| conditions | String | Pipe-delimited conditions |
| drug_allergies | String | Pipe-delimited or NKDA |
| food_allergies | String | Pipe-delimited or None |
| created_date | Date | Account creation date |

### Prescriptions
| Field | Type | Description |
|-------|------|-------------|
| rx_number | String | Prescription number (RX00000001) |
| patient_id | String | Foreign key to patients |
| medication_name | String | Generic drug name |
| ndc | String | National Drug Code (11 digits) |
| quantity | Integer | Quantity dispensed |
| days_supply | Integer | Days supply |
| written_date | Date | Date prescribed |
| fill_date | Date | Date filled |
| refill_number | Integer | 0 for original, 1+ for refills |
| sig | String | Medication instructions |
| prescriber_npi | String | 10-digit NPI |
| copay | Decimal | Patient copayment amount |
| condition | String | Associated diagnosis |
| is_rems | String | Yes/No REMS flag |

### Insurance
| Field | Type | Description |
|-------|------|-------------|
| patient_id | String | Foreign key to patients |
| insurance_rank | String | Primary/Secondary |
| carrier_name | String | Insurance carrier name |
| rx_bin | String | 6-digit BIN number |
| rx_pcn | String | Processor Control Number |
| rx_group | String | Group number |
| cardholder_id | String | Member ID |
| person_code | String | 01-04 (self, spouse, child) |
| effective_date | Date | Coverage start date |
| termination_date | Date | Coverage end date (NULL if active) |

### Transactions
| Field | Type | Description |
|-------|------|-------------|
| transaction_id | String | Unique transaction ID |
| rx_number | String | Foreign key to prescriptions |
| patient_id | String | Foreign key to patients |
| fill_date | Date | Date of transaction |
| rx_bin | String | BIN submitted |
| rx_pcn | String | PCN submitted |
| rx_group | String | Group submitted |
| cardholder_id | String | Member ID submitted |
| ndc | String | NDC submitted |
| quantity | Integer | Quantity submitted |
| days_supply | Integer | Days supply submitted |
| submitted_amount | Decimal | Amount billed to insurance |
| paid_amount | Decimal | Amount paid by insurance |
| patient_pay | Decimal | Patient copay/coinsurance |
| status | String | Approved/Rejected |
| reject_code | String | Rejection code if rejected |
| reject_message | String | Rejection description |
| submission_clarification_code | String | Additional codes |
| transaction_timestamp | Timestamp | ISO 8601 format |

### Lab Results
| Field | Type | Description |
|-------|------|-------------|
| patient_id | String | Foreign key to patients |
| order_date | Date | Date test ordered |
| collection_date | Date | Date specimen collected |
| result_date | Date | Date results available |
| test_name | String | Test panel name |
| test_component | String | Specific component |
| result_value | Decimal | Numeric result |
| unit | String | Unit of measure |
| reference_range | String | Normal range |
| flag | String | Normal/Abnormal |
| ordering_provider_npi | String | Ordering provider NPI |
| performing_lab | String | Lab that performed test |

### Clinical Notes
| Field | Type | Description |
|-------|------|-------------|
| note_id | String | Unique note identifier |
| patient_id | String | Foreign key to patients |
| note_date | Date | Date of encounter |
| note_type | String | SOAP/Progress/Consultation |
| note_text | String | Full note text |
| author_npi | String | Author NPI |
| author_name | String | Author name |
| department | String | Clinical department |

## Validation

After generation, verify:
- [ ] All patient_ids match between pharmacy and EHR systems
- [ ] Prescription dates fall within 2024-2026 range
- [ ] Lab values respect reference ranges (except intentional aberrations)
- [ ] Insurance BIN/PCN formats are valid
- [ ] NDC codes are 11 digits with hyphens
- [ ] NPI numbers are 10 digits
- [ ] SSN format is XXX-XX-XXXX
- [ ] All CSV files are created without errors

## Customization

To modify the data generation:

**Change patient count**:
```python
NUM_PATIENTS = 500  # In both scripts
```

**Add new disease state**:
```python
DISEASE_MEDICATIONS = {
    'New Condition': {
        'medications': ['Drug1', 'Drug2'],
        'ndcs': ['12345-6789-01', '12345-6789-02'],
        'prevalence': 0.05,
        'age_factor': lambda age: 1.0
    }
}
```

**Adjust lab abnormality rates**:
```python
# In generate_labs() function
if num_conditions >= 3 and random.random() < 0.30:  # Changed from 0.20
    is_aberrant = True
```

## Next Steps

After generating data:
1. Review sample records from each CSV file
2. Verify data relationships
3. Proceed to Phase 2: Cloud Infrastructure Setup
4. Load data into GCP BigQuery and AWS S3/Athena

## Troubleshooting

**Import errors**:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Memory issues**:
- Reduce NUM_PATIENTS
- Process data in batches

**Data quality concerns**:
- Check seed values for reproducibility
- Review DISEASE_MEDICATIONS configuration
- Validate CSV output formatting
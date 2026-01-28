"""
Healthcare Data Generation - EHR System
Generates realistic synthetic EHR data including:
- Patient demographics (matching pharmacy system)
- Clinical notes (SOAP, progress, consultation)
- Laboratory results
- Diagnoses with ICD-10 codes
- Immunization records
- eMAR and CPOE records
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import json

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker('en_US')
Faker.seed(42)

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 1, 27)

# ICD-10 codes for conditions
ICD10_CODES = {
    'Hypertension': 'I10',
    'Type 2 Diabetes': 'E11.9',
    'Asthma': 'J45.909',
    'Hyperlipidemia': 'E78.5',
    'Depression': 'F33.1',
    'Anxiety Disorder': 'F41.9',
    'GERD': 'K21.9',
    'Hypothyroidism': 'E03.9',
    'Osteoarthritis': 'M19.90',
    'Chronic Pain': 'G89.29',
    'Schizophrenia': 'F20.9',
    'Severe Acne': 'L70.0',
    'Multiple Sclerosis': 'G35',
    'Migraine': 'G43.909',
    'Epilepsy': 'G40.909',
    'Rheumatoid Arthritis': 'M06.9',
    'COPD': 'J44.9',
    'Atrial Fibrillation': 'I48.91',
    'Heart Failure': 'I50.9',
    'Benign Prostatic Hyperplasia': 'N40.0',
    'Overactive Bladder': 'N32.81'
}

# Lab tests by condition
LAB_TESTS_BY_CONDITION = {
    'Hypertension': [
        ('Basic Metabolic Panel', 'Sodium', 135, 145, 'mmol/L'),
        ('Basic Metabolic Panel', 'Potassium', 3.5, 5.0, 'mmol/L'),
        ('Basic Metabolic Panel', 'Creatinine', 0.6, 1.2, 'mg/dL'),
        ('Lipid Panel', 'Total Cholesterol', 125, 200, 'mg/dL')
    ],
    'Type 2 Diabetes': [
        ('Hemoglobin A1C', 'HbA1c', 4.0, 5.6, '%'),
        ('Basic Metabolic Panel', 'Glucose', 70, 100, 'mg/dL'),
        ('Comprehensive Metabolic Panel', 'Creatinine', 0.6, 1.2, 'mg/dL'),
        ('Lipid Panel', 'Total Cholesterol', 125, 200, 'mg/dL'),
        ('Lipid Panel', 'Triglycerides', 0, 150, 'mg/dL')
    ],
    'Hyperlipidemia': [
        ('Lipid Panel', 'Total Cholesterol', 125, 200, 'mg/dL'),
        ('Lipid Panel', 'LDL', 0, 100, 'mg/dL'),
        ('Lipid Panel', 'HDL', 40, 60, 'mg/dL'),
        ('Lipid Panel', 'Triglycerides', 0, 150, 'mg/dL')
    ],
    'Chronic Pain': [
        ('Liver Function Tests', 'ALT', 7, 56, 'U/L'),
        ('Liver Function Tests', 'AST', 10, 40, 'U/L'),
        ('Complete Blood Count', 'WBC', 4.5, 11.0, 'K/uL')
    ],
    'Hypothyroidism': [
        ('Thyroid Function Tests', 'TSH', 0.4, 4.0, 'mIU/L'),
        ('Thyroid Function Tests', 'Free T4', 0.8, 1.8, 'ng/dL')
    ],
    'Rheumatoid Arthritis': [
        ('Inflammatory Markers', 'CRP', 0, 3.0, 'mg/L'),
        ('Inflammatory Markers', 'ESR', 0, 20, 'mm/hr'),
        ('Complete Blood Count', 'WBC', 4.5, 11.0, 'K/uL')
    ],
    'COPD': [
        ('Pulmonary Function', 'FEV1', 80, 120, '% predicted'),
        ('Arterial Blood Gas', 'pH', 7.35, 7.45, ''),
        ('Arterial Blood Gas', 'PaO2', 75, 100, 'mmHg')
    ],
    'Heart Failure': [
        ('Cardiac Markers', 'BNP', 0, 100, 'pg/mL'),
        ('Basic Metabolic Panel', 'Sodium', 135, 145, 'mmol/L'),
        ('Basic Metabolic Panel', 'Creatinine', 0.6, 1.2, 'mg/dL')
    ],
    'Atrial Fibrillation': [
        ('Coagulation Studies', 'INR', 0.8, 1.1, ''),
        ('Cardiac Markers', 'Troponin', 0, 0.04, 'ng/mL'),
        ('Thyroid Function Tests', 'TSH', 0.4, 4.0, 'mIU/L')
    ]
}

# Immunizations per ACIP guidelines
IMMUNIZATIONS = {
    'childhood': [
        ('DTaP', 'ages 2, 4, 6, 15-18 months, 4-6 years'),
        ('Hib', 'ages 2, 4, 6, 12-15 months'),
        ('Hepatitis B', 'birth, 1-2 months, 6-18 months'),
        ('MMR', 'ages 12-15 months, 4-6 years'),
        ('Varicella', 'ages 12-15 months, 4-6 years'),
        ('Polio', 'ages 2, 4, 6-18 months, 4-6 years')
    ],
    'adult': [
        ('Influenza', 'annually', 0.45),  # 45% coverage
        ('Td/Tdap', 'every 10 years', 0.26),  # 26% up to date
        ('Shingles', 'age 50+', 0.33),  # 33% of 50+
        ('Pneumococcal PPSV23', 'age 65+', 0.64),  # 64% of 65+
        ('COVID-19', 'per CDC guidance', 0.70)
    ]
}

def generate_labs(patient_id, conditions, age):
    """Generate lab results based on patient conditions"""
    labs = []
    
    # Determine number of condition-appropriate labs
    num_conditions = len(conditions)
    
    for condition in conditions:
        if condition not in LAB_TESTS_BY_CONDITION:
            continue
        
        test_list = LAB_TESTS_BY_CONDITION[condition]
        
        # Generate 2-4 lab results per year for patients with conditions
        num_labs = random.randint(2, 4)
        
        for _ in range(num_labs):
            test_date = START_DATE + timedelta(days=random.randint(0, 730))
            
            for test_name, component, min_val, max_val, unit in test_list:
                # Determine if this result should be aberrant
                is_aberrant = False
                
                # 5-15% aberration for patients with 3+ conditions
                if num_conditions >= 3 and random.random() < 0.20:
                    is_aberrant = True
                # 5% aberration for patients with 2 conditions
                elif num_conditions == 2 and random.random() < 0.10:
                    is_aberrant = True
                # 5% aberration for patients with 1 condition
                elif num_conditions == 1 and random.random() < 0.05:
                    is_aberrant = True
                
                if is_aberrant:
                    # Generate aberrant value
                    if random.random() < 0.5:
                        # Below range
                        value = round(random.uniform(min_val * 0.5, min_val * 0.95), 2)
                    else:
                        # Above range
                        value = round(random.uniform(max_val * 1.05, max_val * 1.5), 2)
                    flag = 'Abnormal'
                else:
                    # Normal range
                    value = round(random.uniform(min_val, max_val), 2)
                    flag = 'Normal'
                
                lab = {
                    'patient_id': patient_id,
                    'order_date': test_date.strftime('%Y-%m-%d'),
                    'collection_date': test_date.strftime('%Y-%m-%d'),
                    'result_date': (test_date + timedelta(days=random.randint(1, 3))).strftime('%Y-%m-%d'),
                    'test_name': test_name,
                    'test_component': component,
                    'result_value': value,
                    'unit': unit,
                    'reference_range': f"{min_val}-{max_val}",
                    'flag': flag,
                    'ordering_provider_npi': f"{random.randint(1000000000, 9999999999)}",
                    'performing_lab': random.choice(['Quest Diagnostics', 'LabCorp', 'Hospital Lab'])
                }
                labs.append(lab)
    
    return labs

def generate_clinical_note(patient_id, patient_name, age, gender, conditions, note_type='Progress'):
    """Generate realistic clinical notes"""
    
    condition_text = ', '.join(conditions[:3]) if conditions else 'routine visit'
    
    if note_type == 'SOAP':
        # Subjective
        subjective_templates = [
            f"Patient presents for follow-up of {condition_text}. Reports feeling generally well.",
            f"Patient seen for management of {condition_text}. No new complaints today.",
            f"{age}-year-old {gender} with history of {condition_text} presents for routine follow-up."
        ]
        subjective = random.choice(subjective_templates)
        
        # Objective
        vitals = f"BP {random.randint(110,140)}/{random.randint(70,90)}, HR {random.randint(60,90)}, " \
                f"RR {random.randint(12,20)}, Temp {round(random.uniform(97.8, 99.2), 1)}°F, " \
                f"O2 Sat {random.randint(95,100)}% on room air"
        
        objective = f"Vital Signs: {vitals}. General: Alert and oriented. Well-appearing. " \
                   f"Physical exam unremarkable for stated conditions."
        
        # Assessment
        assessment = f"Assessment: {', '.join([f'{c} - stable' for c in conditions[:2]])}" if conditions else "No acute concerns"
        
        # Plan
        plan_items = [
            "Continue current medications as prescribed",
            "Follow up in 3 months or sooner if concerns",
            "Reinforced medication adherence and lifestyle modifications"
        ]
        
        if 'Type 2 Diabetes' in conditions:
            plan_items.append("Recheck HbA1c in 3 months")
        if 'Hypertension' in conditions:
            plan_items.append("Monitor blood pressure at home")
        
        plan = "Plan: " + "; ".join(plan_items)
        
        note_text = f"SUBJECTIVE:\\n{subjective}\\n\\nOBJECTIVE:\\n{objective}\\n\\nASSESSMENT:\\n{assessment}\\n\\n{plan}"
    
    elif note_type == 'Progress':
        templates = [
            f"Progress Note:\\nPatient: {patient_name}, {age}yo {gender}\\n" \
            f"Chief Complaint: Follow-up {condition_text}\\n" \
            f"Patient continues management of {condition_text}. " \
            f"Current medications reviewed and refilled as appropriate. " \
            f"Patient counseled on importance of medication adherence and lifestyle modifications. " \
            f"No acute concerns at this time. Will continue current plan of care.",
            
            f"Visit Note:\\n{patient_name} seen today for {condition_text} management. " \
            f"Patient reports good adherence to medications. " \
            f"Reviewed recent lab results with patient. " \
            f"Plan to continue current regimen and follow up as scheduled."
        ]
        note_text = random.choice(templates)
    
    elif note_type == 'Consultation':
        specialist = random.choice(['Cardiology', 'Endocrinology', 'Pulmonology', 'Neurology'])
        note_text = f"Consultation Note - {specialist}\\n" \
                   f"Patient: {patient_name}, {age}yo {gender}\\n" \
                   f"Reason for Consultation: {condition_text}\\n\\n" \
                   f"Thank you for this consultation. I have reviewed the patient's history and examination. " \
                   f"Patient has been managing {condition_text}. " \
                   f"I recommend continuation of current therapy with close monitoring. " \
                   f"Will coordinate care with primary care provider."
    
    return note_text

def generate_immunizations(patient_id, age):
    """Generate immunization records based on ACIP guidelines"""
    immunizations = []
    
    # Assume 80% received all childhood vaccines
    if random.random() < 0.80:
        for vaccine, schedule in IMMUNIZATIONS['childhood']:
            # Add historical childhood vaccines
            admin_date = datetime.now() - timedelta(days=age*365) + timedelta(days=random.randint(90, 730))
            if admin_date < START_DATE:
                admin_date = START_DATE + timedelta(days=random.randint(0, 30))
            
            imm = {
                'patient_id': patient_id,
                'vaccine_name': vaccine,
                'cvx_code': f"{random.randint(1, 200):03d}",
                'administration_date': admin_date.strftime('%Y-%m-%d'),
                'dose_number': 1,
                'route': random.choice(['Intramuscular', 'Subcutaneous']),
                'site': random.choice(['Left deltoid', 'Right deltoid', 'Left thigh', 'Right thigh']),
                'lot_number': f"LOT{random.randint(100000, 999999)}",
                'manufacturer': random.choice(['Pfizer', 'Moderna', 'GSK', 'Merck', 'Sanofi']),
                'administered_by_npi': f"{random.randint(1000000000, 9999999999)}"
            }
            immunizations.append(imm)
    
    # Adult immunizations
    # Flu shot (45% coverage)
    if random.random() < 0.45:
        for year in [2024, 2025]:
            flu_date = datetime(year, random.randint(9, 11), random.randint(1, 28))
            if START_DATE <= flu_date <= END_DATE:
                imm = {
                    'patient_id': patient_id,
                    'vaccine_name': 'Influenza',
                    'cvx_code': '141',
                    'administration_date': flu_date.strftime('%Y-%m-%d'),
                    'dose_number': 1,
                    'route': 'Intramuscular',
                    'site': 'Left deltoid',
                    'lot_number': f"FLU{random.randint(100000, 999999)}",
                    'manufacturer': random.choice(['Sanofi', 'GSK', 'Seqirus']),
                    'administered_by_npi': f"{random.randint(1000000000, 9999999999)}"
                }
                immunizations.append(imm)
    
    # Tdap (26% up to date)
    if random.random() < 0.26:
        tdap_date = datetime.now() - timedelta(days=random.randint(0, 3650))  # Within 10 years
        if START_DATE <= tdap_date <= END_DATE:
            imm = {
                'patient_id': patient_id,
                'vaccine_name': 'Td/Tdap',
                'cvx_code': '115',
                'administration_date': tdap_date.strftime('%Y-%m-%d'),
                'dose_number': 1,
                'route': 'Intramuscular',
                'site': 'Left deltoid',
                'lot_number': f"TDAP{random.randint(100000, 999999)}",
                'manufacturer': random.choice(['Sanofi', 'GSK']),
                'administered_by_npi': f"{random.randint(1000000000, 9999999999)}"
            }
            immunizations.append(imm)
    
    # Shingles (33% of adults 50+)
    if age >= 50 and random.random() < 0.33:
        shingles_date = START_DATE + timedelta(days=random.randint(0, 730))
        imm = {
            'patient_id': patient_id,
            'vaccine_name': 'Shingles (Shingrix)',
            'cvx_code': '187',
            'administration_date': shingles_date.strftime('%Y-%m-%d'),
            'dose_number': 1,
            'route': 'Intramuscular',
            'site': 'Left deltoid',
            'lot_number': f"SHING{random.randint(100000, 999999)}",
            'manufacturer': 'GSK',
            'administered_by_npi': f"{random.randint(1000000000, 9999999999)}"
        }
        immunizations.append(imm)
    
    # Pneumococcal (64% of adults 65+)
    if age >= 65 and random.random() < 0.64:
        pneumo_date = START_DATE + timedelta(days=random.randint(0, 730))
        imm = {
            'patient_id': patient_id,
            'vaccine_name': 'Pneumococcal (PPSV23)',
            'cvx_code': '033',
            'administration_date': pneumo_date.strftime('%Y-%m-%d'),
            'dose_number': 1,
            'route': 'Intramuscular',
            'site': 'Left deltoid',
            'lot_number': f"PNEU{random.randint(100000, 999999)}",
            'manufacturer': 'Merck',
            'administered_by_npi': f"{random.randint(1000000000, 9999999999)}"
        }
        immunizations.append(imm)
    
    # COVID-19 (70% coverage)
    if random.random() < 0.70:
        covid_date = START_DATE + timedelta(days=random.randint(0, 730))
        imm = {
            'patient_id': patient_id,
            'vaccine_name': 'COVID-19',
            'cvx_code': '208',
            'administration_date': covid_date.strftime('%Y-%m-%d'),
            'dose_number': random.randint(1, 3),
            'route': 'Intramuscular',
            'site': 'Left deltoid',
            'lot_number': f"COVID{random.randint(100000, 999999)}",
            'manufacturer': random.choice(['Pfizer', 'Moderna']),
            'administered_by_npi': f"{random.randint(1000000000, 9999999999)}"
        }
        immunizations.append(imm)
    
    return immunizations

def main():
    """Main execution function"""
    print("=" * 60)
    print("HEALTHCARE DATA GENERATION - EHR SYSTEM")
    print("=" * 60)
    
    # Load pharmacy patient data to ensure matching demographics
    print("\n[1/6] Loading pharmacy patient data...")
    pharmacy_patients = pd.read_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/pharmacy_patients.csv', keep_default_na=False)
    print(f"   ✓ Loaded {len(pharmacy_patients)} patients from pharmacy system")
    
    # Create EHR patient demographics (matching pharmacy)
    print("\n[2/6] Creating EHR patient demographics...")
    ehr_patients = []
    for _, patient in pharmacy_patients.iterrows():
        ehr_patient = {
            'patient_id': patient['patient_id'],
            'first_name': patient['first_name'],
            'last_name': patient['last_name'],
            'date_of_birth': patient['date_of_birth'],
            'age': patient['age'],
            'gender': patient['gender'],
            'ssn': patient['ssn'],
            'phone': patient['phone'],
            'email': patient['email'],
            'address': patient['address'],
            'city': patient['city'],
            'state': patient['state'],
            'zip_code': patient['zip_code'],
            'created_date': patient['created_date']
        }
        ehr_patients.append(ehr_patient)
    
    ehr_patients_df = pd.DataFrame(ehr_patients)
    print(f"   ✓ Created {len(ehr_patients_df)} EHR patient records")
    
    # Generate diagnoses
    print("\n[3/6] Generating diagnoses...")
    diagnoses = []
    for _, patient in pharmacy_patients.iterrows():
        conditions = patient['conditions'].split('|') if patient['conditions'] != 'None' else []        
        for condition in conditions:
            if condition in ICD10_CODES:
                diagnosis = {
                    'patient_id': patient['patient_id'],
                    'diagnosis_code': ICD10_CODES[condition],
                    'diagnosis_description': condition,
                    'diagnosis_date': (START_DATE + timedelta(days=random.randint(-730, 0))).strftime('%Y-%m-%d'),
                    'status': random.choice(['Active', 'Active', 'Active', 'Resolved']),
                    'is_chronic': 'Yes' if condition in ['Hypertension', 'Type 2 Diabetes', 'Asthma'] else 'No',
                    'diagnosing_provider_npi': f"{random.randint(1000000000, 9999999999)}"
                }
                diagnoses.append(diagnosis)
    
    diagnoses_df = pd.DataFrame(diagnoses)
    print(f"   ✓ Generated {len(diagnoses_df)} diagnoses")
    
    # Generate lab results
    print("\n[4/6] Generating laboratory results...")
    all_labs = []
    for _, patient in pharmacy_patients.iterrows():
        conditions = patient['conditions'].split('|') if patient['conditions'] != 'NaN' else []
        if conditions and conditions[0] != 'None':
            patient_labs = generate_labs(patient['patient_id'], conditions, patient['age'])
            all_labs.extend(patient_labs)
    
    labs_df = pd.DataFrame(all_labs)
    print(f"   ✓ Generated {len(labs_df)} lab results")
    
    # Generate clinical notes
    print("\n[5/6] Generating clinical notes...")
    clinical_notes = []
    note_counter = 1
    for _, patient in pharmacy_patients.iterrows():
        conditions = patient['conditions'].split('|') if patient['conditions'] != 'None' else []
        if not conditions or conditions[0] == 'None':
            continue
        
        # Generate 3-6 notes per patient over 2 years
        num_notes = random.randint(3, 6)
        
        for _ in range(num_notes):
            note_date = START_DATE + timedelta(days=random.randint(0, 730))
            note_type = random.choice(['SOAP', 'SOAP', 'Progress', 'Progress', 'Consultation'])
            
            note_text = generate_clinical_note(
                patient['patient_id'],
                f"{patient['first_name']} {patient['last_name']}",
                patient['age'],
                patient['gender'],
                conditions,
                note_type
            )
            
            note = {
                'note_id': f"NOTE{note_counter:08d}",
                'patient_id': patient['patient_id'],
                'note_date': note_date.strftime('%Y-%m-%d'),
                'note_type': note_type,
                'note_text': note_text,
                'author_npi': f"{random.randint(1000000000, 9999999999)}",
                'author_name': fake.name(),
                'department': random.choice(['Primary Care', 'Internal Medicine', 'Family Medicine', 'Specialty Clinic'])
            }
            clinical_notes.append(note)
            note_counter += 1
    
    notes_df = pd.DataFrame(clinical_notes)
    print(f"   ✓ Generated {len(notes_df)} clinical notes")
    
    # Generate immunizations
    print("\n[6/6] Generating immunization records...")
    all_immunizations = []
    for _, patient in pharmacy_patients.iterrows():
        patient_imms = generate_immunizations(patient['patient_id'], patient['age'])
        all_immunizations.extend(patient_imms)
    
    immunizations_df = pd.DataFrame(all_immunizations)
    print(f"   ✓ Generated {len(immunizations_df)} immunization records")
    
    # Save all data
    print("\n[7/7] Saving data to CSV files...")
    ehr_patients_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/ehr_patients.csv', index=False)
    diagnoses_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/ehr_diagnoses.csv', index=False)
    labs_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/ehr_labs.csv', index=False)
    notes_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/ehr_clinical_notes.csv', index=False)
    immunizations_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/ehr_immunizations.csv', index=False)
    print("   ✓ All files saved successfully")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("EHR DATA GENERATION SUMMARY")
    print("=" * 60)
    print(f"Patients: {len(ehr_patients_df)}")
    print(f"Diagnoses: {len(diagnoses_df)}")
    print(f"Lab Results: {len(labs_df)}")
    abnormal_labs = len(labs_df[labs_df['flag'] == 'Abnormal'])
    print(f"  - Abnormal results: {abnormal_labs} ({abnormal_labs/len(labs_df)*100:.1f}%)")
    print(f"Clinical Notes: {len(notes_df)}")
    print(f"  - SOAP notes: {len(notes_df[notes_df['note_type']=='SOAP'])}")
    print(f"  - Progress notes: {len(notes_df[notes_df['note_type']=='Progress'])}")
    print(f"  - Consultation notes: {len(notes_df[notes_df['note_type']=='Consultation'])}")
    print(f"Immunizations: {len(immunizations_df)}")
    print("=" * 60)
    print("\nData generation complete!")
    print("Next step: Set up cloud infrastructure (GCP and AWS)")

if __name__ == "__main__":
    main()

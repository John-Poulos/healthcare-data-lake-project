"""
Healthcare Data Generation - Pharmacy System
Generates realistic synthetic pharmacy data including:
- Patient demographics
- Insurance information
- Prescription history
- Insurance adjudication transactions
- REMS medication tracking
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import json
import hashlib

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker('en_US')
Faker.seed(42)

# Configuration
NUM_PATIENTS = 250
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 1, 27)

# Age distribution (representative of US population)
AGE_DISTRIBUTION = {
    '13-17': 0.07,
    '18-24': 0.10,
    '25-34': 0.14,
    '35-44': 0.13,
    '45-54': 0.13,
    '55-64': 0.13,
    '65-74': 0.11,
    '75-84': 0.07,
    '85-97': 0.12
}

# Disease states with medications
DISEASE_MEDICATIONS = {
    'Hypertension': {
        'medications': ['Lisinopril', 'Amlodipine', 'Losartan', 'Metoprolol', 'Hydrochlorothiazide', 'Atenolol'],
        'ndcs': ['00603-5729-21', '00093-7369-98', '00093-7365-98', '00378-0520-93', '00172-4880-60', '00378-1050-01'],
        'prevalence': 0.29,  # 29% of adults
        'age_factor': lambda age: 1.5 if age > 45 else 0.5
    },
    'Type 2 Diabetes': {
        'medications': ['Metformin', 'Glipizide', 'Sitagliptin', 'Empagliflozin', 'Insulin Glargine', 'Dulaglutide'],
        'ndcs': ['00093-7214-01', '00093-7267-01', '00025-1489-31', '00597-0143-30', '00088-2220-33', '00002-8977-01'],
        'prevalence': 0.11,
        'age_factor': lambda age: 2.0 if age > 45 else 0.3
    },
    'Asthma': {
        'medications': ['Albuterol HFA', 'Fluticasone Prop HFA', 'Montelukast', 'Budesonide/Formoterol', 'Fluticasone/Salmeterol'],
        'ndcs': ['00173-0682-20', '00173-0862-00', '00093-7355-56', '00186-0791-60', '00173-0715-20'],
        'prevalence': 0.08,
        'age_factor': lambda age: 1.2 if age < 18 or age > 65 else 1.0
    },
    'Hyperlipidemia': {
        'medications': ['Atorvastatin', 'Rosuvastatin', 'Simvastatin', 'Pravastatin', 'Ezetimibe'],
        'ndcs': ['00071-0155-23', '00093-7663-98', '00093-7352-98', '00093-5108-98', '00093-7449-98'],
        'prevalence': 0.39,
        'age_factor': lambda age: 2.5 if age > 40 else 0.2
    },
    'Depression': {
        'medications': ['Sertraline', 'Escitalopram', 'Fluoxetine', 'Bupropion XL', 'Duloxetine', 'Venlafaxine ER'],
        'ndcs': ['00093-7212-01', '00093-5040-98', '00093-7198-56', '00591-5443-01', '00093-7383-56', '00093-7390-56'],
        'prevalence': 0.21,
        'age_factor': lambda age: 1.3 if 18 <= age <= 44 else 1.0
    },
    'Anxiety Disorder': {
        'medications': ['Alprazolam', 'Lorazepam', 'Buspirone', 'Hydroxyzine', 'Clonazepam'],
        'ndcs': ['00093-0253-01', '00054-4469-25', '00591-3440-01', '00054-3177-25', '00093-0832-01'],
        'prevalence': 0.19,
        'age_factor': lambda age: 1.2 if 18 <= age <= 54 else 0.9
    },
    'GERD': {
        'medications': ['Omeprazole', 'Pantoprazole', 'Esomeprazole', 'Lansoprazole', 'Famotidine'],
        'ndcs': ['00093-7267-56', '00093-5129-98', '00093-7711-28', '00093-2035-98', '00093-2748-01'],
        'prevalence': 0.20,
        'age_factor': lambda age: 1.5 if age > 50 else 0.8
    },
    'Hypothyroidism': {
        'medications': ['Levothyroxine 25mcg', 'Levothyroxine 50mcg', 'Levothyroxine 75mcg', 'Levothyroxine 100mcg'],
        'ndcs': ['00378-1805-10', '00378-1810-10', '00378-1815-10', '00378-1820-10'],
        'prevalence': 0.05,
        'age_factor': lambda age: 2.0 if age > 60 else 0.5
    },
    'Osteoarthritis': {
        'medications': ['Meloxicam', 'Celecoxib', 'Diclofenac Sodium', 'Naproxen', 'Tramadol'],
        'ndcs': ['00093-7407-01', '00071-0737-40', '00591-3699-01', '00093-0148-01', '00093-0058-01'],
        'prevalence': 0.14,
        'age_factor': lambda age: 3.0 if age > 65 else 0.3
    },
    'Chronic Pain': {
        'medications': ['Hydrocodone/APAP', 'Oxycodone/APAP', 'Morphine Sulfate ER', 'Tramadol', 'Gabapentin'],  # REMS opioids
        'ndcs': ['00406-0365-01', '00406-0512-01', '00406-8530-01', '00093-0058-01', '00093-0366-01'],
        'prevalence': 0.11,
        'age_factor': lambda age: 1.5 if age > 50 else 0.7,
        'rems': True
    },
    'Schizophrenia': {
        'medications': ['Olanzapine', 'Risperidone', 'Quetiapine', 'Aripiprazole', 'Clozapine'],  # Clozapine is REMS
        'ndcs': ['00093-7379-56', '00093-7243-28', '00093-7725-56', '00378-3890-93', '00378-0555-93'],
        'prevalence': 0.01,
        'age_factor': lambda age: 1.0,
        'rems': True  # Clozapine specifically
    },
    'Severe Acne': {
        'medications': ['Isotretinoin'],  # REMS required
        'ndcs': ['00406-1982-01'],
        'prevalence': 0.001,
        'age_factor': lambda age: 10.0 if 15 <= age <= 25 else 0.01,
        'rems': True
    },
    'Multiple Sclerosis': {
        'medications': ['Glatiramer Acetate', 'Dimethyl Fumarate', 'Fingolimod'],  # Fingolimod is REMS
        'ndcs': ['00781-5115-31', '00555-2020-02', '00078-0607-51'],
        'prevalence': 0.0003,
        'age_factor': lambda age: 2.0 if 20 <= age <= 60 else 0.1,
        'rems': True
    },
    'Migraine': {
        'medications': ['Sumatriptan', 'Topiramate', 'Propranolol', 'Amitriptyline', 'Rizatriptan'],
        'ndcs': ['00093-2250-11', '00093-5074-01', '00378-0499-01', '00093-0057-01', '00378-6090-93'],
        'prevalence': 0.12,
        'age_factor': lambda age: 1.5 if 20 <= age <= 55 else 0.7
    },
    'Epilepsy': {
        'medications': ['Levetiracetam', 'Lamotrigine', 'Valproic Acid', 'Carbamazepine', 'Phenytoin'],
        'ndcs': ['00093-5056-01', '00093-0160-01', '00378-1814-01', '00378-0321-01', '00378-0301-01'],
        'prevalence': 0.01,
        'age_factor': lambda age: 1.0
    },
    'Rheumatoid Arthritis': {
        'medications': ['Methotrexate', 'Hydroxychloroquine', 'Sulfasalazine', 'Adalimumab', 'Etanercept'],
        'ndcs': ['00054-0045-25', '00093-3114-01', '00378-6003-01', '00074-4339-02', '58406-0435-01'],
        'prevalence': 0.007,
        'age_factor': lambda age: 2.0 if age > 50 else 0.5
    },
    'COPD': {
        'medications': ['Tiotropium Bromide', 'Albuterol/Ipratropium', 'Fluticasone/Vilanterol', 'Umeclidinium/Vilanterol'],
        'ndcs': ['00597-0075-41', '00487-9001-99', '00173-0861-10', '00173-0857-10'],
        'prevalence': 0.06,
        'age_factor': lambda age: 5.0 if age > 65 else 0.2
    },
    'Atrial Fibrillation': {
        'medications': ['Apixaban', 'Rivaroxaban', 'Warfarin', 'Metoprolol', 'Diltiazem'],
        'ndcs': ['00003-0893-21', '50458-0597-10', '00378-3058-01', '00378-0520-93', '00378-0165-10'],
        'prevalence': 0.033,
        'age_factor': lambda age: 10.0 if age > 75 else 0.1
    },
    'Heart Failure': {
        'medications': ['Furosemide', 'Carvedilol', 'Spironolactone', 'Lisinopril', 'Sacubitril/Valsartan'],
        'ndcs': ['00378-0201-01', '00378-1805-01', '00378-0065-01', '00603-5729-21', '00078-0699-15'],
        'prevalence': 0.024,
        'age_factor': lambda age: 8.0 if age > 75 else 0.1
    },
    'Benign Prostatic Hyperplasia': {
        'medications': ['Tamsulosin', 'Finasteride', 'Dutasteride', 'Alfuzosin'],
        'ndcs': ['00093-7338-28', '00093-1087-01', '00591-3660-01', '00093-7520-28'],
        'prevalence': 0.14,  # Males only
        'age_factor': lambda age: 15.0 if age > 60 else 0.0,
        'gender': 'M'
    },
    'Overactive Bladder': {
        'medications': ['Oxybutynin', 'Tolterodine', 'Solifenacin', 'Mirabegron'],
        'ndcs': ['00378-0685-01', '00093-5147-56', '00093-7667-56', '00591-3752-30'],
        'prevalence': 0.16,
        'age_factor': lambda age: 3.0 if age > 65 else 0.5
    }
}

# Common drug allergies (representative prevalence)
COMMON_ALLERGIES = {
    'Penicillin': 0.10,
    'Sulfa drugs': 0.03,
    'Codeine': 0.02,
    'Aspirin': 0.02,
    'NSAIDs': 0.015,
    'Amoxicillin': 0.01,
    'Cephalosporins': 0.01
}

# Food allergies
FOOD_ALLERGIES = {
    'Peanuts': 0.02,
    'Tree nuts': 0.015,
    'Shellfish': 0.02,
    'Eggs': 0.013,
    'Milk': 0.026,
    'Soy': 0.004,
    'Wheat': 0.01,
    'Fish': 0.005
}

# Insurance carriers with realistic BIN/PCN
INSURANCE_CARRIERS = [
    {'name': 'Express Scripts', 'bin': '003858', 'pcn': 'MEDDADV', 'group_prefix': 'RX'},
    {'name': 'CVS Caremark', 'bin': '610020', 'pcn': 'CHOICE', 'group_prefix': 'CV'},
    {'name': 'OptumRx', 'bin': '610097', 'pcn': 'OPTUM', 'group_prefix': 'OP'},
    {'name': 'Humana', 'bin': '610455', 'pcn': 'PBM', 'group_prefix': 'HM'},
    {'name': 'Aetna', 'bin': '610455', 'pcn': 'A1', 'group_prefix': 'AE'},
    {'name': 'Blue Cross Blue Shield', 'bin': '610029', 'pcn': 'BCBS', 'group_prefix': 'BC'},
    {'name': 'Cigna', 'bin': '011506', 'pcn': 'CIGNA', 'group_prefix': 'CI'},
    {'name': 'United Healthcare', 'bin': '610020', 'pcn': 'UNITED', 'group_prefix': 'UN'},
    {'name': 'Medicare Part D', 'bin': '610455', 'pcn': 'MEDICARE', 'group_prefix': 'MD'},
    {'name': 'Medicaid', 'bin': '610014', 'pcn': 'MEDICAID', 'group_prefix': 'MC'}
]

# Insurance rejection codes
REJECTION_CODES = {
    'M1': 'Prior Authorization Required',
    'M2': 'Step Therapy Required',
    '75': 'Prior Authorization Required',
    '76': 'Plan Limitations Exceeded',
    '79': 'Refill Too Soon',
    '70': 'Product Not Covered',
    'NN': 'DUR Reject - Duplicate Therapy',
    '88': 'DUR Reject - Drug-Drug Interaction',
    'MR': 'Max Quantity Exceeded'
}

def generate_ssn():
    """Generate a valid-format SSN (not real)"""
    area = random.randint(1, 899)
    group = random.randint(1, 99)
    serial = random.randint(1, 9999)
    return f"{area:03d}-{group:02d}-{serial:04d}"

def generate_phone():
    """Generate US phone number"""
    area = random.randint(200, 999)
    exchange = random.randint(200, 999)
    number = random.randint(1000, 9999)
    return f"({area}) {exchange}-{number}"

def select_age_bracket():
    """Select age bracket based on US demographics"""
    brackets = list(AGE_DISTRIBUTION.keys())
    probabilities = list(AGE_DISTRIBUTION.values())
    bracket = np.random.choice(brackets, p=probabilities)
    
    # Generate age within bracket
    age_range = bracket.split('-')
    return random.randint(int(age_range[0]), int(age_range[1]))

def assign_conditions(age, gender):
    """Assign realistic conditions based on age and gender"""
    conditions = []
    
    for disease, info in DISEASE_MEDICATIONS.items():
        # Skip gender-specific conditions
        if 'gender' in info and info['gender'] != gender:
            continue
            
        # Calculate probability with age factor
        base_prevalence = info['prevalence']
        age_adjusted = base_prevalence * info['age_factor'](age)
        
        if random.random() < age_adjusted:
            conditions.append(disease)
    
    # Ensure at least 20% have multiple conditions
    if len(conditions) == 0 and random.random() < 0.5:
        # Assign at least one condition
        possible = [d for d, i in DISEASE_MEDICATIONS.items() 
                   if 'gender' not in i or i['gender'] == gender]
        conditions.append(random.choice(possible))
    
    return conditions

def generate_patient_demographics():
    """Generate patient demographic data"""
    patients = []
    
    for i in range(NUM_PATIENTS):
        age = select_age_bracket()
        birth_date = datetime.now() - timedelta(days=age*365.25)
        
        # Gender distribution
        gender = random.choice(['M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'X'])  # ~90% binary
        
        first_name = fake.first_name_male() if gender == 'M' else fake.first_name_female() if gender == 'F' else fake.first_name()
        last_name = fake.last_name()
        
        # Assign conditions
        conditions = assign_conditions(age, gender)
        
        # Assign allergies
        drug_allergies = [allergy for allergy, prob in COMMON_ALLERGIES.items() 
                         if random.random() < prob]
        food_allergies = [allergy for allergy, prob in FOOD_ALLERGIES.items() 
                         if random.random() < prob]
        
        patient = {
            'patient_id': f"PT{i+1:05d}",
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': birth_date.strftime('%Y-%m-%d'),
            'age': age,
            'gender': gender,
            'ssn': generate_ssn(),
            'phone': generate_phone(),
            'email': f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}",
            'address': fake.street_address(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'conditions': '|'.join(conditions) if conditions else 'None',
            'drug_allergies': '|'.join(drug_allergies) if drug_allergies else 'NKDA',
            'food_allergies': '|'.join(food_allergies) if food_allergies else 'None',
            'created_date': START_DATE.strftime('%Y-%m-%d')
        }
        
        patients.append(patient)
    
    return pd.DataFrame(patients)

def generate_insurance_profiles(patients_df):
    """Generate insurance information for each patient"""
    insurance_records = []
    
    for _, patient in patients_df.iterrows():
        # Number of insurance plans (1-3)
        num_plans = np.random.choice([1, 2, 3], p=[0.70, 0.25, 0.05])
        
        # Primary insurance
        carrier = random.choice(INSURANCE_CARRIERS)
        
        # Medicare for 65+
        if patient['age'] >= 65:
            carrier = [c for c in INSURANCE_CARRIERS if 'Medicare' in c['name']][0]
        # Medicaid for some younger
        elif patient['age'] < 65 and random.random() < 0.15:
            carrier = [c for c in INSURANCE_CARRIERS if 'Medicaid' in c['name']][0]
        
        insurance = {
            'patient_id': patient['patient_id'],
            'insurance_rank': 'Primary',
            'carrier_name': carrier['name'],
            'rx_bin': carrier['bin'],
            'rx_pcn': carrier['pcn'],
            'rx_group': f"{carrier['group_prefix']}{random.randint(10000, 99999)}",
            'cardholder_id': f"{random.randint(100000000, 999999999)}",
            'person_code': str(random.randint(1, 4)).zfill(2),
            'effective_date': START_DATE.strftime('%Y-%m-%d'),
            'termination_date': None
        }
        insurance_records.append(insurance)
        
        # Secondary insurance (if applicable)
        if num_plans >= 2:
            secondary_carrier = random.choice([c for c in INSURANCE_CARRIERS if c != carrier])
            insurance2 = {
                'patient_id': patient['patient_id'],
                'insurance_rank': 'Secondary',
                'carrier_name': secondary_carrier['name'],
                'rx_bin': secondary_carrier['bin'],
                'rx_pcn': secondary_carrier['pcn'],
                'rx_group': f"{secondary_carrier['group_prefix']}{random.randint(10000, 99999)}",
                'cardholder_id': f"{random.randint(100000000, 999999999)}",
                'person_code': str(random.randint(1, 4)).zfill(2),
                'effective_date': START_DATE.strftime('%Y-%m-%d'),
                'termination_date': None
            }
            insurance_records.append(insurance2)
    
    return pd.DataFrame(insurance_records)

def generate_prescriptions(patients_df):
    """Generate prescription history"""
    prescriptions = []
    rx_counter = 1
    
    for _, patient in patients_df.iterrows():
        conditions = patient['conditions'].split('|') if patient['conditions'] != 'None' else []
        
        if not conditions:
            continue
        
        # Each patient gets 8-16 prescriptions over 2 years
        num_prescriptions = random.randint(8, 16)
        
        for _ in range(num_prescriptions):
            # Select a condition and medication
            condition = random.choice(conditions)
            med_info = DISEASE_MEDICATIONS[condition]
            med_idx = random.randint(0, len(med_info['medications'])-1)
            medication_name = med_info['medications'][med_idx]
            ndc = med_info['ndcs'][med_idx]
            
            # Generate prescription dates
            written_date = START_DATE + timedelta(days=random.randint(0, 730))
            fill_date = written_date + timedelta(days=random.randint(0, 7))
            
            # Quantity and days supply
            if 'inhaler' in medication_name.lower() or 'hfa' in medication_name.lower():
                quantity = 1
                days_supply = 30
            elif 'insulin' in medication_name.lower():
                quantity = random.choice([1, 3, 5])
                days_supply = 30
            else:
                # 5% aberrant dosing
                if random.random() < 0.05:
                    quantity = random.randint(1, 500)  # Aberrant
                    days_supply = random.randint(1, 180)
                else:
                    quantity = random.choice([30, 60, 90])
                    days_supply = quantity
            
            # Instructions (SIG)
            sigs = [
                "Take 1 tablet by mouth daily",
                "Take 1 tablet by mouth twice daily",
                "Take 1 capsule by mouth once daily",
                "Take 2 tablets by mouth twice daily",
                "Inhale 2 puffs twice daily",
                "Apply topically as directed",
                "Take 1 tablet by mouth at bedtime",
                "Take 1-2 tablets by mouth every 4-6 hours as needed",
                "Inject subcutaneously as directed"
            ]
            sig = random.choice(sigs)
            
            # Copay
            copay = round(random.uniform(5, 75), 2)
            if 'rems' in med_info and med_info.get('rems'):
                copay = round(random.uniform(50, 500), 2)  # Specialty meds more expensive
            
            prescription = {
                'rx_number': f"RX{rx_counter:08d}",
                'patient_id': patient['patient_id'],
                'medication_name': medication_name,
                'ndc': ndc,
                'quantity': quantity,
                'days_supply': days_supply,
                'written_date': written_date.strftime('%Y-%m-%d'),
                'fill_date': fill_date.strftime('%Y-%m-%d'),
                'refill_number': 0,
                'sig': sig,
                'prescriber_npi': f"{random.randint(1000000000, 9999999999)}",
                'copay': copay,
                'condition': condition,
                'is_rems': 'Yes' if med_info.get('rems', False) else 'No'
            }
            prescriptions.append(prescription)
            rx_counter += 1
            
            # Add refills (1-3 refills for maintenance meds)
            if condition in ['Hypertension', 'Type 2 Diabetes', 'Hyperlipidemia', 'Hypothyroidism']:
                num_refills = random.randint(1, 3)
                for refill in range(1, num_refills + 1):
                    refill_date = fill_date + timedelta(days=days_supply * refill)
                    if refill_date > END_DATE:
                        break
                    
                    refill_rx = prescription.copy()
                    refill_rx['fill_date'] = refill_date.strftime('%Y-%m-%d')
                    refill_rx['refill_number'] = refill
                    prescriptions.append(refill_rx)
    
    return pd.DataFrame(prescriptions)

def generate_adjudication_transactions(prescriptions_df, insurance_df):
    """Generate insurance adjudication transactions"""
    transactions = []
    
    for _, rx in prescriptions_df.iterrows():
        # Get patient's primary insurance
        patient_insurance = insurance_df[
            (insurance_df['patient_id'] == rx['patient_id']) & 
            (insurance_df['insurance_rank'] == 'Primary')
        ]
        
        if patient_insurance.empty:
            continue
        
        insurance = patient_insurance.iloc[0]
        
        # 15% rejection rate
        is_rejected = random.random() < 0.15
        
        if is_rejected:
            reject_code = random.choice(list(REJECTION_CODES.keys()))
            reject_message = REJECTION_CODES[reject_code]
            status = 'Rejected'
            paid_amount = 0.0
        else:
            reject_code = None
            reject_message = None
            status = 'Approved'
            # AWP minus discount
            awp = round(random.uniform(50, 800), 2)
            paid_amount = round(awp * random.uniform(0.70, 0.95), 2)
        
        transaction = {
            'transaction_id': f"TXN{hash(rx['rx_number'] + rx['fill_date']) % 10000000:07d}",
            'rx_number': rx['rx_number'],
            'patient_id': rx['patient_id'],
            'fill_date': rx['fill_date'],
            'rx_bin': insurance['rx_bin'],
            'rx_pcn': insurance['rx_pcn'],
            'rx_group': insurance['rx_group'],
            'cardholder_id': insurance['cardholder_id'],
            'ndc': rx['ndc'],
            'quantity': rx['quantity'],
            'days_supply': rx['days_supply'],
            'submitted_amount': round(random.uniform(50, 800), 2),
            'paid_amount': paid_amount,
            'patient_pay': rx['copay'],
            'status': status,
            'reject_code': reject_code,
            'reject_message': reject_message,
            'submission_clarification_code': None,
            'transaction_timestamp': rx['fill_date'] + 'T' + f"{random.randint(8,20):02d}:{random.randint(0,59):02d}:00"
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def main():
    """Main execution function"""
    print("=" * 60)
    print("HEALTHCARE DATA GENERATION - PHARMACY SYSTEM")
    print("=" * 60)
    
    print("\n[1/5] Generating patient demographics...")
    patients_df = generate_patient_demographics()
    print(f"   ✓ Generated {len(patients_df)} patients")
    
    print("\n[2/5] Generating insurance profiles...")
    insurance_df = generate_insurance_profiles(patients_df)
    print(f"   ✓ Generated {len(insurance_df)} insurance records")
    
    print("\n[3/5] Generating prescriptions...")
    prescriptions_df = generate_prescriptions(patients_df)
    print(f"   ✓ Generated {len(prescriptions_df)} prescriptions")
    rems_count = len(prescriptions_df[prescriptions_df['is_rems'] == 'Yes'])
    print(f"   ✓ REMS medications: {rems_count}")
    
    print("\n[4/5] Generating insurance adjudication transactions...")
    transactions_df = generate_adjudication_transactions(prescriptions_df, insurance_df)
    print(f"   ✓ Generated {len(transactions_df)} transactions")
    rejected = len(transactions_df[transactions_df['status'] == 'Rejected'])
    print(f"   ✓ Rejected claims: {rejected} ({rejected/len(transactions_df)*100:.1f}%)")
    
    print("\n[5/5] Saving data to CSV files...")
    patients_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/pharmacy_patients.csv', index=False)
    insurance_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/pharmacy_insurance.csv', index=False)
    prescriptions_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/pharmacy_prescriptions.csv', index=False)
    transactions_df.to_csv('/Users/jpoul/OneDrive/Documents/CS Development/Source/Pharmacy/healthcare-data-lake-project/data_generation/pharmacy_transactions.csv', index=False)
    print("   ✓ All files saved successfully")
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("DATA GENERATION SUMMARY")
    print("=" * 60)
    print(f"Patients: {len(patients_df)}")
    print(f"  - With conditions: {len(patients_df[patients_df['conditions'] != 'None'])}")
    print(f"  - With drug allergies: {len(patients_df[patients_df['drug_allergies'] != 'NKDA'])}")
    print(f"Insurance Records: {len(insurance_df)}")
    print(f"Prescriptions: {len(prescriptions_df)}")
    print(f"  - REMS medications: {rems_count}")
    print(f"  - Average per patient: {len(prescriptions_df)/len(patients_df):.1f}")
    print(f"Transactions: {len(transactions_df)}")
    print(f"  - Approved: {len(transactions_df[transactions_df['status']=='Approved'])}")
    print(f"  - Rejected: {rejected}")
    print("=" * 60)
    print("\nNext step: Run generate_ehr_data.py")

if __name__ == "__main__":
    main()

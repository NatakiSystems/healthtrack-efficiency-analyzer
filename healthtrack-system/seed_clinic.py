import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from faker import Faker
from database import SessionLocal, engine, DBModelBase
from models import Patient, Appointment

# Initialize our tools
fake = Faker()
session = SessionLocal()
DBModelBase.metadata.create_all(bind=engine) # This creates the tables in healthtrack.db

def seed_data():
    # --- STEP 1: GENERATE 300 PATIENT PROFILES ---
    patients_list = []
    base_no_show_rate = 0.15

    for _ in range(300):
        # Generate random patient details
        age = random.randint(18, 80)
        primary_issue = random.choice(['Checkup', 'Follow-up', 'Procedure', 'Consultation'])
        
        # Calculate the special no-show probability based on Case Study rules
        no_show_prob = base_no_show_rate
        
        # Rule: Patients over 60 are more reliable (multiply rate by 70%)
        if age > 60:
            no_show_prob *= 0.7
            
        # Rule: Random gender adjustment (if > 0.5, multiply rate by 120%)
        if np.random.random() > 0.5:
            no_show_prob *= 1.2 # 
            
        # Format the final probability using Numpy's uniform method
        # Low of 0.8, High of 1.2, Size of 0.3 
        variation = np.random.uniform(0.8, 1.2)
        final_prob = no_show_prob * variation
        
        # Create the Patient object
        new_patient = Patient(
            name=fake.name(),
            age=age,
            primary_issue=primary_issue,
            no_show_probability=round(final_prob, 2)
        )
        
        session.add(new_patient)
        patients_list.append(new_patient)

    session.commit() # Save the 300 patients to the database
    print("Successfully created 300 patient profiles!")

    # --- STEP 2: GENERATE 60 DAYS OF APPOINTMENTS ---
    slots = ['9:00AM', '10:00AM', '11:00AM', '1:00PM', '2:00PM', '3:00PM', '4:00PM']
    
    # Duration rules from Case Study 
    duration_rules = {
        'Checkup': {'base': 20, 'var': 10},
        'Follow-up': {'base': 15, 'var': 5},
        'Procedure': {'base': 45, 'var': 25},
        'Consultation': {'base': 30, 'var': 15}
    }

    start_date = datetime.now() 
    for day_offset in range(60):
        current_date = start_date + timedelta(days=day_offset)
        day_name = current_date.strftime("%A")

        # Fewer appointments on weekends
        is_weekend = day_name in ['Saturday', 'Sunday']
        
        for slot in slots:
            # Generate random number of appointments
            num_apps = random.randint(1, 2) if is_weekend else random.randint(3, 5)
            
            for _ in range(num_apps):
                p = random.choice(patients_list)
                rules = duration_rules[p.primary_issue]
                
                # Scheduled vs Actual Duration 
                sched_dur = rules['base']
                # Actual duration uses max(10, base + random variation) 
                actual_dur = max(10, rules['base'] + random.randint(-rules['var'], rules['var']))
                
                # Special Afternoon No-Show Logic 
                current_no_show_prob = p.no_show_probability
                if slot in ['3:00PM', '4:00PM']:
                    if random.random() > (current_no_show_prob * 1.3):
                        current_no_show_prob *= 1.5 # Simulating higher afternoon no-shows
                
                show_up = random.random() > current_no_show_prob

                new_app = Appointment(
                    id=str(uuid.uuid4()), # Professional UUID generation 
                    date=current_date,
                    day_of_week=day_name,
                    time_slot=slot,
                    patient_id=p.id,
                    appointment_type=p.primary_issue,
                    scheduled_duration=sched_dur,
                    actual_duration=actual_dur,
                    show_up_status=show_up,
                    duration_difference=actual_dur - sched_dur
                )
                session.add(new_app)
    
    session.commit()
    print("Successfully created 60 days of Appointment Data!")
    seed_data()
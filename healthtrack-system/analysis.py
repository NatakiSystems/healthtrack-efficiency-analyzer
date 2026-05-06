import pandas as pd

def perform_audit():
    # 1. Load the CSV file created in Phase 1
    df = pd.read_csv("healthtrack_data.csv")
    
    print("\n" + "="*60)
    print(" ANCHORPOINT VIRTUAL SERVICES: CLINICAL PERFORMANCE AUDIT")
    print("="*60)
    
    # REQUIREMENT 1: No-Show Patterns (Heatmap Data)
    # Instructions ask for no-show rates by time and type 
    # Math: (1 - average of show_up_status) gives us the no-show rate.
    no_show_rate = 1 - df.groupby(['time_slot', 'appointment_type'])['show_up_status'].mean()
    print("\n[REPORT 1] NO-SHOW RATES BY TIME & TYPE:")
    print(no_show_rate.unstack().round(2))

    # REQUIREMENT 2: Actual Duration Analysis
    # Comparison of scheduled vs actual durations 
    duration_audit = df.groupby('appointment_type')[['scheduled_duration', 'actual_duration']].mean()
    print("\n[REPORT 2] DURATION VARIANCE ANALYSIS (Minutes):")
    print(duration_audit.round(1))

    # REQUIREMENT 3: Clinic Utilization Timeline
    # How effectively time slots are used 
    # We use 'appointment_id' because that is the name required in your Case Study [cite: 9]
    utilization_trend = df.groupby('time_slot')['appointment_id'].count()
    print("\n[REPORT 3] DAILY UTILIZATION BY TIME SLOT:")
    print(utilization_trend)
    print("\n" + "="*60)

# This is the "Ignition Switch" that runs the code
if __name__ == "__main__":
    perform_audit()
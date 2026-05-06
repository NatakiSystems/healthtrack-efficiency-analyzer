import pandas as pd
from database import engine

def main():
    print("Connecting to database...")
    # Load the appointments table into a Pandas DataFrame
    df = pd.read_sql_table("appointments", con=engine)
    
    # Export it to a CSV file
    df.to_csv("healthtrack_data.csv", index=False)
    print("Successfully exported healthtrack_data.csv!")

if __name__ == "__main__":
    main()
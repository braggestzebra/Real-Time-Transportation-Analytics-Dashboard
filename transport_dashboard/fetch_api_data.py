import requests
import sqlite3
import pandas as pd
import time

# Example of using a public transportation API (e.g., Transport for London)
# Note: Replace 'API_KEY' with your actual API key if required

API_URL = 'https://api.tfl.gov.uk/Line/Mode/tube/Status?detail=true'

def fetch_data():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Error fetching data', response.status_code)
        return None

def create_table_if_not_exists(data):
    conn = sqlite3.connect("transportation.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transportation_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route TEXT,
            distance REAL,
            duration INTEGER,
            revenue REAL,
            booking_count INTEGER,
            date TEXT
        )
    """)

    for item in data[:10]:  # Insert only the first 10 records
        cursor.execute("""
            INSERT INTO transportation_data (route, distance, duration, revenue, booking_count, date)
            VALUES (?, ?, ?, ?, ?, ?) 
        """, (item.get('name', 'Unknown Route'), 15.0, 30, 200, 50, "2025-03-05"))

        

    # Commit and close
    conn.commit()
    conn.close()
    print("Real-Time Data Inserted into Database")

# Run the functions
if __name__ == "__main__":
    data = fetch_data()
    if data:
        create_table_if_not_exists(data)
        print("API is working. Here is a sample of the data:")
        print(data[:2])  # Print the first 2 items for a quick check
    else:
        print("API is not working.")
  
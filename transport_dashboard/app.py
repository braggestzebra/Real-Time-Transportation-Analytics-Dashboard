from flask import Flask, render_template
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

if not os.path.exists("static"):
    os.makedirs("static")

def get_latest_data():
    conn = sqlite3.connect("transportation.db")
    df = pd.read_sql("SELECT * FROM transportation_data ORDER BY id DESC LIMIT 10", conn)
    conn.close()
    return df

@app.route('/')
def dashboard():
    df = get_latest_data()

    plt.figure(figsize=(10, 6))
    df.groupby('route')['revenue'].sum().plot(kind='bar')
    plt.xlabel('Route')
    plt.ylabel('Total Revenue')
    plt.title('Real time Revenue by Route')
    plt.savefig('static/total_revenue_chart.png') 

    return render_template("dashboard.html", chart="static/total_revenue_chart.png", data=df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

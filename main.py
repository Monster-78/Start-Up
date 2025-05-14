import subprocess
import os

# Step 1: Run EDA Script (This will clean data and save cleaned_investments.csv)
print("🔍 Running EDA script...")
print("⏳Cool Wait Data Is Under Process.....⏰")
print("🍿Having Some Snacks....🍿")
subprocess.run(["python", "EDA.py"])

# Step 2: Launch Streamlit Dashboard
print("🚀 Launching Streamlit Dashboard...")
os.system("streamlit run startup_dashboard.py")

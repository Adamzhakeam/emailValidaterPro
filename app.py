"""
Flask API for Water Quality Sensor Data
Provides real-time sensor data to the frontend
"""

from flask import Flask, jsonify
from flask_cors import CORS
import threading
import kisa_utils as kutils 

import time
from water_sensor_simulator import WaterSensorSimulator
from data_store import DataStore

from flask import Flask, jsonify, request
app = Flask(__name__)

# Enable CORS for local dev, Docker, and production deployments
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",  # Allow all origins for easier deployment (adjust for production security if needed)
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Accept", "Content-Type", "Authorization", "Cache-Control"],
            "expose_headers": ["Content-Type"],
            "supports_credentials": False,
        }
    },
)

# Remove custom CORS header injection; Flask-CORS will set the correct single-origin header

# Initialize components
simulator = WaterSensorSimulator(noise_level=0.05)
data_store = DataStore("sensor_data.json")

def update_sensor_data():
    """Background task to update sensor data every 60 seconds"""
    while True:
        try:
            # Generate a new reading (scenario will be randomly selected)
            reading = simulator.generate_reading()
            
            # Store the reading
            data_store.add_reading(reading)
            
            # Print status
            print("\n📊 New reading generated:")
            print(f"   Location: {reading['location']}")
            print(f"   Status: {reading['name']}")
            print(f"   Time: {reading['timestamp']}")
            print(f"   Readings:")
            print(f"     • pH: {reading['data']['ph']:.1f}")
            print(f"     • Turbidity: {reading['data']['turbidity_ntu']:.1f} NTU")
            print(f"     • E.coli: {reading['data']['e_coli_ctu_100ml']} CFU/100mL")
            print(f"     • Chlorine: {reading['data']['residual_chlorine_mg_l']:.2f} mg/L")
            print("-" * 80)
            
        except Exception as e:
            print(f"⚠️ Error updating sensor data: {e}")
            import traceback
            traceback.print_exc()
        
        time.sleep(60)  # Wait for 60 seconds before next update

# Start the background data update thread
update_thread = threading.Thread(target=update_sensor_data, daemon=True)
update_thread.start()

@app.route('/api/latest', methods=['GET'])
def get_latest_reading():
    """Get the latest sensor reading"""
    try:
        reading = data_store.get_latest_reading()
        return jsonify(reading)
    except Exception as e:
        print(f"⚠️ Error getting latest reading: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/historical', methods=['GET'])
def get_historical_readings():
    """Get historical readings"""
    try:
        readings = data_store.get_historical_readings()
        return jsonify(readings)
    except Exception as e:
        print(f"⚠️ Error getting historical readings: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    try:
        alerts = data_store.get_alerts()
        return jsonify(alerts)
    except Exception as e:
        print(f"⚠️ Error getting alerts: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


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
    """Background task to update sensor data for all locations every 60 seconds"""
    while True:
        try:
            # Generate readings for all 7 locations
            all_scenarios = ["clean", "turbid", "contaminated", "industrial", "reservoir", "pump_kurambiro", "pump_lubigi"]
            
            print(f"\n📊 Generating readings for all {len(all_scenarios)} locations:")
            print("=" * 80)
            
            for scenario in all_scenarios:
                # Generate a reading for this specific scenario
                reading = simulator.generate_reading(scenario)
                
                # Store the reading
                data_store.add_reading(reading)
                
                # Print status for this location
                print(f"📍 {reading['location']}:")
                print(f"   Status: {reading['name']}")
                print(f"   pH: {reading['data']['ph']:.1f} | Turbidity: {reading['data']['turbidity_ntu']:.1f} NTU")
                print(f"   E.coli: {reading['data']['e_coli_ctu_100ml']} CFU/100mL | Chlorine: {reading['data']['residual_chlorine_mg_l']:.2f} mg/L")
                print("-" * 40)
            
            print(f"✅ Generated readings for all {len(all_scenarios)} locations")
            print("=" * 80)
            
        except Exception as e:
            print(f"⚠️ Error updating sensor data: {e}")
            import traceback
            traceback.print_exc()
        
        time.sleep(60)  # Wait for 60 seconds before next update

# Start the background data update thread
update_thread = threading.Thread(target=update_sensor_data, daemon=True)
update_thread.start()

@app.route('/', methods=['GET'])
def root():
    """Root endpoint to prevent 404 errors"""
    return jsonify({
        "message": "Water Quality Monitoring API",
        "version": "1.0.0",
        "endpoints": {
            "latest": "/api/latest",
            "historical": "/api/historical", 
            "alerts": "/api/alerts",
            "all_locations": "/api/all-locations"
        },
        "status": "active",
        "description": "Generates data for 7 locations every 60 seconds"
    })

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

@app.route('/api/all-locations', methods=['GET'])
def get_all_locations():
    """Get latest readings from all locations"""
    try:
        # Get the last 7 readings (one for each location)
        all_readings = data_store.get_historical_readings(limit=7)
        
        # Group by location to get the latest from each
        location_data = {}
        for reading in all_readings:
            location = reading.get('location', 'Unknown')
            if location not in location_data:
                location_data[location] = reading
        
        # Convert to list format
        result = list(location_data.values())
        
        return jsonify({
            "locations": result,
            "count": len(result),
            "timestamp": result[0]['timestamp'] if result else None
        })
    except Exception as e:
        print(f"⚠️ Error getting all locations: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


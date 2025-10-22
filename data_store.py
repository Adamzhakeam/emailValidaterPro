"""
Data store for water quality sensor readings
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class DataStore:
    def __init__(self, json_file: str = "sensor_data.json"):
        self.json_file = json_file
        self.data = {
            "latest_reading": None,
            "historical_readings": [],
            "alerts": []
        }
        self._load_data()

    def _load_data(self):
        """Load existing data from JSON file"""
        # Default structure
        default_data = {
            "latest_reading": None,
            "historical_readings": [],
            "alerts": []
        }
        
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    # Merge loaded data with default structure to ensure all keys exist
                    self.data = {**default_data, **loaded_data}
                print(f"📊 Loaded {len(self.data['historical_readings'])} historical readings")
            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ Error loading data file, starting fresh: {e}")
                self.data = default_data
        else:
            print("📝 Creating new data store")
            self.data = default_data

    def _save_data(self):
        """Save current data to JSON file"""
        try:
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving data: {e}")

    def add_reading(self, reading: Dict[str, Any]):
        """Add a new sensor reading"""
        # Update latest reading
        self.data["latest_reading"] = reading

        # Add to historical readings (keep last 1000 readings)
        self.data["historical_readings"].append(reading)
        if len(self.data["historical_readings"]) > 1000:
            self.data["historical_readings"] = self.data["historical_readings"][-1000:]

        # Check for alerts
        self._check_alerts(reading)

        # Save to file
        self._save_data()

    def _check_alerts(self, reading: Dict[str, Any]):
        """Check reading for alert conditions"""
        data = reading["data"]
        timestamp = reading["timestamp"]
        alerts = []

        # Critical alerts
        if data["e_coli_ctu_100ml"] > 100:
            alerts.append({
                "level": "critical",
                "type": "biological",
                "message": f"High E.coli levels detected: {data['e_coli_ctu_100ml']} CFU/100mL"
            })

        if data["turbidity_ntu"] > 30:
            alerts.append({
                "level": "critical",
                "type": "physical",
                "message": f"Critical turbidity levels: {data['turbidity_ntu']} NTU"
            })

        if data["ph"] < 5 or data["ph"] > 9:
            alerts.append({
                "level": "critical",
                "type": "chemical",
                "message": f"pH out of safe range: {data['ph']}"
            })

        if data["total_coliforms_ctu_100ml"] > 50:
            alerts.append({
                "level": "critical",
                "type": "biological",
                "message": f"High total coliforms: {data['total_coliforms_ctu_100ml']} CFU/100mL"
            })

        # Warning alerts
        if data["turbidity_ntu"] > 10 and data["turbidity_ntu"] <= 30:
            alerts.append({
                "level": "warning",
                "type": "physical",
                "message": f"Elevated turbidity: {data['turbidity_ntu']} NTU"
            })

        if data["residual_chlorine_mg_l"] < 0.2:
            alerts.append({
                "level": "warning",
                "type": "chemical",
                "message": f"Low residual chlorine: {data['residual_chlorine_mg_l']} mg/L"
            })

        if data["ph"] < 6.5 or data["ph"] > 8.5:
            alerts.append({
                "level": "warning",
                "type": "chemical",
                "message": f"pH outside optimal range: {data['ph']}"
            })

        if data["iron_fe_mg_l"] > 0.3:
            alerts.append({
                "level": "warning",
                "type": "chemical",
                "message": f"High iron content: {data['iron_fe_mg_l']} mg/L"
            })

        if data["manganese_mn_mg_l"] > 0.1:
            alerts.append({
                "level": "warning",
                "type": "chemical",
                "message": f"Elevated manganese: {data['manganese_mn_mg_l']} mg/L"
            })

        if data["ammonia_nh3_mg_l"] > 0.5:
            alerts.append({
                "level": "warning",
                "type": "chemical",
                "message": f"High ammonia levels: {data['ammonia_nh3_mg_l']} mg/L"
            })

        # Add alerts with timestamp and location
        for alert in alerts:
            alert["timestamp"] = timestamp
            alert["location"] = reading["location"]
            self.data["alerts"].append(alert)

        # Keep last 100 alerts
        if len(self.data["alerts"]) > 100:
            self.data["alerts"] = self.data["alerts"][-100:]

    def get_latest_reading(self) -> Optional[Dict[str, Any]]:
        """Get the most recent sensor reading"""
        return self.data["latest_reading"]

    def get_historical_readings(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get historical readings with optional limit"""
        readings = self.data["historical_readings"]
        return readings[-limit:] if limit else readings

    def get_alerts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent alerts with optional limit"""
        alerts = self.data["alerts"]
        return alerts[-limit:] if limit else alerts

    def clear_data(self):
        """Clear all stored data"""
        self.data = {
            "latest_reading": None,
            "historical_readings": [],
            "alerts": []
        }
        self._save_data()


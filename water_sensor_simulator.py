"""
Water Quality Sensor Data Simulator
Generates synthetic water quality sensor readings with realistic variations
"""

import random
import time
from typing import Dict, Any, Optional
import kisa_utils as kutils

class WaterSensorSimulator:
    """Simulates water quality sensor readings"""

    # Define baseline scenarios with typical ranges
    SCENARIOS = {
        "clean": {
            "name": "✅ CLEAN DRINKING WATER",
            "location": "Ggaba III Plant",
            "ranges": {
                'temperature_c': (20.0, 25.0),
                'turbidity_ntu': (0.5, 3.0),
                'electrical_conductivity_us_cm': (500.0, 800.0),
                'total_suspended_solids_mg_l': (1.0, 5.0),
                'ph': (7.0, 8.0),
                'residual_chlorine_mg_l': (0.2, 0.6),
                'dissolved_oxygen_mg_l': (7.0, 9.0),
                'nitrates_no3_mg_l': (2.0, 8.0),
                'nitrites_no2_mg_l': (0.01, 0.05),
                'ammonia_nh3_mg_l': (0.05, 0.15),
                'phosphates_po4_mg_l': (0.05, 0.20),
                'hardness_mg_l': (80.0, 150.0),
                'iron_fe_mg_l': (0.05, 0.15),
                'manganese_mn_mg_l': (0.01, 0.05),
                'e_coli_ctu_100ml': (0, 0),
                'faecal_coliforms_ctu_100ml': (0, 0),
                'total_coliforms_ctu_100ml': (0, 1),
                'water_pressure_bar': (3.0, 4.0),
                'flow_rate_l_s': (20.0, 28.0),
                'alkalinity_mgL': (80.0, 120.0),
                'color_ptco': (5.0, 15.0)
            }
        },
        "turbid": {
            "name": "🌀 HIGH TURBIDITY WATER",
            "location": "Nakasero Hill Tank",
            "ranges": {
                'temperature_c': (22.0, 27.0),
                'turbidity_ntu': (15.0, 35.0),
                'electrical_conductivity_us_cm': (800.0, 1200.0),
                'total_suspended_solids_mg_l': (20.0, 50.0),
                'ph': (6.5, 7.5),
                'residual_chlorine_mg_l': (0.1, 0.3),
                'dissolved_oxygen_mg_l': (5.0, 7.0),
                'nitrates_no3_mg_l': (5.0, 15.0),
                'nitrites_no2_mg_l': (0.05, 0.15),
                'ammonia_nh3_mg_l': (0.2, 0.5),
                'phosphates_po4_mg_l': (0.2, 0.5),
                'hardness_mg_l': (150.0, 250.0),
                'iron_fe_mg_l': (0.2, 0.5),
                'manganese_mn_mg_l': (0.1, 0.3),
                'e_coli_ctu_100ml': (0, 2),
                'faecal_coliforms_ctu_100ml': (0, 2),
                'total_coliforms_ctu_100ml': (1, 5),
                'water_pressure_bar': (2.8, 3.5),
                'flow_rate_l_s': (18.0, 25.0),
                'alkalinity_mgL': (60.0, 90.0),
                'color_ptco': (20.0, 40.0)
            }
        },
        "contaminated": {
            "name": "⚠️ CONTAMINATED WATER",
            "location": "Kyanja Reservoir",
            "ranges": {
                'temperature_c': (22.0, 26.0),
                'turbidity_ntu': (5.0, 12.0),
                'electrical_conductivity_us_cm': (1500.0, 2200.0),
                'total_suspended_solids_mg_l': (8.0, 18.0),
                'ph': (6.2, 7.0),
                'residual_chlorine_mg_l': (0.2, 0.4),
                'dissolved_oxygen_mg_l': (6.0, 8.0),
                'nitrates_no3_mg_l': (4.0, 10.0),
                'nitrites_no2_mg_l': (0.08, 0.2),
                'ammonia_nh3_mg_l': (0.15, 0.4),
                'phosphates_po4_mg_l': (0.15, 0.35),
                'hardness_mg_l': (250.0, 350.0),
                'iron_fe_mg_l': (0.5, 1.2),
                'manganese_mn_mg_l': (0.2, 0.5),
                'e_coli_ctu_100ml': (0, 0),
                'faecal_coliforms_ctu_100ml': (0, 1),
                'total_coliforms_ctu_100ml': (0, 3),
                'water_pressure_bar': (3.2, 4.2),
                'flow_rate_l_s': (17.0, 23.0),
                'alkalinity_mgL': (100.0, 150.0),
                'color_ptco': (50.0, 80.0)
            }
        },
        "industrial": {
            "name": "🏭 INDUSTRIAL WATER",
            "location": "Industrial Area Namanve",
            "ranges": {
                'temperature_c': (24.0, 30.0),
                'turbidity_ntu': (8.0, 20.0),
                'electrical_conductivity_us_cm': (1200.0, 1800.0),
                'total_suspended_solids_mg_l': (15.0, 35.0),
                'ph': (6.0, 7.5),
                'residual_chlorine_mg_l': (0.1, 0.4),
                'dissolved_oxygen_mg_l': (4.0, 7.0),
                'nitrates_no3_mg_l': (8.0, 18.0),
                'nitrites_no2_mg_l': (0.1, 0.3),
                'ammonia_nh3_mg_l': (0.3, 0.8),
                'phosphates_po4_mg_l': (0.3, 0.8),
                'hardness_mg_l': (200.0, 400.0),
                'iron_fe_mg_l': (0.3, 0.8),
                'manganese_mn_mg_l': (0.15, 0.4),
                'e_coli_ctu_100ml': (0, 1),
                'faecal_coliforms_ctu_100ml': (0, 2),
                'total_coliforms_ctu_100ml': (1, 4),
                'water_pressure_bar': (2.5, 3.8),
                'flow_rate_l_s': (15.0, 22.0),
                'alkalinity_mgL': (90.0, 140.0),
                'color_ptco': (25.0, 50.0)
            }
        },
        "reservoir": {
            "name": "💧 RESERVOIR WATER",
            "location": "Mutungo Reservoir",
            "ranges": {
                'temperature_c': (21.0, 26.0),
                'turbidity_ntu': (2.0, 8.0),
                'electrical_conductivity_us_cm': (600.0, 1000.0),
                'total_suspended_solids_mg_l': (3.0, 12.0),
                'ph': (6.8, 7.8),
                'residual_chlorine_mg_l': (0.15, 0.5),
                'dissolved_oxygen_mg_l': (6.5, 8.5),
                'nitrates_no3_mg_l': (3.0, 9.0),
                'nitrites_no2_mg_l': (0.02, 0.08),
                'ammonia_nh3_mg_l': (0.08, 0.25),
                'phosphates_po4_mg_l': (0.08, 0.25),
                'hardness_mg_l': (120.0, 200.0),
                'iron_fe_mg_l': (0.08, 0.25),
                'manganese_mn_mg_l': (0.02, 0.08),
                'e_coli_ctu_100ml': (0, 0),
                'faecal_coliforms_ctu_100ml': (0, 1),
                'total_coliforms_ctu_100ml': (0, 2),
                'water_pressure_bar': (3.5, 4.5),
                'flow_rate_l_s': (18.0, 26.0),
                'alkalinity_mgL': (100.0, 160.0),
                'color_ptco': (8.0, 20.0)
            }
        },
        "pump_kurambiro": {
            "name": "⚙️ PUMP STATION WATER",
            "location": "Kurambiro Water Pump",
            "ranges": {
                'temperature_c': (22.0, 27.0),
                'turbidity_ntu': (1.5, 6.0),
                'electrical_conductivity_us_cm': (700.0, 1100.0),
                'total_suspended_solids_mg_l': (2.0, 8.0),
                'ph': (7.0, 8.2),
                'residual_chlorine_mg_l': (0.2, 0.7),
                'dissolved_oxygen_mg_l': (7.0, 9.0),
                'nitrates_no3_mg_l': (2.5, 7.0),
                'nitrites_no2_mg_l': (0.01, 0.06),
                'ammonia_nh3_mg_l': (0.06, 0.18),
                'phosphates_po4_mg_l': (0.06, 0.22),
                'hardness_mg_l': (90.0, 170.0),
                'iron_fe_mg_l': (0.06, 0.18),
                'manganese_mn_mg_l': (0.01, 0.06),
                'e_coli_ctu_100ml': (0, 0),
                'faecal_coliforms_ctu_100ml': (0, 0),
                'total_coliforms_ctu_100ml': (0, 1),
                'water_pressure_bar': (4.0, 5.0),
                'flow_rate_l_s': (22.0, 30.0),
                'alkalinity_mgL': (110.0, 170.0),
                'color_ptco': (6.0, 18.0)
            }
        },
        "pump_lubigi": {
            "name": "⚙️ PUMP STATION WATER",
            "location": "Lubigi Water Pump",
            "ranges": {
                'temperature_c': (22.0, 27.0),
                'turbidity_ntu': (1.5, 6.0),
                'electrical_conductivity_us_cm': (700.0, 1100.0),
                'total_suspended_solids_mg_l': (2.0, 8.0),
                'ph': (7.0, 8.2),
                'residual_chlorine_mg_l': (0.2, 0.7),
                'dissolved_oxygen_mg_l': (7.0, 9.0),
                'nitrates_no3_mg_l': (2.5, 7.0),
                'nitrites_no2_mg_l': (0.01, 0.06),
                'ammonia_nh3_mg_l': (0.06, 0.18),
                'phosphates_po4_mg_l': (0.06, 0.22),
                'hardness_mg_l': (90.0, 170.0),
                'iron_fe_mg_l': (0.06, 0.18),
                'manganese_mn_mg_l': (0.01, 0.06),
                'e_coli_ctu_100ml': (0, 0),
                'faecal_coliforms_ctu_100ml': (0, 0),
                'total_coliforms_ctu_100ml': (0, 1),
                'water_pressure_bar': (4.0, 5.0),
                'flow_rate_l_s': (22.0, 30.0),
                'alkalinity_mgL': (110.0, 170.0),
                'color_ptco': (6.0, 18.0)
            }
        }
    }

    def __init__(self, noise_level: float = 0.05):
        """Initialize the simulator with noise level and scenario weights"""
        self.noise_level = noise_level
        self.weights = {
            "clean": 0.25,           # 25% chance
            "turbid": 0.15,          # 15% chance
            "contaminated": 0.10,     # 10% chance
            "industrial": 0.20,      # 20% chance
            "reservoir": 0.15,       # 15% chance
            "pump_kurambiro": 0.10,  # 10% chance
            "pump_lubigi": 0.05      # 5% chance
        }

    def select_random_scenario(self) -> str:
        """Select a random scenario based on weights"""
        scenarios = list(self.weights.keys())
        weights = [self.weights[s] for s in scenarios]
        return random.choices(scenarios, weights=weights)[0]

    def _add_noise(self, value: float, min_val: float, max_val: float) -> float:
        """Add realistic sensor noise to a value"""
        noise = random.uniform(-self.noise_level, self.noise_level)
        noisy_value = value * (1 + noise)
        return max(min_val, min(noisy_value, max_val))

    def generate_reading(self, scenario: Optional[str] = None) -> Dict[str, Any]:
        """Generate a reading for the specified scenario or random if none specified"""
        if scenario is None:
            scenario = self.select_random_scenario()
        elif scenario not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}. Available: {list(self.SCENARIOS.keys())}")

        scenario_data = self.SCENARIOS[scenario]
        timestamp = kutils.dates.currentTimestamp()

        reading = {
            'scenario': scenario,
            'name': scenario_data['name'],
            'location': scenario_data['location'],
            'timestamp': timestamp,
            'data': {}
        }

        # Generate values for each parameter
        for param, (min_val, max_val) in scenario_data['ranges'].items():
            base_value = random.uniform(min_val, max_val)
            # Round to different precision based on parameter type
            if param in ['e_coli_ctu_100ml', 'faecal_coliforms_ctu_100ml', 'total_coliforms_ctu_100ml']:
                value = int(round(self._add_noise(base_value, min_val, max_val), 0))
            elif param in ['ph', 'turbidity_ntu', 'temperature_c']:
                value = round(self._add_noise(base_value, min_val, max_val), 1)
            else:
                value = round(self._add_noise(base_value, min_val, max_val), 2)
            reading['data'][param] = value

        return reading


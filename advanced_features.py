# Advanced Features Module for Ghana AI Hackathon Transport Optimizer
import hashlib
import time
import threading
from datetime import datetime, timedelta
import json
import uuid
import random
import numpy as np
from collections import defaultdict

# Conditional imports with fallbacks
try:
    from sklearn.neural_network import MLPRegressor
    HAS_ADVANCED_ML = True
except ImportError:
    HAS_ADVANCED_ML = False

class BlockchainLedger:
    """Blockchain implementation for transparent transport operations"""
    
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = {
            'index': 0,
            'timestamp': time.time(),
            'transactions': [],
            'previous_hash': '0',
            'nonce': 0
        }
        genesis_block['hash'] = self.calculate_hash(genesis_block)
        self.chain.append(genesis_block)
    
    def calculate_hash(self, block):
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def add_transaction(self, transaction_type, data):
        transaction = {
            'id': str(uuid.uuid4()),
            'type': transaction_type,
            'data': data,
            'timestamp': time.time()
        }
        self.pending_transactions.append(transaction)
        return transaction['id']
    
    def mine_block(self):
        if not self.pending_transactions:
            return None
        
        new_block = {
            'index': len(self.chain),
            'timestamp': time.time(),
            'transactions': self.pending_transactions.copy(),
            'previous_hash': self.chain[-1]['hash'],
            'nonce': 0
        }
        
        # Simple proof of work
        while not new_block['hash'].startswith('00'):
            new_block['nonce'] += 1
            new_block['hash'] = self.calculate_hash(new_block)
        
        self.chain.append(new_block)
        self.pending_transactions = []
        return new_block

class DigitalTwinEngine:
    """Digital Twin simulation for real-time transport network modeling"""
    
    def __init__(self):
        self.twin_state = {}
        self.simulation_running = False
        self.real_time_data = {}
        self.predictions = {}
    
    def initialize_twin(self, network_data):
        """Initialize digital twin with network topology"""
        self.twin_state = {
            'vehicles': {},
            'stops': network_data.get('stops', {}),
            'routes': network_data.get('routes', {}),
            'passenger_flow': {},
            'last_update': time.time()
        }
    
    def simulate_real_time(self):
        """Simulate real-time network state"""
        while self.simulation_running:
            # Simulate vehicle positions
            for route_id in self.twin_state['routes']:
                if route_id not in self.twin_state['vehicles']:
                    self.twin_state['vehicles'][route_id] = []
                
                # Add random vehicle positions
                vehicle_count = random.randint(2, 6)
                self.twin_state['vehicles'][route_id] = [
                    {
                        'id': f"V{route_id}_{i}",
                        'position': random.uniform(0, 100),
                        'capacity_utilization': random.uniform(0.3, 0.95),
                        'delay_minutes': random.randint(-2, 15)
                    }
                    for i in range(vehicle_count)
                ]
            
            # Update passenger flow
            for stop_id in self.twin_state['stops']:
                self.twin_state['passenger_flow'][stop_id] = {
                    'waiting_passengers': random.randint(0, 50),
                    'boarding_rate': random.uniform(0.5, 3.0),
                    'predicted_demand': random.randint(100, 2000)
                }
            
            self.twin_state['last_update'] = time.time()
            time.sleep(5)  # Update every 5 seconds
    
    def start_simulation(self):
        self.simulation_running = True
        threading.Thread(target=self.simulate_real_time, daemon=True).start()
    
    def stop_simulation(self):
        self.simulation_running = False
    
    def get_twin_state(self):
        return self.twin_state
    
    def predict_congestion(self, route_id, time_horizon=30):
        """Predict congestion levels for the next time_horizon minutes"""
        base_congestion = random.uniform(0.3, 0.8)
        predictions = []
        
        for minute in range(time_horizon):
            # Simulate congestion patterns
            congestion_factor = base_congestion + 0.2 * np.sin(minute / 10) + random.uniform(-0.1, 0.1)
            congestion_factor = max(0, min(1, congestion_factor))
            
            predictions.append({
                'time': minute,
                'congestion_level': congestion_factor,
                'estimated_delay': congestion_factor * 10,
                'alternative_routes': self.suggest_alternatives(route_id, congestion_factor)
            })
        
        return predictions
    
    def suggest_alternatives(self, route_id, congestion_level):
        """Suggest alternative routes based on congestion"""
        if congestion_level > 0.7:
            return ['Alternative Route A', 'Alternative Route B']
        elif congestion_level > 0.5:
            return ['Alternative Route A']
        return []

class IoTDataProcessor:
    """IoT and Edge Computing integration for smart infrastructure"""
    
    def __init__(self):
        self.sensors = {}
        self.edge_devices = {}
        self.data_stream = []
    
    def register_sensor(self, sensor_id, sensor_type, location):
        """Register IoT sensor"""
        self.sensors[sensor_id] = {
            'type': sensor_type,
            'location': location,
            'status': 'active',
            'last_reading': None
        }
    
    def process_sensor_data(self, sensor_id, data):
        """Process incoming sensor data"""
        if sensor_id in self.sensors:
            processed_data = {
                'sensor_id': sensor_id,
                'timestamp': time.time(),
                'data': data,
                'processed': True
            }
            self.data_stream.append(processed_data)
            self.sensors[sensor_id]['last_reading'] = processed_data
            return processed_data
        return None
    
    def simulate_iot_data(self):
        """Simulate IoT sensor data"""
        sensor_types = ['passenger_counter', 'vehicle_tracker', 'weather_sensor', 'air_quality']
        
        for i in range(20):  # Simulate 20 sensors
            sensor_id = f"IOT_{i:03d}"
            sensor_type = random.choice(sensor_types)
            location = {
                'lat': 5.6037 + random.uniform(-0.1, 0.1),
                'lon': -0.1870 + random.uniform(-0.1, 0.1)
            }
            
            self.register_sensor(sensor_id, sensor_type, location)
            
            # Generate sample data
            if sensor_type == 'passenger_counter':
                data = {'count': random.randint(0, 100)}
            elif sensor_type == 'vehicle_tracker':
                data = {'speed': random.uniform(0, 60), 'fuel_level': random.uniform(0.1, 1.0)}
            elif sensor_type == 'weather_sensor':
                data = {'temperature': random.uniform(20, 35), 'humidity': random.uniform(40, 90)}
            else:  # air_quality
                data = {'pm2.5': random.uniform(10, 150), 'co2': random.uniform(300, 500)}
            
            self.process_sensor_data(sensor_id, data)
    
    def get_sensor_summary(self):
        """Get summary of all IoT sensors"""
        return {
            'total_sensors': len(self.sensors),
            'active_sensors': len([s for s in self.sensors.values() if s['status'] == 'active']),
            'sensor_types': list(set(s['type'] for s in self.sensors.values())),
            'recent_readings': len([d for d in self.data_stream if time.time() - d['timestamp'] < 300])
        }

class SocialImpactAnalyzer:
    """Social Impact Analytics for sustainable transport"""
    
    def __init__(self):
        self.impact_metrics = {}
    
    def calculate_environmental_impact(self, optimization_results):
        """Calculate environmental benefits"""
        total_efficiency_gain = sum(r['efficiency_gain'] for r in optimization_results)
        
        # Estimated CO2 reduction (simplified calculation)
        co2_reduction = total_efficiency_gain * 0.1  # kg CO2 per % efficiency gain
        fuel_savings = total_efficiency_gain * 2.5  # liters per % efficiency gain
        
        return {
            'co2_reduction_kg': round(co2_reduction, 2),
            'fuel_savings_liters': round(fuel_savings, 2),
            'trees_equivalent': round(co2_reduction / 22, 1),  # 1 tree absorbs ~22kg CO2/year
            'environmental_score': min(100, total_efficiency_gain * 2)
        }
    
    def calculate_social_benefits(self, stops_data):
        """Calculate social accessibility benefits"""
        total_passengers = stops_data['daily_passengers'].sum()
        avg_accessibility = stops_data['daily_passengers'].mean()
        
        return {
            'people_served_daily': int(total_passengers),
            'accessibility_index': round(avg_accessibility / 1000, 2),
            'underserved_areas': len(stops_data[stops_data['daily_passengers'] < 5000]),
            'well_served_areas': len(stops_data[stops_data['daily_passengers'] > 10000])
        }
    
    def calculate_economic_impact(self, optimization_results):
        """Calculate economic benefits"""
        total_efficiency = sum(r['efficiency_gain'] for r in optimization_results)
        
        # Estimated cost savings (simplified)
        operational_savings = total_efficiency * 1000  # USD per % efficiency
        time_savings_value = total_efficiency * 500  # USD value of time saved
        
        return {
            'operational_savings_usd': round(operational_savings, 2),
            'time_savings_value_usd': round(time_savings_value, 2),
            'total_economic_benefit': round(operational_savings + time_savings_value, 2),
            'roi_percentage': round(total_efficiency * 3, 1)
        }

class GamificationEngine:
    """Gamification system to encourage sustainable transport use"""
    
    def __init__(self):
        self.user_profiles = {}
        self.challenges = []
        self.leaderboard = []
        self.achievements = {}
    
    def create_user_profile(self, user_id, name):
        """Create a new user profile"""
        self.user_profiles[user_id] = {
            'name': name,
            'points': 0,
            'level': 1,
            'badges': [],
            'trips_taken': 0,
            'co2_saved': 0,
            'challenges_completed': 0
        }
    
    def add_trip_points(self, user_id, trip_data):
        """Award points for sustainable transport trips"""
        if user_id not in self.user_profiles:
            return None
        
        base_points = 10
        bonus_points = 0
        
        # Bonus for off-peak travel
        if trip_data.get('off_peak', False):
            bonus_points += 5
        
        # Bonus for shared transport
        if trip_data.get('shared', False):
            bonus_points += 3
        
        total_points = base_points + bonus_points
        
        self.user_profiles[user_id]['points'] += total_points
        self.user_profiles[user_id]['trips_taken'] += 1
        self.user_profiles[user_id]['co2_saved'] += trip_data.get('co2_saved', 2.5)
        
        # Check for level up
        self.check_level_up(user_id)
        
        return total_points
    
    def check_level_up(self, user_id):
        """Check if user should level up"""
        profile = self.user_profiles[user_id]
        new_level = min(10, profile['points'] // 100 + 1)
        
        if new_level > profile['level']:
            profile['level'] = new_level
            profile['badges'].append(f"Level {new_level} Achiever")
    
    def get_leaderboard(self, limit=10):
        """Get top users leaderboard"""
        sorted_users = sorted(
            self.user_profiles.items(),
            key=lambda x: x[1]['points'],
            reverse=True
        )[:limit]
        
        return [
            {
                'rank': i + 1,
                'user_id': user_id,
                'name': profile['name'],
                'points': profile['points'],
                'level': profile['level'],
                'trips': profile['trips_taken']
            }
            for i, (user_id, profile) in enumerate(sorted_users)
        ]
    
    def create_challenges(self):
        """Create weekly challenges"""
        self.challenges = [
            {
                'id': 'challenge_1',
                'title': 'Eco Warrior',
                'description': 'Take 5 public transport trips this week',
                'target': 5,
                'reward_points': 50,
                'type': 'trips'
            },
            {
                'id': 'challenge_2',
                'title': 'Off-Peak Pioneer',
                'description': 'Travel during off-peak hours 3 times',
                'target': 3,
                'reward_points': 30,
                'type': 'off_peak'
            },
            {
                'id': 'challenge_3',
                'title': 'Route Explorer',
                'description': 'Try 3 different routes',
                'target': 3,
                'reward_points': 40,
                'type': 'routes'
            }
        ]

class VoiceAssistant:
    """Voice assistant for accessibility and ease of use"""
    
    def __init__(self):
        self.commands = {}
        self.responses = {}
        self.setup_commands()
    
    def setup_commands(self):
        """Setup voice command patterns"""
        self.commands = {
            'route_info': [
                'tell me about route',
                'route information',
                'how often does the bus come'
            ],
            'next_bus': [
                'when is the next bus',
                'bus schedule',
                'next arrival'
            ],
            'best_route': [
                'best route to',
                'how to get to',
                'route planning'
            ],
            'service_status': [
                'service status',
                'any delays',
                'bus running on time'
            ]
        }
    
    def process_voice_command(self, command_text):
        """Process voice command and return appropriate response"""
        command_text = command_text.lower()
        
        for command_type, patterns in self.commands.items():
            for pattern in patterns:
                if pattern in command_text:
                    return self.generate_response(command_type, command_text)
        
        return {
            'type': 'unknown',
            'response': "I'm sorry, I didn't understand that command. You can ask about routes, schedules, or service status."
        }
    
    def generate_response(self, command_type, command_text):
        """Generate appropriate response for command"""
        responses = {
            'route_info': {
                'type': 'route_info',
                'response': "Here's the route information. The bus runs every 15 minutes during peak hours and every 20 minutes during off-peak hours."
            },
            'next_bus': {
                'type': 'next_bus',
                'response': f"The next bus is arriving in {random.randint(3, 15)} minutes."
            },
            'best_route': {
                'type': 'best_route',
                'response': "I found 3 possible routes to your destination. The fastest route takes 25 minutes with one transfer."
            },
            'service_status': {
                'type': 'service_status',
                'response': "All services are running normally. There's a minor delay of 5 minutes on Route 12 due to traffic."
            }
        }
        
        return responses.get(command_type, {'type': 'unknown', 'response': 'Command not recognized'})

class AdvancedAnalytics:
    """Advanced AI-powered analytics and predictions"""
    
    def __init__(self):
        self.predictive_models = {}
        self.anomaly_detector = None
        self.optimization_engine = None
    
    def train_demand_prediction_model(self, historical_data):
        """Train ML model for demand prediction using available libraries"""
        if HAS_ADVANCED_ML:
            # Use MLPRegressor as a simpler alternative to LSTM
            model = MLPRegressor(
                hidden_layer_sizes=(50, 25),
                max_iter=100,
                random_state=42
            )
            
            # Generate sample training data
            X_train = np.random.random((1000, 24))
            y_train = np.random.random((1000,))
            
            model.fit(X_train, y_train)
            self.predictive_models['demand'] = model
            return model
        else:
            # Fallback to simple statistical model
            self.predictive_models['demand'] = 'statistical_model'
            return 'statistical_model'
    
    def predict_future_demand(self, current_data, hours_ahead=24):
        """Predict passenger demand for next hours_ahead hours"""
        if 'demand' not in self.predictive_models:
            return None
        
        # Generate predictions
        predictions = []
        for hour in range(hours_ahead):
            # Simplified prediction
            base_demand = random.uniform(500, 2000)
            time_factor = 1 + 0.3 * np.sin(hour * 2 * np.pi / 24)  # Daily pattern
            predicted_demand = base_demand * time_factor
            
            predictions.append({
                'hour': hour,
                'predicted_demand': round(predicted_demand),
                'confidence': random.uniform(0.7, 0.95)
            })
        
        return predictions
    
    def detect_anomalies(self, current_data):
        """Detect anomalies in transport network"""
        anomalies = []
        
        # Simulate anomaly detection
        for route in current_data.get('routes', []):
            if random.random() < 0.1:  # 10% chance of anomaly
                anomaly_type = random.choice(['delay', 'overcrowding', 'breakdown'])
                anomalies.append({
                    'route_id': route.get('route_id', 'unknown'),
                    'type': anomaly_type,
                    'severity': random.choice(['low', 'medium', 'high']),
                    'description': f"Detected {anomaly_type} on route",
                    'timestamp': time.time()
                })
        
        return anomalies
    
    def generate_real_time_insights(self, network_state):
        """Generate real-time insights from current network state"""
        insights = []
        
        # Capacity utilization insights
        if 'vehicles' in network_state:
            avg_utilization = np.mean([
                v['capacity_utilization'] 
                for vehicles in network_state['vehicles'].values() 
                for v in vehicles
            ])
            
            if avg_utilization > 0.85:
                insights.append({
                    'type': 'capacity_warning',
                    'message': f"High capacity utilization detected: {avg_utilization:.1%}",
                    'action': 'Consider deploying additional vehicles'
                })
        
        # Delay insights
        if 'vehicles' in network_state:
            delays = [
                v['delay_minutes'] 
                for vehicles in network_state['vehicles'].values() 
                for v in vehicles
            ]
            avg_delay = np.mean(delays)
            
            if avg_delay > 5:
                insights.append({
                    'type': 'delay_warning',
                    'message': f"Average delay: {avg_delay:.1f} minutes",
                    'action': 'Investigate traffic conditions and adjust schedules'
                })
        
        return insights

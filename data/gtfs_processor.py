"""
GTFS Data Processing Module for Accra Transport Optimization

This module handles loading, processing, and analyzing GTFS (General Transit Feed Specification) 
data for the Accra public transport system.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import zipfile
import requests
from geopy.distance import geodesic
import networkx as nx
from typing import Dict, List, Tuple, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GTFSProcessor:
    """Process GTFS data for transport analysis"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.gtfs_data = {}
        self.transport_graph = None
        
    def create_sample_gtfs_data(self) -> Dict[str, pd.DataFrame]:
        """Create sample GTFS data for demonstration"""
        logger.info("Creating sample GTFS data for Accra")
        
        # Agency data
        agency_data = {
            'agency_id': ['GPRTU', 'METRO_MASS'],
            'agency_name': ['Ghana Private Road Transport Union', 'Metro Mass Transit'],
            'agency_url': ['http://gprtu.gov.gh', 'http://metromasstransit.com.gh'],
            'agency_timezone': ['Africa/Accra', 'Africa/Accra']
        }
        
        # Bus stops (expanded dataset)
        stops_data = {
            'stop_id': ['ST001', 'ST002', 'ST003', 'ST004', 'ST005', 'ST006', 'ST007', 'ST008', 'ST009', 'ST010',
                       'ST011', 'ST012', 'ST013', 'ST014', 'ST015'],
            'stop_name': ['Kwame Nkrumah Circle', 'Kaneshie Market', 'Achimota Station', 'Tema Station', 
                         'Madina Market', 'Lapaz', 'Dansoman', 'Airport', 'University of Ghana', 'Nungua',
                         'Osu Castle', 'Labadi Beach', 'East Legon', 'Spintex', 'Kasoa'],
            'stop_lat': [5.5600, 5.5450, 5.6050, 5.6700, 5.6800, 5.6000, 5.5300, 5.6050, 5.6500, 5.5900,
                        5.5500, 5.5400, 5.6200, 5.5800, 5.5200],
            'stop_lon': [-0.2000, -0.2300, -0.2200, -0.0800, -0.1600, -0.2500, -0.2800, -0.1700, -0.1900, -0.0600,
                        -0.1800, -0.1600, -0.1400, -0.1200, -0.4200],
            'zone_id': ['Z1', 'Z1', 'Z2', 'Z3', 'Z2', 'Z1', 'Z1', 'Z2', 'Z2', 'Z3',
                       'Z1', 'Z1', 'Z2', 'Z3', 'Z4']
        }
        
        # Routes
        routes_data = {
            'route_id': ['R001', 'R002', 'R003', 'R004', 'R005', 'R006', 'R007', 'R008'],
            'agency_id': ['GPRTU', 'GPRTU', 'METRO_MASS', 'GPRTU', 'METRO_MASS', 'GPRTU', 'GPRTU', 'METRO_MASS'],
            'route_short_name': ['37', '2', 'MM1', '8', 'MM2', '4', '12', 'MM3'],
            'route_long_name': ['Circle-Kaneshie Express', 'Achimota-Tema Main', 'Metro Madina-Airport', 
                               'Lapaz-Nungua Route', 'Metro Dansoman-UG', 'Osu-East Legon', 
                               'Spintex-Kasoa', 'Metro Circle-Labadi'],
            'route_type': [3, 3, 3, 3, 3, 3, 3, 3],  # 3 = Bus
            'route_color': ['FF0000', '00FF00', '0000FF', 'FFFF00', 'FF00FF', '00FFFF', 'FFA500', '800080']
        }
        
        # Stop times (sample schedule)
        stop_times_data = []
        trip_counter = 1
        
        for route_id in routes_data['route_id']:
            # Create multiple trips per route
            for trip_num in range(1, 6):  # 5 trips per route
                trip_id = f"T{trip_counter:03d}"
                
                # Sample stops for this route (simplified)
                if route_id == 'R001':  # Circle-Kaneshie
                    route_stops = ['ST001', 'ST002']
                    times = ['06:00:00', '06:45:00']
                elif route_id == 'R002':  # Achimota-Tema
                    route_stops = ['ST003', 'ST004']
                    times = ['06:30:00', '08:00:00']
                elif route_id == 'R003':  # Madina-Airport
                    route_stops = ['ST005', 'ST008']
                    times = ['07:00:00', '08:00:00']
                else:
                    route_stops = ['ST001', 'ST010']  # Default route
                    times = ['07:30:00', '08:30:00']
                
                for i, (stop_id, time) in enumerate(zip(route_stops, times)):
                    # Add trip variations throughout the day
                    base_time = datetime.strptime(time, '%H:%M:%S')
                    trip_time = base_time + timedelta(hours=trip_num-1)
                    
                    stop_times_data.append({
                        'trip_id': trip_id,
                        'arrival_time': trip_time.strftime('%H:%M:%S'),
                        'departure_time': trip_time.strftime('%H:%M:%S'),
                        'stop_id': stop_id,
                        'stop_sequence': i + 1
                    })
                
                trip_counter += 1
        
        # Trips
        trips_data = []
        for i in range(1, trip_counter):
            trip_id = f"T{i:03d}"
            route_id = routes_data['route_id'][(i-1) % len(routes_data['route_id'])]
            trips_data.append({
                'route_id': route_id,
                'service_id': 'WEEKDAY',
                'trip_id': trip_id,
                'trip_headsign': f"Trip {i}",
                'direction_id': 0,
                'shape_id': f"S{i:03d}"
            })
        
        # Calendar (service periods)
        calendar_data = {
            'service_id': ['WEEKDAY', 'WEEKEND'],
            'monday': [1, 0],
            'tuesday': [1, 0],
            'wednesday': [1, 0],
            'thursday': [1, 0],
            'friday': [1, 0],
            'saturday': [0, 1],
            'sunday': [0, 1],
            'start_date': ['20240101', '20240101'],
            'end_date': ['20241231', '20241231']
        }
        
        # Convert to DataFrames
        self.gtfs_data = {
            'agency': pd.DataFrame(agency_data),
            'stops': pd.DataFrame(stops_data),
            'routes': pd.DataFrame(routes_data),
            'trips': pd.DataFrame(trips_data),
            'stop_times': pd.DataFrame(stop_times_data),
            'calendar': pd.DataFrame(calendar_data)
        }
        
        logger.info(f"Created GTFS data with {len(self.gtfs_data['stops'])} stops and {len(self.gtfs_data['routes'])} routes")
        return self.gtfs_data
    
    def analyze_service_frequency(self) -> pd.DataFrame:
        """Analyze service frequency by route"""
        if 'stop_times' not in self.gtfs_data or 'trips' not in self.gtfs_data:
            logger.error("Missing required GTFS data for frequency analysis")
            return pd.DataFrame()
        
        # Merge trips with stop_times
        merged = self.gtfs_data['stop_times'].merge(self.gtfs_data['trips'], on='trip_id')
        
        # Calculate frequency by route
        frequency_analysis = []
        
        for route_id in merged['route_id'].unique():
            route_data = merged[merged['route_id'] == route_id]
            
            # Get unique departure times
            departure_times = pd.to_datetime(route_data['departure_time'], format='%H:%M:%S')
            departure_times = departure_times.sort_values()
            
            if len(departure_times) > 1:
                # Calculate intervals between consecutive departures
                intervals = departure_times.diff().dropna()
                avg_interval = intervals.mean().total_seconds() / 60  # Convert to minutes
                
                frequency_analysis.append({
                    'route_id': route_id,
                    'trips_per_day': len(departure_times),
                    'avg_frequency_minutes': round(avg_interval, 1),
                    'first_departure': departure_times.min().strftime('%H:%M'),
                    'last_departure': departure_times.max().strftime('%H:%M')
                })
        
        return pd.DataFrame(frequency_analysis)
    
    def calculate_route_coverage(self) -> pd.DataFrame:
        """Calculate geographic coverage of routes"""
        if 'stops' not in self.gtfs_data:
            logger.error("Missing stops data for coverage analysis")
            return pd.DataFrame()
        
        stops = self.gtfs_data['stops']
        
        # Calculate coverage area (bounding box)
        coverage_stats = {
            'total_stops': len(stops),
            'latitude_range': stops['stop_lat'].max() - stops['stop_lat'].min(),
            'longitude_range': stops['stop_lon'].max() - stops['stop_lon'].min(),
            'center_lat': stops['stop_lat'].mean(),
            'center_lon': stops['stop_lon'].mean(),
            'coverage_area_km2': self._calculate_coverage_area(stops)
        }
        
        return pd.DataFrame([coverage_stats])
    
    def _calculate_coverage_area(self, stops: pd.DataFrame) -> float:
        """Calculate approximate coverage area using convex hull"""
        # Simplified area calculation using bounding box
        lat_range = stops['stop_lat'].max() - stops['stop_lat'].min()
        lon_range = stops['stop_lon'].max() - stops['stop_lon'].min()
        
        # Convert to approximate kilometers (rough estimate for Ghana's latitude)
        lat_km = lat_range * 111  # 1 degree latitude ≈ 111 km
        lon_km = lon_range * 111 * np.cos(np.radians(stops['stop_lat'].mean()))
        
        return lat_km * lon_km
    
    def build_transport_graph(self) -> nx.Graph:
        """Build a network graph of the transport system"""
        if 'stops' not in self.gtfs_data or 'stop_times' not in self.gtfs_data:
            logger.error("Missing required data for graph construction")
            return nx.Graph()
        
        G = nx.Graph()
        
        # Add stop nodes
        for _, stop in self.gtfs_data['stops'].iterrows():
            G.add_node(stop['stop_id'], 
                      name=stop['stop_name'],
                      lat=stop['stop_lat'],
                      lon=stop['stop_lon'])
        
        # Add edges based on route connections
        merged = self.gtfs_data['stop_times'].merge(self.gtfs_data['trips'], on='trip_id')
        
        for trip_id in merged['trip_id'].unique():
            trip_stops = merged[merged['trip_id'] == trip_id].sort_values('stop_sequence')
            
            # Connect consecutive stops in the trip
            for i in range(len(trip_stops) - 1):
                stop1 = trip_stops.iloc[i]['stop_id']
                stop2 = trip_stops.iloc[i + 1]['stop_id']
                
                # Calculate distance between stops
                if G.has_node(stop1) and G.has_node(stop2):
                    stop1_coords = (G.nodes[stop1]['lat'], G.nodes[stop1]['lon'])
                    stop2_coords = (G.nodes[stop2]['lat'], G.nodes[stop2]['lon'])
                    distance = geodesic(stop1_coords, stop2_coords).kilometers
                    
                    if G.has_edge(stop1, stop2):
                        # Update edge weight if multiple routes use same connection
                        G[stop1][stop2]['weight'] = min(G[stop1][stop2]['weight'], distance)
                        G[stop1][stop2]['routes'].add(trip_stops.iloc[i]['route_id'])
                    else:
                        G.add_edge(stop1, stop2, 
                                 weight=distance,
                                 routes={trip_stops.iloc[i]['route_id']})
        
        self.transport_graph = G
        logger.info(f"Built transport graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        return G
    
    def analyze_network_connectivity(self) -> Dict:
        """Analyze network connectivity metrics"""
        if self.transport_graph is None:
            self.build_transport_graph()
        
        G = self.transport_graph
        
        analysis = {
            'total_stops': G.number_of_nodes(),
            'total_connections': G.number_of_edges(),
            'average_degree': sum(dict(G.degree()).values()) / G.number_of_nodes(),
            'is_connected': nx.is_connected(G),
            'number_of_components': nx.number_connected_components(G),
            'diameter': nx.diameter(G) if nx.is_connected(G) else None,
            'average_clustering': nx.average_clustering(G),
            'density': nx.density(G)
        }
        
        # Find most connected stops
        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G)
        
        analysis['most_connected_stops'] = sorted(degree_centrality.items(), 
                                                key=lambda x: x[1], reverse=True)[:5]
        analysis['most_important_stops'] = sorted(betweenness_centrality.items(), 
                                                key=lambda x: x[1], reverse=True)[:5]
        
        return analysis
    
    def export_processed_data(self, output_dir: str = "processed_data"):
        """Export processed GTFS data to CSV files"""
        os.makedirs(output_dir, exist_ok=True)
        
        for table_name, df in self.gtfs_data.items():
            output_path = os.path.join(output_dir, f"{table_name}.csv")
            df.to_csv(output_path, index=False)
            logger.info(f"Exported {table_name} data to {output_path}")
        
        # Export analysis results
        frequency_analysis = self.analyze_service_frequency()
        if not frequency_analysis.empty:
            frequency_analysis.to_csv(os.path.join(output_dir, "frequency_analysis.csv"), index=False)
        
        coverage_analysis = self.calculate_route_coverage()
        if not coverage_analysis.empty:
            coverage_analysis.to_csv(os.path.join(output_dir, "coverage_analysis.csv"), index=False)
        
        connectivity_analysis = self.analyze_network_connectivity()
        with open(os.path.join(output_dir, "connectivity_analysis.txt"), 'w') as f:
            for key, value in connectivity_analysis.items():
                f.write(f"{key}: {value}\n")
    
    def generate_summary_report(self) -> str:
        """Generate a summary report of the GTFS data analysis"""
        if not self.gtfs_data:
            return "No GTFS data loaded for analysis."
        
        report = []
        report.append("="*60)
        report.append("ACCRA PUBLIC TRANSPORT GTFS ANALYSIS REPORT")
        report.append("="*60)
        report.append("")
        
        # Basic statistics
        report.append("BASIC STATISTICS:")
        report.append(f"• Total Bus Stops: {len(self.gtfs_data.get('stops', []))}")
        report.append(f"• Total Routes: {len(self.gtfs_data.get('routes', []))}")
        report.append(f"• Total Trips: {len(self.gtfs_data.get('trips', []))}")
        report.append(f"• Transport Agencies: {len(self.gtfs_data.get('agency', []))}")
        report.append("")
        
        # Frequency analysis
        freq_analysis = self.analyze_service_frequency()
        if not freq_analysis.empty:
            report.append("SERVICE FREQUENCY ANALYSIS:")
            avg_frequency = freq_analysis['avg_frequency_minutes'].mean()
            report.append(f"• Average service frequency: {avg_frequency:.1f} minutes")
            report.append(f"• Most frequent route: {freq_analysis.loc[freq_analysis['avg_frequency_minutes'].idxmin(), 'route_id']}")
            report.append(f"• Least frequent route: {freq_analysis.loc[freq_analysis['avg_frequency_minutes'].idxmax(), 'route_id']}")
            report.append("")
        
        # Coverage analysis
        coverage = self.calculate_route_coverage()
        if not coverage.empty:
            report.append("GEOGRAPHIC COVERAGE:")
            report.append(f"• Coverage area: {coverage.iloc[0]['coverage_area_km2']:.1f} km²")
            report.append(f"• Network center: ({coverage.iloc[0]['center_lat']:.4f}, {coverage.iloc[0]['center_lon']:.4f})")
            report.append("")
        
        # Network connectivity
        connectivity = self.analyze_network_connectivity()
        report.append("NETWORK CONNECTIVITY:")
        report.append(f"• Network connectivity: {'Connected' if connectivity.get('is_connected', False) else 'Disconnected'}")
        report.append(f"• Average connections per stop: {connectivity.get('average_degree', 0):.1f}")
        report.append(f"• Network density: {connectivity.get('density', 0):.3f}")
        
        if connectivity.get('most_connected_stops'):
            most_connected = connectivity['most_connected_stops'][0][0]
            report.append(f"• Most connected stop: {most_connected}")
        
        report.append("")
        report.append("="*60)
        
        return "\n".join(report)

def main():
    """Main function to demonstrate GTFS processing"""
    processor = GTFSProcessor()
    
    # Create sample data
    gtfs_data = processor.create_sample_gtfs_data()
    
    # Perform analysis
    print("Processing GTFS data for Accra transport system...")
    
    # Generate and print summary report
    report = processor.generate_summary_report()
    print(report)
    
    # Export processed data
    processor.export_processed_data()
    print("\nProcessed data exported to 'processed_data' directory")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
🚀 Advanced AI Transport Optimization System - Production Launcher
Ghana AI Hackathon 2024 - Production Ready

This script launches the complete advanced transport optimization system
with all features enabled and ready for demonstration.
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print the application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║         🚀 ADVANCED AI TRANSPORT OPTIMIZATION SYSTEM 🚀                     ║
║                                                                              ║
║                        Ghana AI Hackathon 2024                              ║
║                          Production Ready                                    ║
║                                                                              ║
║  Features: AI/ML • Blockchain • Digital Twin • IoT • AR/VR • Voice • More   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    print(banner)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'pandas', 'numpy', 'plotly', 'folium', 
        'scikit-learn', 'ortools', 'networkx', 'geopy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
        print("✅ All dependencies installed!")
    else:
        print("✅ All dependencies satisfied!")
    
    return True

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Advanced AI Transport System...")
    print("🌐 Server will be available at: http://localhost:5000")
    print("📱 Access from any device on your network")
    print("\n" + "="*80)
    print("DEMO READY - All Advanced Features Available:")
    print("="*80)
    print("🔗 Blockchain Integration    - Transparent transaction ledger")
    print("🔄 Digital Twin Engine       - Real-time 3D city simulation") 
    print("🌐 IoT Sensor Network        - Live environmental monitoring")
    print("🥽 AR/VR Visualization       - Immersive transport experience")
    print("🎤 AI Voice Assistant        - Natural language interaction")
    print("🎮 Gamification System       - Sustainability rewards")
    print("📊 Social Impact Analytics   - Environmental benefits tracking")
    print("🚌 Route Optimization        - AI-powered transport planning")
    print("="*80)
    print("\n💡 Quick Start:")
    print("   1. Open browser to http://localhost:5000")
    print("   2. Click 'Initialize AI System'")
    print("   3. Explore all advanced features!")
    print("\n🎊 Ready to win Ghana AI Hackathon 2024! 🎊")
    print("="*80)
    
    # Import and run the main app
    try:
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False
    
    return True

def main():
    """Main execution function"""
    print_banner()
    
    print("🔧 Production System Check...")
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found. Please run this script from the project directory.")
        sys.exit(1)
    
    if not os.path.exists('advanced_features.py'):
        print("❌ Error: advanced_features.py not found. Please ensure all files are present.")
        sys.exit(1)
    
    print("✅ Project files found")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed")
        sys.exit(1)
    
    # Start the application
    print("\n" + "="*80)
    input("Press ENTER to start the Advanced AI Transport System...")
    
    if start_application():
        print("✅ Application started successfully!")
    else:
        print("❌ Failed to start application")
        sys.exit(1)

if __name__ == "__main__":
    main()

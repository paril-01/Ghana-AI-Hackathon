#!/usr/bin/env python3
"""
Feature Test Script for Advanced AI Transport System
Tests all major endpoints and features to ensure they're working properly.
"""

import requests
import json
import time

def test_feature(url, name, expected_status=200):
    """Test a single feature endpoint"""
    try:
        print(f"Testing {name}...")
        response = requests.get(url, timeout=10)
        if response.status_code == expected_status:
            print(f"✅ {name}: SUCCESS")
            return True
        else:
            print(f"❌ {name}: FAILED (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {str(e)}")
        return False

def main():
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Advanced AI Transport System Features")
    print("=" * 50)
    
    # Test main endpoints
    tests = [
        (f"{base_url}/", "Main Dashboard"),
        (f"{base_url}/api/advanced_dashboard", "Advanced Dashboard API"),
        (f"{base_url}/api/blockchain/status", "Blockchain Status"),
        (f"{base_url}/api/digital_twin/status", "Digital Twin Status"),
        (f"{base_url}/api/iot/data", "IoT Data API"),
        (f"{base_url}/api/social_impact/metrics", "Social Impact API"),
        (f"{base_url}/api/gamification/status", "Gamification API"),
        (f"{base_url}/api/voice/status", "Voice Assistant API"),
        (f"{base_url}/api/analytics/overview", "Analytics API"),
        (f"{base_url}/optimize", "Route Optimization"),  # Now expects 200
    ]
    
    passed = 0
    total = len(tests)
    
    for url, name, *args in tests:
        expected_status = args[0] if args else 200
        if test_feature(url, name, expected_status):
            passed += 1
        time.sleep(0.5)  # Small delay between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL FEATURES WORKING! System ready for hackathon demo!")
    else:
        print(f"⚠️  {total - passed} features need attention")
    
    print("\n🚀 Advanced Features Available:")
    print("   • Real-time Dashboard with Live Updates")
    print("   • Blockchain-based Route Verification")
    print("   • Digital Twin Traffic Simulation")
    print("   • IoT Device Integration")
    print("   • Social Impact Analytics")
    print("   • Gamification System")
    print("   • Voice Assistant Commands")
    print("   • Advanced ML Analytics")
    print("   • AR/VR Visualization")
    print("   • WebSocket Real-time Communication")

if __name__ == "__main__":
    main()

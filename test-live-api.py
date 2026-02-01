#!/usr/bin/env python3
"""
🧪 TEST LIVE API SERVER

Test the real data API server locally before deployment.
Verifies all endpoints and data sources are working correctly.

Author: Ether (Crypto Trading Swarm Agent)
"""

import requests
import json
import time
import sys
from datetime import datetime

def test_api_endpoint(url: str, endpoint: str) -> bool:
    """Test a single API endpoint"""
    try:
        print(f"  🔍 Testing {endpoint}...")
        
        response = requests.get(f"{url}{endpoint}", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Basic data validation
            if endpoint == "/api/system-status":
                required_fields = ["status", "metrics", "markets", "agents"]
                missing = [f for f in required_fields if f not in data]
                if missing:
                    print(f"    ❌ Missing fields: {missing}")
                    return False
                
                # Check for live data indicators
                if data.get("data_source") == "live":
                    print(f"    ✅ Live data confirmed")
                else:
                    print(f"    ⚠️  Data source: {data.get('data_source', 'unknown')}")
            
            print(f"    ✅ {endpoint} - OK ({len(str(data))} bytes)")
            return True
            
        else:
            print(f"    ❌ {endpoint} - HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"    ⏱️  {endpoint} - Timeout")
        return False
    except Exception as e:
        print(f"    ❌ {endpoint} - Error: {e}")
        return False

def test_data_quality(url: str) -> bool:
    """Test the quality of real data"""
    try:
        print("  🔍 Testing data quality...")
        
        # Test system status
        response = requests.get(f"{url}/api/system-status", timeout=10)
        if response.status_code != 200:
            print("    ❌ Cannot fetch system status")
            return False
        
        data = response.json()
        
        # Check markets
        markets = data.get("markets", [])
        if not markets:
            print("    ❌ No markets found")
            return False
        
        print(f"    ✅ Found {len(markets)} prediction markets")
        
        # Check market data quality
        for market in markets:
            if market.get("type") == "crypto_price":
                current_price = market.get("current_price", 0)
                if current_price > 0:
                    print(f"    ✅ {market['asset']} price: ${current_price:,.2f}")
                else:
                    print(f"    ⚠️  {market['asset']} price seems invalid")
        
        # Check agents
        agents = data.get("agents", [])
        if agents:
            avg_accuracy = sum(a.get("accuracy", 0) for a in agents) / len(agents)
            print(f"    ✅ {len(agents)} agents, avg accuracy: {avg_accuracy:.1%}")
        
        # Check if data is recent
        timestamp = data.get("timestamp")
        if timestamp:
            data_time = datetime.fromisoformat(timestamp.replace('Z', ''))
            age = (datetime.now() - data_time).total_seconds()
            if age < 300:  # Less than 5 minutes old
                print(f"    ✅ Data is fresh ({age:.0f}s old)")
            else:
                print(f"    ⚠️  Data is {age:.0f}s old")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Data quality test failed: {e}")
        return False

def test_external_dependencies() -> bool:
    """Test external data sources"""
    print("  🔍 Testing external dependencies...")
    
    # Test CoinGecko API
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "usd"}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            btc_price = data.get("bitcoin", {}).get("usd")
            if btc_price:
                print(f"    ✅ CoinGecko API - BTC: ${btc_price:,.2f}")
                return True
        
        print("    ❌ CoinGecko API failed")
        return False
        
    except Exception as e:
        print(f"    ❌ External dependency test failed: {e}")
        return False

def main():
    """Run comprehensive API tests"""
    print("🧪 TESTING LIVE PREDICTION VENUE API")
    print("=" * 40)
    print()
    
    # Test local development server
    local_url = "http://localhost:8080"
    
    print("🔍 1. TESTING EXTERNAL DEPENDENCIES")
    print("-" * 35)
    ext_success = test_external_dependencies()
    print()
    
    print("🔍 2. TESTING LOCAL API SERVER")
    print("-" * 30)
    print(f"   URL: {local_url}")
    
    # List of endpoints to test
    endpoints = [
        "/",
        "/api/system-status",
        "/api/markets", 
        "/api/agents",
        "/api/trades",
        "/api/health",
        "/api/feed"
    ]
    
    local_results = []
    for endpoint in endpoints:
        success = test_api_endpoint(local_url, endpoint)
        local_results.append(success)
    
    print()
    
    print("🔍 3. TESTING DATA QUALITY")
    print("-" * 25)
    data_quality_success = test_data_quality(local_url)
    print()
    
    # Summary
    print("📊 TEST SUMMARY")
    print("-" * 15)
    print(f"   External deps:  {'✅ PASS' if ext_success else '❌ FAIL'}")
    print(f"   API endpoints:  {sum(local_results)}/{len(endpoints)} ({'✅ PASS' if all(local_results) else '❌ FAIL'})")
    print(f"   Data quality:   {'✅ PASS' if data_quality_success else '❌ FAIL'}")
    print()
    
    overall_success = ext_success and all(local_results) and data_quality_success
    
    if overall_success:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Live API server is ready for deployment")
        print()
        print("🚀 Next steps:")
        print("   1. Start local server: python3 real-api-server.py")
        print("   2. Test frontend: cd frontend && npm start")
        print("   3. Deploy live: ./deploy-live.sh")
    else:
        print("❌ SOME TESTS FAILED!")
        print("⚠️  Please fix issues before deploying to production")
        print()
        print("💡 Troubleshooting:")
        print("   • Check internet connection for external APIs")
        print("   • Verify API server is running on port 8080")
        print("   • Check server logs for detailed error messages")
    
    print()
    return 0 if overall_success else 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
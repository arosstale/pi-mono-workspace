#!/usr/bin/env python3
"""Test MSAM REST API integration"""

import json
import time
import requests

API_URL = "http://localhost:8000"

def test_store():
    """Test storing atoms via API."""
    print("📤 Testing POST /store...")
    response = requests.post(
        f"{API_URL}/store",
        json={
            "content": "User tested MSAM REST API successfully",
            "stream": "episodic",
            "arousal": 0.6,
            "valence": 0.7,
            "encoding_confidence": 0.9
        },
        timeout=10
    )
    print(f"  Status: {response.status_code}")
    print(f"  Response: {json.dumps(response.json(), indent=2)[:200]}")
    return response.status_code == 200

def test_query():
    """Test querying via API."""
    print("\n📥 Testing POST /query...")
    response = requests.post(
        f"{API_URL}/query",
        json={"query": "What do you know about MSAM REST API?"},
        timeout=10
    )
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Confidence Tier: {data.get('confidence_tier')}")
        print(f"  Total Tokens: {data.get('total_tokens')}")
        print(f"  Items Returned: {data.get('items_returned')}")
        print(f"  Latency: {data.get('latency_ms')}ms")
        if data.get('atoms'):
            print(f"  First Atom: {data['atoms'][0]['content'][:80]}...")
    return response.status_code == 200

def test_context():
    """Test context via API."""
    print("\n📋 Testing POST /context...")
    response = requests.post(
        f"{API_URL}/context",
        json={},
        timeout=10
    )
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Total Tokens: {data.get('total_tokens')}")
        print(f"  Method: {data.get('method')}")
    return response.status_code == 200

def test_stats():
    """Test stats via API."""
    print("\n📊 Testing GET /stats...")
    response = requests.get(f"{API_URL}/stats", timeout=10)
    print(f"  Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"  Total Atoms: {data.get('total_atoms')}")
        print(f"  Active Atoms: {data.get('active_atoms')}")
        print(f"  Est Tokens: {data.get('est_active_tokens')}")
    return response.status_code == 200

def main():
    """Run all API tests."""
    print("🧪 MSAM REST API Integration Test\n")
    print(f"API URL: {API_URL}")
    print("=" * 50)

    results = []
    results.append(("POST /store", test_store()))
    results.append(("POST /query", test_query()))
    results.append(("POST /context", test_context()))
    results.append(("GET /stats", test_stats()))

    print("\n" + "=" * 50)
    print("📋 Test Results:")
    for endpoint, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status} {endpoint}")

    all_pass = all(success for _, success in results)
    if all_pass:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed")

    return 0 if all_pass else 1

if __name__ == "__main__":
    try:
        exit(main())
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: MSAM server not running")
        print("   Start it with: cd ~/msam && python -m msam.serve")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        exit(1)

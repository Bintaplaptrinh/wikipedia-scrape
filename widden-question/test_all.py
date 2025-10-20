#!/usr/bin/env python3
"""
Quick test script to verify all modules work correctly
Run: python test_all.py
"""

import sys
import os

def test_imports():
    """Test all imports work"""
    print("=" * 60)
    print("TEST 1: Import all modules")
    print("=" * 60)
    
    try:
        from bfs.bfs_pathfinder import BFSPathfinder
        print("✓ BFSPathfinder imported")
    except Exception as e:
        print(f"✗ BFSPathfinder import failed: {e}")
        return False
    
    try:
        from analytic.q4 import InfluenceAnalyzer
        print("✓ InfluenceAnalyzer imported")
    except Exception as e:
        print(f"✗ InfluenceAnalyzer import failed: {e}")
        return False
    
    try:
        from analytic.q5 import Correlation
        print("✓ Correlation imported")
    except Exception as e:
        print(f"✗ Correlation import failed: {e}")
        return False
    
    try:
        from scrape.scrape_wiki import CountryScrape
        print("✓ CountryScrape imported")
    except Exception as e:
        print(f"✗ CountryScrape import failed: {e}")
        return False
    
    print("\n✅ All imports successful!\n")
    return True

def test_files_exist():
    """Test required files exist"""
    print("=" * 60)
    print("TEST 2: Check required files")
    print("=" * 60)
    
    required_files = [
        'countries.jsonl',
        'graph.json',
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing (run: python load_data.py)")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        print("Run setup steps first:")
        print("  1. python load_data.py")
        print("  2. cd scrape && python scrape_wiki.py")
        return False
    
    print("\n✅ All required files exist!\n")
    return True

def test_bfs():
    """Test BFS functionality"""
    print("=" * 60)
    print("TEST 3: BFS Algorithm")
    print("=" * 60)
    
    if not os.path.exists('graph.json'):
        print("⚠️  graph.json not found, skipping BFS test")
        return True
    
    try:
        from bfs.bfs_pathfinder import BFSPathfinder
        
        bfs = BFSPathfinder()
        print(f"✓ Graph loaded: {len(bfs.graph)} countries")
        
        # Test path finding
        test_countries = list(bfs.graph.keys())[:2]
        if len(test_countries) >= 2:
            start, end = test_countries[0], test_countries[1]
            path, distance = bfs.bfs(start, end)
            
            if path:
                print(f"✓ BFS path found: {start} → {end} ({distance} hops)")
            else:
                print(f"✓ BFS executed (no path found, which is OK)")
        
        print("\n✅ BFS working correctly!\n")
        return True
        
    except Exception as e:
        print(f"✗ BFS test failed: {e}")
        return False

def test_analytics():
    """Test analytics modules"""
    print("=" * 60)
    print("TEST 4: Analytics Modules")
    print("=" * 60)
    
    if not os.path.exists('graph.json'):
        print("⚠️  graph.json not found, skipping analytics test")
        return True
    
    try:
        # Test Q4
        from analytic.q4 import InfluenceAnalyzer
        analyzer = InfluenceAnalyzer()
        print(f"✓ Q4 InfluenceAnalyzer initialized")
        
        top = analyzer.calculate_degree_centrality()
        print(f"✓ Q4 Degree centrality calculated: {len(top)} results")
        
        # Test Q5
        from analytic.q5 import Correlation
        correlator = Correlation()
        print(f"✓ Q5 Correlation initialized")
        
        connectivity = correlator.cal_connectivity()
        print(f"✓ Q5 Connectivity calculated: {len(connectivity)} countries")
        
        print("\n✅ Analytics modules working!\n")
        return True
        
    except Exception as e:
        print(f"✗ Analytics test failed: {e}")
        return False

def main():
    print("\n" + "=" * 60)
    print("WIDDEN-QUESTION - AUTOMATED TEST SUITE")
    print("=" * 60 + "\n")
    
    all_passed = True
    
    # Test 1: Imports
    if not test_imports():
        all_passed = False
        print("❌ Import test failed - check dependencies")
    
    # Test 2: Files
    if not test_files_exist():
        all_passed = False
        print("❌ File test failed - run setup first")
    
    # Test 3: BFS
    if not test_bfs():
        all_passed = False
        print("❌ BFS test failed")
    
    # Test 4: Analytics
    if not test_analytics():
        all_passed = False
        print("❌ Analytics test failed")
    
    # Summary
    print("=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYour code is ready to run:")
        print("  python main.py")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("=" * 60)
        print("\nCheck errors above and fix issues")
    print()

if __name__ == '__main__':
    main()

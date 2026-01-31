#!/usr/bin/env python3
"""
Test script for AI Voice Generation System
Verifies that all dependencies are properly installed
"""

import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing Python dependencies...\n")
    
    tests = {
        'Flask': 'flask',
        'pyttsx3': 'pyttsx3',
        'pydub': 'pydub',
    }
    
    passed = 0
    failed = 0
    
    for name, module in tests.items():
        try:
            __import__(module)
            print(f"✓ {name} - OK")
            passed += 1
        except ImportError as e:
            print(f"✗ {name} - FAILED")
            print(f"  Error: {e}")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {passed} passed, {failed} failed")
    print(f"{'='*50}\n")
    
    return failed == 0

def test_tts_engine():
    """Test if TTS engine can be initialized"""
    print("Testing TTS engine initialization...\n")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # Get voices
        voices = engine.getProperty('voices')
        print(f"✓ TTS engine initialized successfully")
        print(f"✓ Found {len(voices)} voice(s) available")
        
        for i, voice in enumerate(voices[:3]):  # Show first 3 voices
            print(f"  Voice {i+1}: {voice.name}")
        
        engine.stop()
        return True
    except Exception as e:
        print(f"✗ TTS engine test failed")
        print(f"  Error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("\nTesting directory structure...\n")
    
    import os
    
    dirs = [
        'templates',
        'static',
        'static/css',
        'static/js',
        'static/audio'
    ]
    
    all_exist = True
    for directory in dirs:
        if os.path.exists(directory):
            print(f"✓ {directory}/ - EXISTS")
        else:
            print(f"✗ {directory}/ - MISSING")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("AI VOICE GENERATION SYSTEM - INSTALLATION TEST")
    print("="*50 + "\n")
    
    results = []
    
    # Test 1: Import dependencies
    results.append(("Dependencies", test_imports()))
    
    # Test 2: TTS engine
    results.append(("TTS Engine", test_tts_engine()))
    
    # Test 3: Directory structure
    results.append(("Directories", test_directories()))
    
    # Final report
    print("\n" + "="*50)
    print("FINAL REPORT")
    print("="*50)
    
    all_passed = all(result[1] for result in results)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    print("="*50 + "\n")
    
    if all_passed:
        print("✓ All tests passed! System is ready to use.")
        print("  Run 'python app.py' to start the application.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("  Refer to SETUP_GUIDE.txt for troubleshooting.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

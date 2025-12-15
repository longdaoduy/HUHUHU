#!/usr/bin/env python3
"""
Debug script to test chatbot with AI mode
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from chatbot import TravelChatbot
from ai_recommend import ai_recommend, loadDestination

def main():
    print("=" * 60)
    print("Chatbot AI Mode Debug Test")
    print("=" * 60)
    
    try:
        # Test 1: Load destinations
        print("\n✅ Test 1: Loading destinations...")
        destinations = loadDestination()
        print(f"   Loaded {len(destinations)} destinations")
        
        # Test 2: Format destinations
        print("\n✅ Test 2: Formatting destinations for AI...")
        if destinations:
            formatted = "\n".join([f"- {d.get('name')}" for d in destinations[:5]])
            print(f"   Sample:\n{formatted}")
        
        # Test 3: Initialize chatbot
        print("\n✅ Test 3: Initializing chatbot...")
        chatbot = TravelChatbot()
        print(f"   Chatbot initialized successfully")
        
        # Test 4: Quick mode (no AI)
        print("\n✅ Test 4: Testing Quick Mode...")
        result = chatbot.chat("mua sắm", use_ai=False)
        print(f"   Status: {result['status']}")
        print(f"   Message: {result['message'][:100]}...")
        print(f"   Recommendations: {len(result.get('recommendations', []))}")
        
        # Test 5: AI Mode
        print("\n⚠️  Test 5: Testing AI Mode (this might take a moment)...")
        try:
            result = chatbot.chat("Tôi muốn đi mua sắm ở Sài Gòn", use_ai=True)
            print(f"   Status: {result['status']}")
            if result['status'] == 'success':
                print(f"   ✅ AI Response received!")
                print(f"   Message: {result['message'][:150]}...")
            else:
                print(f"   ❌ Error: {result['message']}")
        except Exception as e:
            print(f"   ❌ Exception during AI mode: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print("\n" + "=" * 60)
        print("Debug test completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

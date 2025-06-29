#!/usr/bin/env python3
"""Local test script for Japanese G2P functionality."""

import sys

def test_g2p_functions():
    """Test different G2P functions locally."""
    
    print("Testing Japanese G2P functions...")
    
    # Test basic pyopenjtalk
    try:
        import pyopenjtalk
        result = pyopenjtalk.g2p("こんにちは")
        print(f"✓ pyopenjtalk basic: {result}")
    except ImportError:
        print("✗ pyopenjtalk not installed")
        return False
    
    # Test pyopenjtalk-plus
    try:
        import pyopenjtalk_plus
        result = pyopenjtalk_plus.g2p("こんにちは")
        print(f"✓ pyopenjtalk-plus: {result}")
    except ImportError:
        print("⚠ pyopenjtalk-plus not installed (optional)")
    
    # Test espnet2 phoneme tokenizer
    try:
        from espnet2.text.phoneme_tokenizer import pyopenjtalk_g2p_prosody, pyopenjtalk_plus_g2p_prosody
        
        # Test standard prosody
        text = "こんにちは。"
        result = pyopenjtalk_g2p_prosody(text)
        print(f"✓ pyopenjtalk_g2p_prosody: {' '.join(result)}")
        
        # Test plus prosody
        try:
            result_plus = pyopenjtalk_plus_g2p_prosody(text)
            print(f"✓ pyopenjtalk_plus_g2p_prosody: {' '.join(result_plus)}")
        except Exception as e:
            print(f"⚠ pyopenjtalk_plus_g2p_prosody: {e}")
            
    except ImportError as e:
        print(f"✗ Could not import espnet2 modules: {e}")
        return False
    
    # Test with various inputs
    test_cases = [
        ("こんにちは。", "greeting"),
        ("元気ですか？", "question"),
        ("日本語は難しいです。", "statement"),
        ("今日は良い天気ですね。", "complex"),
    ]
    
    print("\nTesting various inputs:")
    for text, desc in test_cases:
        try:
            result = pyopenjtalk_g2p_prosody(text)
            print(f"  {desc}: {text} -> {len(result)} phonemes")
        except Exception as e:
            print(f"  {desc}: Failed - {e}")
    
    return True

if __name__ == "__main__":
    success = test_g2p_functions()
    sys.exit(0 if success else 1)
#!/usr/bin/env python3
"""Verify environment configuration and test API"""

import os
from dotenv import load_dotenv

print("=" * 70)
print("ENVIRONMENT VERIFICATION")
print("=" * 70)

# Step 1: Check .env file location
print("\n1. Checking .env file...")
current_dir = os.getcwd()
env_file = os.path.join(current_dir, ".env")

print(f"   Current directory: {current_dir}")
print(f"   Looking for .env at: {env_file}")

if os.path.exists(env_file):
    print(f"   ✓ .env file EXISTS")
    
    # Read and check contents (safely)
    with open(env_file, 'r') as f:
        content = f.read()
    
    lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
    print(f"   ✓ File has {len(lines)} non-empty, non-comment lines")
    
    # Check for FIREWORKS_API_KEY
    fw_lines = [l for l in lines if 'FIREWORKS_API_KEY' in l]
    if fw_lines:
        print(f"   ✓ Found FIREWORKS_API_KEY line")
        # Check format
        for line in fw_lines:
            if '=' in line:
                key_part = line.split('=', 1)[1].strip()
                if key_part:
                    print(f"   ✓ Key appears to have a value ({len(key_part)} chars)")
                    if key_part.startswith('"') or key_part.startswith("'"):
                        print(f"   ⚠ WARNING: Key is wrapped in quotes - REMOVE THEM!")
                    if ' ' in key_part:
                        print(f"   ⚠ WARNING: Key contains spaces - check for errors!")
                else:
                    print(f"   ✗ Key value is EMPTY!")
    else:
        print(f"   ✗ FIREWORKS_API_KEY not found in .env file")
else:
    print(f"   ✗ .env file NOT FOUND")
    print(f"   → Create a .env file in: {current_dir}")

# Step 2: Load environment
print("\n2. Loading environment variables...")
load_dotenv(override=True)  # Force reload
print("   ✓ load_dotenv() executed with override=True")

# Step 3: Check if variable loaded
print("\n3. Checking loaded environment variable...")
api_key = os.getenv("FIREWORKS_API_KEY")

if api_key:
    print(f"   ✓ FIREWORKS_API_KEY loaded successfully")
    print(f"   ✓ Length: {len(api_key)} characters")
    
    # Clean key check
    clean_key = api_key.strip().strip('"').strip("'")
    if clean_key != api_key:
        print(f"   ⚠ Key has extra characters (quotes/spaces)")
        print(f"   → Original length: {len(api_key)}")
        print(f"   → Cleaned length: {len(clean_key)}")
        api_key = clean_key
    
    # Show safe preview
    if len(api_key) >= 12:
        print(f"   ✓ Key preview: {api_key[:6]}...{api_key[-6:]}")
    
    # Check format
    if api_key.startswith('fw_'):
        print(f"   ✓ Key format looks correct (starts with 'fw_')")
    else:
        print(f"   ⚠ Key doesn't start with 'fw_' - might be invalid")
        print(f"   → First 10 chars: {api_key[:10]}")
else:
    print(f"   ✗ FIREWORKS_API_KEY is NOT loaded!")
    print(f"   → Check your .env file format")
    print(f"   → Should be: FIREWORKS_API_KEY=fw_your_key_here")
    print(f"   → NO quotes, NO spaces around the = sign")

# Step 4: Test API with cleaned key
print("\n4. Testing API connection...")
if api_key:
    # Clean the key one more time
    api_key = api_key.strip().strip('"').strip("'")
    
    try:
        from openai import OpenAI
        
        print(f"   → Initializing client...")
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.fireworks.ai/inference/v1"
        )
        
        print(f"   → Making test API call...")
        response = client.chat.completions.create(
            model="accounts/fireworks/models/llama-v3p1-8b-instruct",
            messages=[{"role": "user", "content": "Say only 'WORKS'"}],
            max_tokens=5,
            temperature=0
        )
        
        result = response.choices[0].message.content
        print(f"   ✓ API call SUCCESSFUL!")
        print(f"   ✓ Response: {result}")
        print("\n" + "=" * 70)
        print("SUCCESS! Your API key is working correctly.")
        print("=" * 70)
        
    except Exception as e:
        print(f"   ✗ API call FAILED")
        error_msg = str(e)
        print(f"   ✗ Error: {error_msg}")
        
        if "unauthorized" in error_msg.lower() or "403" in error_msg:
            print("\n" + "=" * 70)
            print("PROBLEM: API key is INVALID or EXPIRED")
            print("=" * 70)
            print("\nTroubleshooting steps:")
            print("1. Go to: https://fireworks.ai/account/api-keys")
            print("2. Check if your API key is still active")
            print("3. Generate a COMPLETELY NEW key")
            print("4. Copy the ENTIRE key (should start with 'fw_')")
            print("5. Update .env file:")
            print("   FIREWORKS_API_KEY=fw_paste_entire_key_here")
            print("   (NO quotes, NO extra spaces)")
            print("6. Make sure you have credits in your Fireworks account")
        elif "rate" in error_msg.lower():
            print("\n   Issue: Rate limit or quota exceeded")
        else:
            print("\n   Issue: Unknown error - see message above")
else:
    print("   ⊘ Skipped (no API key loaded)")

print("\n" + "=" * 70)
print("VERIFICATION COMPLETE")
print("=" * 70)

# Step 5: Show what to do next
if not api_key or not os.path.exists(env_file):
    print("\n📋 NEXT STEPS:")
    print("1. Create/edit .env file in:", current_dir)
    print("2. Add this line (with your actual key):")
    print("   FIREWORKS_API_KEY=fw_your_actual_key_here")
    print("3. Save the file")
    print("4. Run this script again to verify")
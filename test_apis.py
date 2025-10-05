#!/usr/bin/env python3
"""
API Testing Script for Career Advisor
Tests all API keys to ensure they're working properly
"""

import os
import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

def test_google_gemini():
    """Test Google Gemini API"""
    print("🔍 Testing Google Gemini API...")
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_API_KEY not found in .env file")
        return False
    
    try:
        # Test with a simple request
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{
                "parts": [{"text": "Hello, just testing API connectivity. Respond with 'API Working'"}]
            }]
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                print("✅ Google Gemini API: Working")
                return True
            else:
                print("❌ Google Gemini API: Unexpected response format")
                return False
        else:
            print(f"❌ Google Gemini API: Error {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Google Gemini API: Error - {str(e)}")
        return False

def test_openai():
    """Test OpenAI API"""
    print("\n🔍 Testing OpenAI API...")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in .env file")
        return False
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo-0125",
            "messages": [{"role": "user", "content": "Hello, just testing API connectivity. Respond with 'API Working'"}],
            "max_tokens": 10
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                print("✅ OpenAI API: Working")
                return True
            else:
                print("❌ OpenAI API: Unexpected response format")
                return False
        else:
            print(f"❌ OpenAI API: Error {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API: Error - {str(e)}")
        return False

def test_perplexity():
    """Test Perplexity API"""
    print("\n🔍 Testing Perplexity API...")
    api_key = os.getenv("PERPLEXITY_API_KEY")
    
    if not api_key:
        print("❌ PERPLEXITY_API_KEY not found in .env file")
        return False
    
    try:
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "sonar-reasoning-pro",
            "messages": [{"role": "user", "content": "Hello, just testing API connectivity. Respond with 'API Working'"}],
            "max_tokens": 10
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                print("✅ Perplexity API: Working")
                return True
            else:
                print("❌ Perplexity API: Unexpected response format")
                return False
        else:
            print(f"❌ Perplexity API: Error {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Perplexity API: Error - {str(e)}")
        return False

def test_openrouter():
    """Test OpenRouter API Primary"""
    print("\n🔍 Testing OpenRouter API (Primary)...")
    api_key = os.getenv("OPENROUTER_API_KEY")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY not found in .env file")
        return False
    
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/crew-ai/career-advisor",
            "X-Title": "Career Advisor Test"
        }
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": "Hello, just testing API connectivity. Respond with 'API Working'"}],
            "max_tokens": 10
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                print("✅ OpenRouter API (Primary): Working")
                return True
            else:
                print("❌ OpenRouter API (Primary): Unexpected response format")
                return False
        else:
            print(f"❌ OpenRouter API (Primary): Error {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter API (Primary): Error - {str(e)}")
        return False

def test_openrouter_2():
    """Test OpenRouter API Secondary"""
    print("\n🔍 Testing OpenRouter API (Secondary)...")
    api_key = os.getenv("OPENROUTER_API_KEY_1")
    
    if not api_key:
        print("❌ OPENROUTER_API_KEY_1 not found in .env file")
        return False
    
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/crew-ai/career-advisor",
            "X-Title": "Career Advisor Test"
        }
        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [{"role": "user", "content": "Hello, just testing API connectivity. Respond with 'API Working'"}],
            "max_tokens": 10
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                print("✅ OpenRouter API (Secondary): Working")
                return True
            else:
                print("❌ OpenRouter API (Secondary): Unexpected response format")
                return False
        else:
            print(f"❌ OpenRouter API (Secondary): Error {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ OpenRouter API (Secondary): Error - {str(e)}")
        return False

def test_serper():
    """Test Serper Dev API"""
    print("\n🔍 Testing Serper Dev API...")
    api_key = os.getenv("SERPER_API_KEY")
    
    if not api_key:
        print("❌ SERPER_API_KEY not found in .env file")
        return False
    
    try:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        data = {
            "q": "API test query",
            "num": 1
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'organic' in result or 'searchParameters' in result:
                print("✅ Serper Dev API: Working")
                return True
            else:
                print("❌ Serper Dev API: Unexpected response format")
                return False
        else:
            print(f"❌ Serper Dev API: Error {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Serper Dev API: Error - {str(e)}")
        return False

def main():
    """Run all API tests"""
    print("🚀 Testing all API keys for Career Advisor...")
    print("=" * 50)
    
    results = {}
    
    # Test each API
    results['google_gemini'] = test_google_gemini()
    results['perplexity'] = test_perplexity()
    results['openrouter_primary'] = test_openrouter()
    results['openrouter_secondary'] = test_openrouter_2()
    results['serper'] = test_serper()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 API Test Summary:")
    print("=" * 50)
    
    working_count = 0
    total_count = len(results)
    
    for api_name, status in results.items():
        status_emoji = "✅" if status else "❌"
        status_text = "Working" if status else "Failed"
        print(f"{status_emoji} {api_name.replace('_', ' ').title()}: {status_text}")
        if status:
            working_count += 1
    
    print(f"\n🎯 Result: {working_count}/{total_count} APIs are working")
    
    if working_count == total_count:
        print("🎉 All APIs are working! Your Career Advisor is ready to run!")
    elif working_count >= 3:
        print("⚠️  Most APIs are working. You can run the Career Advisor, but consider fixing the failed ones.")
    else:
        print("❌ Too many APIs failed. Please check your API keys before running the Career Advisor.")
    
    return results

if __name__ == "__main__":
    main()

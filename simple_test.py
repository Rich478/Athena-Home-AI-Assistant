#!/usr/bin/env python
"""
Simple test for the basic LangGraph API functionality
"""

import requests
import json

def simple_test():
    """Test basic API functionality."""
    base_url = "http://127.0.0.1:2024"
    
    print("Testing basic Athena API...")
    
    # Simple test payload
    payload = {
        "assistant_id": "athena",
        "input": {"messages": [{"role": "user", "content": "Hello! Can you tell me what time it is?"}]},
        "config": {
            "configurable": {
                "thread_id": "test_thread_001"
            }
        },
        "stream_mode": "values"
    }
    
    try:
        print("Sending request...")
        response = requests.post(
            f"{base_url}/runs/stream",
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=30
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("Response received! Streaming content:")
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if 'messages' in data and data['messages']:
                            for msg in data['messages']:
                                if 'content' in msg and isinstance(msg['content'], str):
                                    print(f"Athena: {msg['content']}")
                        print("---")
                    except json.JSONDecodeError:
                        print(f"Raw line: {line}")
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    simple_test()
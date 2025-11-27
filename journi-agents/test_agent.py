import requests
import json
import sys

def test_agent(text):
    url = "http://localhost:8000/process"
    headers = {"Content-Type": "application/json"}
    payload = {
        "text": text,
        "user_id": "test_user"
    }

    print(f"🚀 Sending request to {url}...")
    print(f"📝 Input text: {text}")

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        print("\n✅ Response received:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        agent_response = data.get("agent_response", {})
        if isinstance(agent_response, str):
             print(f"\n⚠️ Agent response is a string: {agent_response}")
        else:
            category = agent_response.get("category")
            print(f"\n🏷️  Category: {category}")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the server. Is it running?")
        print("Try running: uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    input_text = "I ate a salad (300 kcal) and spent $15 on lunch."
    if len(sys.argv) > 1:
        input_text = " ".join(sys.argv[1:])
    
    test_agent(input_text)

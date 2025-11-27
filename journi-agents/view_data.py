import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# --- Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRED_PATH = os.path.join(BASE_DIR, "sa-journi.json")

if not firebase_admin._apps:
    if os.path.exists(CRED_PATH):
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred)
    else:
        firebase_admin.initialize_app()

FIRESTORE_DATABASE_ID = os.environ.get("FIRESTORE_DATABASE_ID", "(default)")
db = firestore.client(database_id=FIRESTORE_DATABASE_ID)

def print_collection(name, limit=5):
    print(f"\n📂 Collection: {name} (Last {limit})")
    print("-" * 40)
    
    docs = db.collection(name).order_by("created_at", direction=firestore.Query.DESCENDING).limit(limit).stream()
    
    found = False
    for doc in docs:
        found = True
        data = doc.to_dict()
        print(f"🆔 ID: {doc.id}")
        
        # Format timestamp if present
        if "created_at" in data and data["created_at"]:
            print(f"📅 Date: {data['created_at']}")
            
        print(f"📄 Data: {json.dumps(data, indent=2, default=str, ensure_ascii=False)}")
        print("-" * 20)
        
    if not found:
        print("(Empty)")

if __name__ == "__main__":
    print("🔍 Inspecting Firestore Data...")
    
    print_collection("notes")
    print_collection("transactions")
    print_collection("meals")
    print_collection("workouts")
    print_collection("health_logs")

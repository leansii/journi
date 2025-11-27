import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRED_PATH = os.path.join(BASE_DIR, "sa-journi.json")

if not firebase_admin._apps: # Проверка, чтобы не инициализировать дважды
    if os.path.exists(CRED_PATH):
        cred = credentials.Certificate(CRED_PATH)
        firebase_admin.initialize_app(cred)
        print(f"🔥 Firestore initialized with credentials from {CRED_PATH}")
    else:
        # В Cloud Run это сработает автоматически без файла
        firebase_admin.initialize_app()
        print("🔥 Firestore initialized with default credentials (Cloud Run mode)")

# Get Firestore database ID from environment variable, default to '(default)'
FIRESTORE_DATABASE_ID = os.environ.get("FIRESTORE_DATABASE_ID", "(default)")

# Pass the database ID to the client
db = firestore.client(database_id=FIRESTORE_DATABASE_ID)

def save_note(text: str, category: str, full_json_data: dict) -> str:
    """Saves the original note and returns its ID."""
    note_data = {
        "user_id": "demo_user_123",
        "text": text,           # Исходный текст
        "category": category,   # MIXED, FINANCE, HEALTH...
        "created_at": firestore.SERVER_TIMESTAMP,
        "processed_data": full_json_data # Полный JSON для истории
    }
    _, doc_ref = db.collection("notes").add(note_data)
    print(f"📝 Note saved: {doc_ref.id}")
    return doc_ref.id


def save_transactions(finance_data: dict, note_id: str):
    """Saves financial transactions linked to the note."""
    if not finance_data or "transactions" not in finance_data: return
    batch = db.batch()
    for tx in finance_data["transactions"]:
        doc_ref = db.collection("transactions").document()
        tx_data = tx.copy()
        tx_data["note_id"] = note_id
        tx_data["user_id"] = "demo_user_123"
        tx_data["created_at"] = firestore.SERVER_TIMESTAMP
        batch.set(doc_ref, tx_data)
    batch.commit()
    print(f"💰 Saved {len(finance_data['transactions'])} transactions")

def save_meals(nutrition_data: dict, note_id: str):
    """Saves nutrition data linked to the note."""
    if not nutrition_data: return

    doc_ref = db.collection("meals").document()
    meal_data = nutrition_data.copy()
    meal_data["note_id"] = note_id
    meal_data["user_id"] = "demo_user_123"
    meal_data["created_at"] = firestore.SERVER_TIMESTAMP
    doc_ref.set(meal_data)
    print(f"🥗 Saved meal data")

def save_workouts(fitness_data: dict, note_id: str):
    """Saves workouts linked to the note."""
    if not fitness_data or "workouts" not in fitness_data: return
    batch = db.batch()
    for workout in fitness_data["workouts"]:
        doc_ref = db.collection("workouts").document()
        w_data = workout.copy()
        w_data["note_id"] = note_id
        w_data["user_id"] = "demo_user_123"
        w_data["created_at"] = firestore.SERVER_TIMESTAMP
        batch.set(doc_ref, w_data)
    batch.commit()
    print(f"🏋️‍♀️ Saved {len(fitness_data['workouts'])} workouts")

def save_symptoms(health_data: dict, note_id: str):
    """Saves health log linked to the note."""
    if not health_data: return

    doc_ref = db.collection("health_logs").document()
    h_data = health_data.copy()
    h_data["note_id"] = note_id
    h_data["user_id"] = "demo_user_123"
    h_data["created_at"] = firestore.SERVER_TIMESTAMP
    doc_ref.set(h_data)
    print(f"🩺 Saved health log")

def create_initial_note(text: str, user_id: str = "demo_user_123") -> str:
    """Creates an initial note with 'processing' status and returns its ID."""
    note_data = {
        "user_id": user_id,
        "text": text,
        "status": "processing",
        "created_at": firestore.SERVER_TIMESTAMP,
        "processed_data": {} 
    }
    _, doc_ref = db.collection("notes").add(note_data)
    note_id = doc_ref.id
    print(f"📝 Initial note created: {note_id}")
    return note_id

def update_note_with_results(note_id: str, category: str, full_json_data: dict):
    """Updates the note with the final processed data and sets status to 'processed'."""
    note_ref = db.collection("notes").document(note_id)
    update_data = {
        "status": "processed",
        "category": category,
        "processed_data": full_json_data
    }
    note_ref.update(update_data)
    print(f"✅ Note updated: {note_id}")
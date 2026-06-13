import uuid
from datetime import datetime

def init_db():
    print("Mock database initialized.")

#USER DB
def create_user(firebase_uid, email, display_name, contact_number=None, verified_email=False):
    return str(uuid.uuid4())

def get_user(email):
    return {
        "id": "mock-uuid",
        "displayName": "Mock User",
        "email": email,
        "membersSince": "Jan-01-2026 12:00:00",
        "contactNumber": "1234567890",
        "verified": True
    }

def update_user(email, display_name=None, contact_number=None):
    pass

def update_user_verification(email, verified=True):
    return [{"verified": verified}]

#ENTRY DB      
def create_lost_entry(item_data):
    pass

def update_item_entry(item_id, email, title, category, location, description, losttime):
    return [{"id": item_id}]

def create_found_entry(item_data):
    pass

def get_lost_entries():
    return [{
        "id": "item1",
        "type": "lost",
        "title": "Lost Keys",
        "category": "Keys",
        "location": "Library",
        "description": "Lost my room keys.",
        "losttime": "Morning",
        "photourl": "",
        "status": "active",
        "reporterid": "test@iitbhilai.ac.in"
    }]

def get_lost_entries_by_user(email):
    return get_lost_entries()

def get_found_entries():
    return [{
        "id": "item2",
        "type": "found",
        "title": "Found Water Bottle",
        "category": "Accessories",
        "location": "Canteen",
        "description": "Blue milton bottle.",
        "losttime": "Afternoon",
        "photourl": "",
        "status": "active",
        "reporterid": "another@iitbhilai.ac.in"
    }]

def get_found_entries_by_user(email):
    return get_found_entries()

def resolve_entry(item_id, email):
    return [{"status": "resolved"}]
 
def delete_entry(item_id, email):
    return []

def get_item_by_id(item_id):
    return get_lost_entries()[0]

def get_reporter_id(item_id):
    return "test@iitbhilai.ac.in"
    
#CHAT DB
def load_chat(id):
    return [{
        "id": "chat1",
        "itemid": id,
        "sender": "test@iitbhilai.ac.in",
        "receiver": "public",
        "message": "Is this still available?",
        "time": "2026-01-01T12:00:00Z"
    }]

def save_chat(msg_data):
    pass
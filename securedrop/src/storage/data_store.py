import json
import os

class DataStore:
    def __init__(self):
        # Get the absolute path to THIS PROJECT's root (securedrop folder)
        current_script_path = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_script_path))

        
        self.data_dir = os.path.join(project_root, "data")
        self.users_file = os.path.join(project_root, "data", "users.json")
        
        print("=== DEBUG PATHS ===")
        print(f"Project root: {project_root}")
        print(f"Data directory: {self.data_dir}")
        print(f"Users file: {self.users_file}")
        print("===================")
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def save_user(self, user_data):
        """Save user data to JSON file"""
        print(f"💾 Saving user: {user_data['email']}")
        
        # Load existing users
        all_users = self.load_all_users()
        
        # Add new user
        email = user_data['email']
        all_users[email] = user_data
        
        # Save to file
        try:
            with open(self.users_file, 'w') as f:
                json.dump(all_users, f, indent=2)
            print(f"✅ SUCCESS: Saved to {self.users_file}")
            return True
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return False
    
    def load_all_users(self):
        """Load all users from file"""
        if not os.path.exists(self.users_file):
            return {}
            
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
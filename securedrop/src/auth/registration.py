from storage.data_store import DataStore
from crypto.password_hasher import PasswordHasher

class UserRegistration:
    def __init__(self):
        self.data_store = DataStore()
        self.password_hasher = PasswordHasher()
    
    def is_valid_email(self, email):
        """Check if email has proper format"""
        if '@' not in email:
            return False
        parts = email.split('@')
        if len(parts) != 2:
            return False
        if '.' not in parts[1]:
            return False
        return True
    
    def register_user(self):
        print("\n--- User Registration ---")
        
        # Collect user information
        full_name = input("Enter Full Name: ")
        email = input("Enter Email Address: ").strip()
        
        # Validate email format
        if not self.is_valid_email(email):
            print("ERROR: Invalid email format! Use: user@example.com")
            return None
        
        # Check if user already exists
        existing_users = self.data_store.load_all_users()
        if email in existing_users:
            print("ERROR: User with this email already exists!")
            return None
        
        password = input("Enter Password: ")
        confirm_password = input("Re-enter Password: ")
        
        # Check passwords match
        if password != confirm_password:
            print("ERROR: Passwords do not match!")
            return None
            
        # Check password length
        if len(password) < 8:
            print("ERROR: Password must be at least 8 characters!")
            return None
        
        # Hash the password securely
        password_hash, salt = self.password_hasher.hash_password(password)
        
        # Create user data with HASHED password
        user_data = {
            'full_name': full_name,
            'email': email,
            'password_hash': password_hash.hex(),  # Store as hex string
            'salt': salt.hex(),                    # Store as hex string
            'contacts': []
        }
        
        # Save to file
        if self.data_store.save_user(user_data):
            print("Passwords Match.")
            print("User Registered.")
            print("Password securely hashed and stored.")
            return user_data
        
        return None
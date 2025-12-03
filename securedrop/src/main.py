#!/usr/bin/env python3
import sys
import os
from getpass import getpass
from auth.registration import UserRegistration
from auth.login import UserLogin
from auth.session import UserSession
from storage.data_store import DataStore
from contacts.manager import ContactManager
from network.discovery import NetworkManager

def get_client_id():
    """Get client ID from environment or command line"""
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "CA"

def show_help():
    """Show available commands"""
    print('\nAvailable commands:')
    print('"add"  -> Add a new contact')
    print('"list" -> List all online contacts')
    print('"send" -> Transfer file to contact')
    print('"exit" -> Exit SecureDrop')
    print('"help" -> Show this help message')

def start_secure_shell(user_data, client_id):
    """Start the SecureDrop interactive shell"""
    session = UserSession(user_data)
    contact_manager = ContactManager(user_data['email'], client_id)
    network_manager = NetworkManager(client_id, user_data['email'])
    
    print(f"\nWelcome to SecureDrop, {user_data['full_name']}!")
    print('Type "help" For Commands.')
    
    while session.is_active():
        try:
            command = input("secure_drop> ").strip().lower()
            
            if command == "help":
                show_help()
            elif command == "add":
                contact_manager.add_contact_interactive()
            elif command == "list":
                # Milestone 4: List online contacts
                online_contacts = network_manager.get_online_contacts(
                    contact_manager.get_contacts()
                )
                if online_contacts:
                    print("\nThe following contacts are online:")
                    for contact in online_contacts:
                        print(f"* {contact['full_name']} <{contact['email']}>")
                else:
                    print("\nNo contacts are currently online.")
            elif command == "send":
                # Milestone 5: File transfer
                print("\nFile transfer functionality")
                print("Usage: send <email> <file_path>")
                print("Example: send bob@gmail.com /home/user/file.txt")
                
                # Get send command arguments
                args = input("Enter send command: ").strip()
                if args:
                    parts = args.split()
                    if len(parts) >= 2:
                        contact_email = parts[0]
                        file_path = parts[1]
                        if os.path.exists(file_path):
                            print(f"\nPreparing to send file to {contact_email}...")
                            print("(File transfer implementation would go here)")
                            print("For testing: File would be sent with SHA-256 verification")
                        else:
                            print(f"Error: File '{file_path}' does not exist.")
                    else:
                        print("Error: Invalid format. Use: send email@example.com /path/to/file")
                else:
                    print("Cancelled.")
            elif command == "exit":
                print("Exiting SecureDrop.")
                session.logout()
                return
            elif command == "":
                continue
            elif command == "lst":  # Test case for Milestone 4
                print(f'Unknown command: "{command}". Type "help" for available commands.')
            else:
                print(f'Unknown command: "{command}". Type "help" for available commands.')
                
        except KeyboardInterrupt:
            print("\nExiting SecureDrop.")
            session.logout()
            return
        except Exception as e:
            print(f"Error: {str(e)}")
            continue

def main():
    client_id = get_client_id()
    print(f"=== SecureDrop (Client {client_id}) ===")
    
    data_store = DataStore(client_id)
    users = data_store.load_all_users()
    
    if not users:
        # Milestone 1: Registration
        print("\nNo users are registered with this client.")
        response = input("Do you want to register a new user (y/n)? ").lower()
        
        if response == 'y':
            registrar = UserRegistration(client_id)
            user_data = registrar.register_user()
            if user_data:
                print("\nUser Registered.")
                print("Exiting SecureDrop.")
            else:
                print("\nRegistration failed. Exiting.")
        else:
            print("\nExiting SecureDrop.")
    else:
        # Milestone 2: Login
        login = UserLogin(client_id)
        max_attempts = 3
        attempts = 0
        
        while attempts < max_attempts:
            print()
            email = input("Enter Email Address: ").strip()
            password = getpass("Enter Password: ")
            
            user_data = login.authenticate(email, password)
            
            if user_data:
                print("\nWelcome to SecureDrop.")
                start_secure_shell(user_data, client_id)
                return
            else:
                print("\nEmail and Password Combination Invalid.")
                attempts += 1
                
                if attempts < max_attempts:
                    print(f"{max_attempts - attempts} attempts remaining.")
        
        print("\nToo many failed attempts. Exiting.")

if __name__ == "__main__":
    main()
from auth.registration import UserRegistration

print("=== SecureDrop Starting ===")
print("No users are registered with this client.")

answer = input("Do you want to register a new user (y/n)? ")

if answer == 'y':
    # Use our registration class
    registrar = UserRegistration()
    user_data = registrar.register_user()
    
    if user_data:
        print(f"SUCCESS: Registered {user_data['full_name']}!")
    else:
        print("Registration failed.")
        
else:
    print("Exiting SecureDrop.")

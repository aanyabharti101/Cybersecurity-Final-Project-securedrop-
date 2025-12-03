import os
import json

class CertificateManager:
    def __init__(self, certs_dir="certs"):
        self.certs_dir = certs_dir
        os.makedirs(certs_dir, exist_ok=True)
    
    def generate_user_certificate(self, email, client_id):
        """Generate a mock certificate for the user"""
        # In a real implementation, this would generate actual certificates
        # For now, we'll create a simple JSON certificate file
        cert_data = {
            'email': email,
            'client_id': client_id,
            'public_key': f"mock_public_key_for_{email}",
            'issued_at': '2024-01-01',
            'expires_at': '2025-01-01'
        }
        
        cert_filename = f"{email.replace('@', '_').replace('.', '_')}.cert"
        cert_path = os.path.join(self.certs_dir, cert_filename)
        
        with open(cert_path, 'w') as f:
            json.dump(cert_data, f, indent=2)
        
        return cert_path
#!/usr/bin/env python3
"""
Self-Signed Certificate Generator for IoTConnect
Generates X.509 certificates for device authentication
"""

import os
import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_self_signed_certificate(device_id, cert_dir="./certs", validity_days=365):
    """
    Generate a self-signed X.509 certificate for IoTConnect device authentication
    
    Args:
        device_id (str): Unique device identifier
        cert_dir (str): Directory to save certificates
        validity_days (int): Certificate validity period in days
    
    Returns:
        tuple: (private_key_path, certificate_path, ca_cert_path)
    """
    
    # Ensure certificate directory exists
    os.makedirs(cert_dir, exist_ok=True)
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Create certificate subject
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "IoTConnect Device"),
        x509.NameAttribute(NameOID.COMMON_NAME, device_id),
    ])
    
    # Create certificate
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        datetime.datetime.utcnow() + datetime.timedelta(days=validity_days)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(device_id),
            x509.DNSName(f"{device_id}.iotconnect.io"),
        ]),
        critical=False,
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=0),
        critical=True,
    ).add_extension(
        x509.KeyUsage(
            digital_signature=True,
            key_cert_sign=True,
            crl_sign=True,
            content_commitment=False,
            data_encipherment=False,
            key_agreement=False,
            key_encipherment=True,
            encipher_only=False,
            decipher_only=False,
        ),
        critical=True,
    ).sign(private_key, hashes.SHA256())
    
    # File paths
    private_key_path = os.path.join(cert_dir, f"pk_{device_id}.pem")
    cert_path = os.path.join(cert_dir, f"cert_{device_id}.crt")
    ca_cert_path = os.path.join(cert_dir, f"ca_{device_id}.pem")
    
    # Write private key
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Write certificate
    with open(cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # For self-signed, the CA certificate is the same as the device certificate
    with open(ca_cert_path, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    print(f"✅ Self-signed certificate generated successfully!")
    print(f"📁 Private Key: {private_key_path}")
    print(f"📁 Certificate: {cert_path}")
    print(f"📁 CA Certificate: {ca_cert_path}")
    print(f"⏰ Valid until: {cert.not_valid_after}")
    
    return private_key_path, cert_path, ca_cert_path

def main():
    """Generate self-signed certificate for the gateway device"""
    device_id = "GW-20001448"  # Your gateway device ID
    
    try:
        # Install cryptography if not available
        try:
            import cryptography
        except ImportError:
            print("Installing cryptography library...")
            import subprocess
            subprocess.check_call(["pip", "install", "cryptography"])
            import cryptography
        
        # Generate certificates
        private_key_path, cert_path, ca_cert_path = generate_self_signed_certificate(
            device_id=device_id,
            cert_dir="./certs",
            validity_days=365  # 1 year validity
        )
        
        print("\n📋 Next Steps:")
        print("1. Update your gateway_app.py to use CA_SELF_SIGNED authentication")
        print("2. Upload the certificate to IoTConnect platform")
        print("3. Configure the device to use self-signed authentication")
        
    except Exception as e:
        print(f"❌ Error generating certificate: {e}")

if __name__ == "__main__":
    main()
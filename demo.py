from src.biometric_auth import BiometricAuth

def main():
    # Create instance
    auth = BiometricAuth()

    # Fingerprint demo
    if auth.setup_fingerprint():
        print("\nTesting Fingerprint Authentication:")
        print("1. Enrolling new fingerprint...")
        auth.enroll_fingerprint()
        
        print("\n2. Verifying fingerprint...")
        auth.verify_fingerprint()

    # Facial recognition demo
    print("\nTesting Facial Recognition:")
    print("1. Enrolling new face...")
    auth.enroll_face("John", "path/to/john_photo.jpg")
    
    print("\n2. Verifying face...")
    auth.verify_face("path/to/verify_photo.jpg")

if __name__ == "__main__":
    main()

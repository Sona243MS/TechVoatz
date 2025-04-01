from biometric_auth import BiometricAuth

# Create instance
auth = BiometricAuth()

# For fingerprint authentication
if auth.setup_fingerprint():
    # Enroll new fingerprint
    auth.enroll_fingerprint()
    
    # Verify fingerprint
    if auth.verify_fingerprint():
        print("Fingerprint authentication successful!")

# For facial recognition
# Enroll a face
auth.enroll_face("John", "path/to/john_photo.jpg")

# Verify a face
if auth.verify_face("path/to/verify_photo.jpg"):
    print("Facial recognition successful!")

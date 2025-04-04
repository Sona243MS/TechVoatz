import face_recognition
import cv2
import numpy as np
from pyfingerprint.pyfingerprint import PyFingerprint
from dotenv import load_dotenv
import os

load_dotenv()

class BiometricAuth:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.port = os.getenv('FINGERPRINT_PORT', '/dev/ttyUSB0')
        self.baudrate = int(os.getenv('FINGERPRINT_BAUDRATE', '57600'))
        
    def setup_fingerprint(self):
        try:
            self.f = PyFingerprint(self.port, self.baudrate)
            if not self.f.verifyPassword():
                raise ValueError('Password verification failed!')
            return True
        except Exception as e:
            print(f'Error initializing fingerprint sensor: {e}')
            return False

    def enroll_fingerprint(self):
        try:
            print('Place finger on sensor...')
            while not self.f.readImage():
                pass

            self.f.convertImage(0x01)
            result = self.f.searchTemplate()
            
            if result[0] >= 0:
                print('Fingerprint already exists')
                return False

            print('Remove finger...')
            while self.f.readImage():
                pass

            print('Place same finger again...')
            while not self.f.readImage():
                pass

            self.f.convertImage(0x02)
            if self.f.compareCharacteristics() == 0:
                print('Fingers do not match')
                return False

            self.f.createTemplate()
            self.f.storeTemplate()
            print('Fingerprint enrolled successfully!')
            return True

        except Exception as e:
            print(f'Error enrolling fingerprint: {e}')
            return False

    def verify_fingerprint(self):
        try:
            print('Place finger on sensor...')
            while not self.f.readImage():
                pass

            self.f.convertImage(0x01)
            result = self.f.searchTemplate()
            
            if result[0] >= 0:
                print('Fingerprint matched!')
                return True
            else:
                print('Fingerprint not found!')
                return False

        except Exception as e:
            print(f'Error verifying fingerprint: {e}')
            return False

    def enroll_face(self, name, image_path):
        try:
            image = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)
            print(f'Face enrolled for {name}')
            return True
        except Exception as e:
            print(f'Error enrolling face: {e}')
            return False

    def verify_face(self, image_path):
        try:
            unknown_image = face_recognition.load_image_file(image_path)
            unknown_face_encodings = face_recognition.face_encodings(unknown_image)

            if not unknown_face_encodings:
                print('No face found in image')
                return False

            unknown_face_encoding = unknown_face_encodings[0]
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                unknown_face_encoding,
                tolerance=float(os.getenv('FACE_RECOGNITION_THRESHOLD', '0.6'))
            )

            if True in matches:
                match_index = matches.index(True)
                name = self.known_face_names[match_index]
                print(f'Face matched with {name}!')
                return True
            else:
                print('Face not recognized')
                return False

        except Exception as e:
            print(f'Error verifying face: {e}')
            return False

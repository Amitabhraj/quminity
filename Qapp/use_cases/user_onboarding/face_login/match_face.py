import face_recognition
import numpy as np
import pickle

def match_face(stored_encoding_bytes, incoming_encoding):
    stored_encoding = pickle.loads(stored_encoding_bytes)

    results = face_recognition.compare_faces(
        [stored_encoding],
        incoming_encoding,
        tolerance=0.45
    )
    return results[0]

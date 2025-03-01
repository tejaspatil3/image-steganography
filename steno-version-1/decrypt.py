import cv2

def decrypt_message(image_path, message_length):
    """
    Extracts the password and message from the image.
    Returns a tuple (extracted_password, extracted_message).
    """
    img = cv2.imread(image_path)
    if img is None:
        return None, None

    c = {i: chr(i) for i in range(255)}

    n, m, z = 0, 0, 0
    extracted_data = ""

    for _ in range(message_length + 5):  # Extract password + message
        extracted_data += c[img[n, m, z]]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    extracted_password = extracted_data[:5]  # First 5 chars are password
    extracted_message = extracted_data[5:]  # Rest is the actual message

    return extracted_password, extracted_message

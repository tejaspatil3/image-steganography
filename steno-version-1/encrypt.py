import cv2

def encrypt_message(image_path, password, secret_message, output_path):
    """
    Encrypts a message inside an image with a 5-character alphanumeric password.
    The password is stored in the first 5 pixels before the actual message.
    """
    img = cv2.imread(image_path)
    if img is None:
        return False

    d = {chr(i): i for i in range(255)}

    full_message = password + secret_message  # Embed password first
    n, m, z = 0, 0, 0

    for char in full_message:
        img[n, m, z] = d[char]
        n = (n + 1) % img.shape[0]
        m = (m + 1) % img.shape[1]
        z = (z + 1) % 3

    cv2.imwrite(output_path, img)
    return True

import cv2
import numpy as np

def encrypt_image(image_path, message, password, output_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not found or invalid format.")

    d = {chr(i): i for i in range(256)}  # Mapping ASCII to integer values

    secret_data = password + message  # Store password first, then message
    secret_data += chr(0)  # Null character to indicate end of message

    n, m = 0, 0

    print("\nEncrypting Password and Message...")  # Debugging

    for char in secret_data:
        if n >= img.shape[0] or m >= img.shape[1]:
            raise ValueError("Message is too long for this image.")

        img[n, m, 2] = d[char]  # Storing in the Red channel
        print(f"Pixel ({n},{m},RED): {ord(char)} -> '{char}'")  # Debugging

        n += 1  # Move to the next pixel

    cv2.imwrite(output_path, img)
    print(f"\nEncryption complete. Encrypted image saved as {output_path}")

if __name__ == "__main__":
    img_path = "mypic.jpg"
    msg = input("Enter secret message: ")
    password = input("Enter a 5-character alphanumeric password: ")

    if len(password) != 5 or not password.isalnum():
        print("Password must be exactly 5 alphanumeric characters.")
    else:
        encrypt_image(img_path, msg, password, "encryptedImage.png")

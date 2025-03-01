import cv2
import os

def encrypt_image(image_path, message, password):
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("❌ Image not found or invalid format.")

    d = {chr(i): i for i in range(256)}  # ASCII to integer mapping
    
    secret_data = "@@@" + password + message  # Add unique marker
    n, m, channel = 0, 0, 0  # Start at (0,0) and cycle through RGB

    print("\n🔐 Encrypting Message...")

    for char in secret_data:
        if n >= img.shape[0]:  # Move to next column if end of row
            m += 1
            n = 0
        if m >= img.shape[1]:  # Stop if image is too small
            raise ValueError("❌ Message is too long for this image.")

        img[n, m, channel] = d[char]  # Store in R, G, or B channel
        print(f"Pixel ({n},{m},{'RGB'[channel]}): {ord(char)} -> '{char}'")  # Debugging

        n += 1
        channel = (channel + 1) % 3  # Cycle through R -> G -> B

    original_filename = os.path.basename(image_path)
    encrypted_filename = f"encrypted_{original_filename}"  
    output_path = os.path.join(os.path.dirname(image_path), encrypted_filename)

    cv2.imwrite(output_path, img)
    print(f"\n✅ Encryption complete. Encrypted image saved as {output_path}")

if __name__ == "__main__":
    img_path = "mypic.jpg"  # Change to your image
    msg = input("Enter secret message: ")
    password = input("Enter a 5-character alphanumeric password: ")

    if len(password) != 5 or not password.isalnum():
        print("❌ Password must be exactly 5 alphanumeric characters.")
    else:
        encrypt_image(img_path, msg, password)

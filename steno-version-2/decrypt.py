import cv2

def decrypt_image(image_path, user_password):
    img = cv2.imread(image_path)
    height, width, _ = img.shape  # Get image dimensions

    extracted_password = ""
    extracted_message = ""

    n, m, z = 0, 0, 2  # Start at (0,0) and use Red channel (2)

    # Extract password (first 5 characters)
    for _ in range(5):
        if n >= height or m >= width:  # ✅ Prevent out-of-bounds error
            print("Error: Image too small for decryption.")
            return None

        extracted_password += chr(img[n, m, z])
        n += 1
        m += 1
        z = (z + 1) % 3

    print(f"Extracted Password: {extracted_password}")  # ✅ Debugging line

    # Check if password matches
    if extracted_password != user_password:
        print("Error: Incorrect password")
        return None

    # Extract message
    for _ in range(height * width):  # Prevent infinite loop
        if n >= height or m >= width:  # ✅ Prevent out-of-bounds error
            break

        extracted_message += chr(img[n, m, z])
        n += 1
        m += 1
        z = (z + 1) % 3

    print(f"Decrypted Message: {extracted_message}")  # ✅ Debugging line
    return extracted_message

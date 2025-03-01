import cv2

def decrypt_image(image_path, user_password):
    img = cv2.imread(image_path)
    height, width, _ = img.shape  # Get image dimensions

    extracted_password = ""
    extracted_message = ""

    n, m = 0, 0  # Start at (0,0) and use Red channel (2)

    # Extract password (first 5 characters)
    for _ in range(5):
        if n >= height or m >= width:  # Prevent out-of-bounds error
            print("Error: Image too small for decryption.")
            return None

        extracted_password += chr(img[n, m, 2])
        n += 1  # Move to next pixel

    print(f"Extracted Password: {extracted_password}")  # Debugging line

    # Check if password matches
    if extracted_password != user_password:
        print("Error: Incorrect password")
        return None

    # Extract message
    while True:
        if n >= height or m >= width:  # Prevent out-of-bounds error
            break

        char = chr(img[n, m, 2])
        if char == chr(0):  # Stop when we hit the null character
            break

        extracted_message += char
        n += 1

    print(f"Decrypted Message: {extracted_message}")  # Debugging line
    return extracted_message

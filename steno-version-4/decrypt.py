import cv2

def decrypt_image(image_path, user_password):
    img = cv2.imread(image_path)
    
    if img is None:
        raise ValueError("❌ Image not found or invalid format.")

    height, width, _ = img.shape  # Get image dimensions

    extracted_data = ""
    n, m, channel = 0, 0, 0  # Start at (0,0) and cycle through RGB

    print("\n🔎 Extracting Hidden Data...")

    for _ in range(height * width * 3):  # Prevent infinite loop
        if n >= height:  # Move to next column if end of row
            m += 1
            n = 0
        if m >= width:
            break

        extracted_data += chr(img[n, m, channel])  # Read from R, G, or B channel
        n += 1
        channel = (channel + 1) % 3  # Cycle through R -> G -> B

        if len(extracted_data) >= 3 and extracted_data[:3] != "@@@":  # No marker found
            print("❌ Error: This image is not encrypted!")
            return None

    # Remove the marker and extract password
    extracted_data = extracted_data[3:]  
    extracted_password, extracted_message = extracted_data[:5], extracted_data[5:]

    print(f"🔑 Extracted Password: {extracted_password}")  # Debugging

    if extracted_password != user_password:
        print("❌ Error: Incorrect password")
        return None

    print(f"\n💬 Decrypted Message: {extracted_message}")  # Debugging
    return extracted_message

if __name__ == "__main__":
    img_path = "encrypted_mypic.jpg"  # Change to your image
    user_password = input("Enter the password to decrypt: ")
    
    decrypted_message = decrypt_image(img_path, user_password)
    if decrypted_message:
        print("\n✅ Message successfully decrypted!")

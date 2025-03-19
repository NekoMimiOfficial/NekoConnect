def encrypt(text, password):
    encrypted_text = []
    password_length = len(password)
    
    for i, char in enumerate(text):
        # Get the ASCII value of the character
        char_code = ord(char)
        
        # Determine the shift based on the corresponding character in the password
        # Use modulo to wrap around the password if it's shorter than the text
        shift = ord(password[i % password_length]) - ord('a')  # Assuming password is lowercase
        
        # Encrypt only alphabetic characters
        if char.isalpha():
            if char.islower():
                # Encrypt lowercase letters
                new_char = chr((char_code - ord('a') + shift) % 26 + ord('a'))
            else:
                # Encrypt uppercase letters
                new_char = chr((char_code - ord('A') + shift) % 26 + ord('A'))
            encrypted_text.append(new_char)
        else:
            # Non-alphabetic characters are added unchanged
            encrypted_text.append(char)

    return ''.join(encrypted_text)

def decrypt(encrypted_text, password):
    decrypted_text = []
    password_length = len(password)
    
    for i, char in enumerate(encrypted_text):
        # Get the ASCII value of the character
        char_code = ord(char)
        
        # Determine the shift based on the corresponding character in the password
        shift = ord(password[i % password_length]) - ord('a')  # Assuming password is lowercase
        
        # Decrypt only alphabetic characters
        if char.isalpha():
            if char.islower():
                # Decrypt lowercase letters
                new_char = chr((char_code - ord('a') - shift) % 26 + ord('a'))
            else:
                # Decrypt uppercase letters
                new_char = chr((char_code - ord('A') - shift) % 26 + ord('A'))
            decrypted_text.append(new_char)
        else:
            # Non-alphabetic characters are added unchanged
            decrypted_text.append(char)

    return ''.join(decrypted_text)

# Example usage
if __name__ == "__main__":
    text = "Hello, World!"
    password = "key"
    
    encrypted = encrypt(text, password.lower())  # Convert password to lowercase for consistency
    print("Encrypted:", encrypted)

    decrypted = decrypt(encrypted, password.lower())
    print("Decrypted:", decrypted)

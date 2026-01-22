import streamlit_authenticator as stauth

# Use this script to generate hashed passwords for your auth.yaml

# Add passwords to this list
passwords_to_hash = ['admin123', 'user456']

# Generate hashes
hashed_passwords = stauth.Hasher(passwords_to_hash).generate()

for password, hash_val in zip(passwords_to_hash, hashed_passwords):
    print(f"Password: {password}")
    print(f"Hash: {hash_val}")
    print("-" * 20)

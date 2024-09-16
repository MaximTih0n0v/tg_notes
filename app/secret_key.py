import secrets

# Генерация (256-битного) секретного ключа
secret_key = secrets.token_hex(32)
print(secret_key)

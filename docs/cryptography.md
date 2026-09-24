# Cryptography & Security (`std.crypto`)

Sikhar provides built-in enterprise-grade cryptographic functions and security primitives with zero external dependencies, powered by Python's battle-tested standard library.

---

## Importing

```sk
aayaat std.crypto
```

Both English and native Nepali identifiers are supported out of the box.

---

## Hashing Algorithms

### Secure Hash Function (SHA-256)
Computes a standard 256-bit hexadecimal digest.

```sk
rakha digest = crypto.sha256("password123")
dekha digest
# 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

Nepali alias: `crypto.hashing(data)`

### Extended Hashing (SHA-512 & MD5)

```sk
# SHA-512 (512-bit digest)
rakha sha512_digest = crypto.sha512("sensitive payload")

# MD5 (Legacy 128-bit checksum)
rakha checksum = crypto.md5("file content")
```

---

## Message Authentication (`hmac_sha256`)

Computes a keyed-hash message authentication code (HMAC) using SHA-256 to ensure data integrity and authenticity.

```sk
rakha secret_key = "super_secret_signing_key"
rakha payload = '{"user_id": 1001, "role": "admin"}'

rakha signature = crypto.hmac_sha256(secret_key, payload)
dekha "Signature: " + signature
```

Nepali alias: `crypto.gupta(secret_key, payload)`

---

## Base64 Encoding and Decoding

Safely encode and decode binary and string payloads into ASCII strings:

```sk
rakha original = "Hello from Kathmandu!"

# Encode
rakha encoded = crypto.base64_encode(original)
dekha encoded
# SGVsbG8gZnJvbSBLYXRobWFuZHUh

# Decode
rakha decoded = crypto.base64_decode(encoded)
dekha decoded
# Hello from Kathmandu!
```

---

## Cryptographically Secure Random Generation

Generate cryptographically strong random bytes and URL-safe tokens suitable for session identifiers, CSRF tokens, and security nonces:

```sk
# Secure random hex string (parameter is number of random bytes)
rakha salt = crypto.random_bytes(16) # 32 hex characters
dekha "Salt: " + salt

# Secure URL-safe token
rakha token = crypto.random_token(32)
dekha "Session Token: " + token
```

Nepali alias: `crypto.chinno(length)`

---

## Function Summary

| Function | Nepali Alias | Parameters | Return Type | Description |
|---|---|---|---|---|
| `crypto.sha256(data)` | `crypto.hashing` | `data: str` | `str` | Computes SHA-256 hex digest |
| `crypto.sha512(data)` | — | `data: str` | `str` | Computes SHA-512 hex digest |
| `crypto.md5(data)` | — | `data: str` | `str` | Computes MD5 hex checksum |
| `crypto.hmac_sha256(key, data)` | `crypto.gupta` | `key: str, data: str` | `str` | HMAC-SHA256 signature |
| `crypto.base64_encode(data)` | — | `data: str` | `str` | Base64 encodes string |
| `crypto.base64_decode(b64_str)` | — | `b64_str: str` | `str` | Decodes Base64 to string |
| `crypto.random_bytes(count=16)` | — | `count: int` | `str` | Generates random hex bytes |
| `crypto.random_token(length=32)`| `crypto.chinno` | `length: int` | `str` | Generates URL-safe token |

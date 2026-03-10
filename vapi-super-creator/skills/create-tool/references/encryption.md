# Tool Argument Encryption Reference

> Source: https://docs.vapi.ai/tools/encryption

> **Doc reference:** https://docs.vapi.ai/tools/encryption

Protects sensitive data like SSN, credit card numbers, and other PII by encrypting specific fields before they're sent to your server.

### Setup

1. Dashboard > **Add Custom Credential** > Enable Encryption > **RSA-OAEP-256** > **SPKI-PEM**

### Generate RSA Key Pair

```bash
# Generate private key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Extract public key in SPKI-PEM format
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

### Specify Fields to Encrypt

Define JSON paths for sensitive fields in your tool configuration:

```json
{
  "fieldsToEncrypt": ["ssn", "payment.cardNumber", "payment.cvv"]
}
```

### How It Works

1. When tool is called with sensitive data, Vapi encrypts specified fields using RSA-OAEP-256
2. Your server receives **base64-encoded encrypted strings** instead of plaintext
3. Your server decrypts using the private key

### Decryption Code

**TypeScript:**
```typescript
import * as crypto from 'crypto';
import * as fs from 'fs';

function decryptField(encryptedBase64: string, privateKeyPath: string): string {
  const privateKey = fs.readFileSync(privateKeyPath, 'utf8');
  const encryptedBuffer = Buffer.from(encryptedBase64, 'base64');

  const decrypted = crypto.privateDecrypt(
    {
      key: privateKey,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256',
    },
    encryptedBuffer
  );

  return decrypted.toString('utf8');
}

// Usage
const ssn = decryptField(encryptedSSN, './private_key.pem');
```

**Python:**
```python
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_field(encrypted_base64: str, private_key_path: str) -> str:
    with open(private_key_path, 'rb') as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    encrypted_data = base64.b64decode(encrypted_base64)

    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted.decode('utf-8')

# Usage
ssn = decrypt_field(encrypted_ssn, './private_key.pem')
```

### Security Best Practices
- **Never** commit private keys to version control
- Rotate keys periodically
- Encrypt selectively (only truly sensitive fields)
- Validate decrypted data
- Always use HTTPS for all communication

---


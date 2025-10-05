# 🔥 MNEMONIC API EXAMPLES - DEVELOPMENT ONLY!

## ⚠️ CRITICAL SECURITY WARNING ⚠️

**THIS FUNCTIONALITY IS EXTREMELY DANGEROUS!**

- **ONLY** use `include_mnemonics=true` for development/testing
- **NEVER** use in production environments
- **NEVER** expose this endpoint to public users
- **ALWAYS** log security warnings when mnemonics are requested

## API Endpoints

### 1. Safe Wallet List (Default)
```http
GET {{base_url}}/api/wallet/list
Authorization: Bearer {{access_token}}
```

**Response:**
```json
{
    "count": 2,
    "success": true,
    "wallets": [
        {
            "address": "0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721",
            "balance": 9.330582,
            "created_at": "2025-10-05T06:25:12.781492",
            "id": "02759e08-3140-4c82-a912-ab06195449e9",
            "is_primary": false,
            "updated_at": "2025-10-05T06:25:40.631995",
            "user_id": "48cabdd6-4f25-49e1-94bc-452fb243e609",
            "wallet_name": "My First Wallet"
        },
        {
            "address": "0xa7ac606529AbFa32F2fBb3Dad07a925D482Ee55D",
            "balance": 4.621475,
            "created_at": "2025-10-05T06:25:40.633004",
            "id": "c6245153-f9e6-47a3-b2cb-3dbb4082dd51",
            "is_primary": true,
            "updated_at": "2025-10-05T06:25:40.633006",
            "user_id": "48cabdd6-4f25-49e1-94bc-452fb243e609",
            "wallet_name": "My First Wallet"
        }
    ]
}
```

### 2. Dangerous Wallet List (WITH MNEMONICS - DEV ONLY!)
```http
GET {{base_url}}/api/wallet/list?include_mnemonics=true
Authorization: Bearer {{access_token}}
```

**Response:**
```json
{
    "count": 2,
    "security_warning": "Mnemonics included - DEVELOPMENT ONLY!",
    "success": true,
    "wallets": [
        {
            "address": "0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721",
            "balance": 9.330582,
            "created_at": "2025-10-05T06:25:12.781492",
            "id": "02759e08-3140-4c82-a912-ab06195449e9",
            "is_primary": false,
            "mnemonic": "protect road input panda abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
            "updated_at": "2025-10-05T06:25:40.631995",
            "user_id": "48cabdd6-4f25-49e1-94bc-452fb243e609",
            "wallet_name": "My First Wallet"
        },
        {
            "address": "0xa7ac606529AbFa32F2fBb3Dad07a925D482Ee55D",
            "balance": 4.621475,
            "created_at": "2025-10-05T06:25:40.633004",
            "id": "c6245153-f9e6-47a3-b2cb-3dbb4082dd51",
            "is_primary": true,
            "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
            "updated_at": "2025-10-05T06:25:40.633006",
            "user_id": "48cabdd6-4f25-49e1-94bc-452fb243e609",
            "wallet_name": "My First Wallet"
        }
    ]
}
```

## Postman Collection Updates

The Postman collection now includes:

1. **"List User Wallets"** - Safe version (default)
2. **"List User Wallets (WITH MNEMONICS - DEV ONLY)"** - Dangerous version

## Security Features

### 1. **Logging Warnings**
```
2025-10-05 13:19:32,233 - services.wallet_service - WARNING - SECURITY RISK: Returning mnemonic for wallet 0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721
```

### 2. **Response Warnings**
- `security_warning` field in response
- Clear documentation in API descriptions

### 3. **Parameter Validation**
- `include_mnemonics` defaults to `false`
- Must explicitly set to `true` to enable dangerous mode

## Usage Examples

### JavaScript/Frontend
```javascript
// SAFE - Default behavior
const safeResponse = await fetch('/api/wallet/list', {
    headers: { 'Authorization': `Bearer ${token}` }
});

// DANGEROUS - Development only!
const dangerousResponse = await fetch('/api/wallet/list?include_mnemonics=true', {
    headers: { 'Authorization': `Bearer ${token}` }
});
```

### Python/Backend
```python
# SAFE - Default behavior
result = wallet_service.get_user_wallets(user_id)

# DANGEROUS - Development only!
result = wallet_service.get_user_wallets(user_id, include_mnemonics=True)
```

## Production Security Checklist

Before deploying to production:

- [ ] **Remove** `include_mnemonics=true` from all client code
- [ ] **Verify** no production endpoints expose mnemonics
- [ ] **Test** that `include_mnemonics=true` returns error in production
- [ ] **Monitor** logs for any mnemonic-related warnings
- [ ] **Document** this feature as development-only

## Error Handling

If mnemonic decryption fails:
```json
{
    "mnemonic": "DECRYPTION_FAILED"
}
```

If mnemonic decryption has an error:
```json
{
    "mnemonic": "DECRYPTION_ERROR"
}
```

---

## 🚨 FINAL WARNING 🚨

**THIS IS NOT A PRODUCTION FEATURE!**

**STAY HARD!** 🔥 But stay **SECURE**! 

Never compromise security for convenience. This feature exists ONLY for development and testing purposes.

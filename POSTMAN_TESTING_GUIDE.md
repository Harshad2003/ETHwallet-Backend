# 🔥 CypherD Wallet Backend - Postman Testing Guide

**BULLETPROOF API Testing with Postman Collection**

## 🚀 Quick Setup

### 1. Import Collection
1. Open Postman
2. Click "Import" button
3. Select `CypherD_Wallet_Backend.postman_collection.json`
4. Collection will be imported with all endpoints

### 2. Environment Setup
The collection includes environment variables that auto-populate:
- `base_url`: http://localhost:5001
- `access_token`: Auto-saved from login
- `refresh_token`: Auto-saved from login
- `wallet_address`: Auto-saved from wallet creation
- `mnemonic_phrase`: Auto-saved from wallet creation
- `transfer_message`: Auto-saved from transfer preparation
- `signature`: Auto-saved from message signing
- `transaction_id`: Auto-saved from transaction responses

## 🧪 Testing Workflow

### **Phase 1: Authentication Testing**

1. **Health Check**
   - Endpoint: `GET /api/health`
   - Purpose: Verify API is running
   - Expected: 200 OK with status "healthy"

2. **User Signup**
   - Endpoint: `POST /api/auth/signup`
   - Body: Update email to unique value
   - Expected: 201 Created with user data and tokens
   - **Auto-saves**: `access_token`, `refresh_token`

3. **User Signin**
   - Endpoint: `POST /api/auth/signin`
   - Body: Use same credentials as signup
   - Expected: 200 OK with user data and tokens
   - **Auto-saves**: `access_token`, `refresh_token`

4. **Get Profile**
   - Endpoint: `GET /api/auth/profile`
   - Headers: Uses auto-saved `access_token`
   - Expected: 200 OK with user profile

5. **Update Profile**
   - Endpoint: `PUT /api/auth/profile`
   - Body: Update first_name, last_name, phone_number
   - Expected: 200 OK with updated profile

6. **Change Password**
   - Endpoint: `POST /api/auth/change-password`
   - Body: Provide current and new password
   - Expected: 200 OK with success message

7. **Refresh Token**
   - Endpoint: `POST /api/auth/refresh`
   - Headers: Uses auto-saved `refresh_token`
   - Expected: 200 OK with new `access_token`

### **Phase 2: Wallet Management Testing**

8. **Create New Wallet**
   - Endpoint: `POST /api/wallet/create`
   - Body: Set wallet_name and is_primary
   - Expected: 201 Created with wallet data and mnemonic
   - **Auto-saves**: `wallet_address`, `mnemonic_phrase`

9. **Import Existing Wallet**
   - Endpoint: `POST /api/wallet/import`
   - Body: Use test mnemonic: "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
   - Expected: 201 Created with imported wallet

10. **Get Wallet Balance**
    - Endpoint: `GET /api/wallet/balance/{wallet_address}`
    - Uses auto-saved `wallet_address`
    - Expected: 200 OK with balance information

11. **List User Wallets**
    - Endpoint: `GET /api/wallet/list`
    - Expected: 200 OK with array of user wallets

### **Phase 3: Price & Conversion Testing**

12. **Get ETH Price**
    - Endpoint: `GET /api/wallet/price/eth`
    - Expected: 200 OK with current ETH price in USD

13. **Convert USD to ETH**
    - Endpoint: `POST /api/wallet/price/convert`
    - Body: `{"usd_amount": 1000.0}`
    - Expected: 200 OK with ETH amount and conversion rate

### **Phase 4: Transaction Testing**

14. **Prepare Transfer (ETH)**
    - Endpoint: `POST /api/wallet/transfer/prepare`
    - Body: Set from_address, to_address, amount
    - Expected: 200 OK with transfer message
    - **Auto-saves**: `transfer_message`

15. **Prepare Transfer (USD)**
    - Endpoint: `POST /api/wallet/transfer/prepare`
    - Body: Set from_address, to_address, amount_usd
    - Expected: 200 OK with transfer message and ETH amount

16. **Sign Message**
    - Endpoint: `POST /api/wallet/sign-message`
    - Body: Use auto-saved `transfer_message`, `wallet_address`, `mnemonic_phrase`
    - Expected: 200 OK with signature
    - **Auto-saves**: `signature`

17. **Execute Transfer**
    - Endpoint: `POST /api/wallet/transfer/execute`
    - Body: Use auto-saved `transfer_message`, `signature`, `wallet_address`
    - Expected: 200 OK with transaction data
    - **Auto-saves**: `transaction_id`

### **Phase 5: Transaction History Testing**

18. **Get Transaction History**
    - Endpoint: `GET /api/transactions/history/{wallet_address}`
    - Uses auto-saved `wallet_address`
    - Expected: 200 OK with transaction array

19. **Get Transaction Stats**
    - Endpoint: `GET /api/transactions/stats/{wallet_address}`
    - Uses auto-saved `wallet_address`
    - Expected: 200 OK with statistics

20. **Get Transaction Details**
    - Endpoint: `GET /api/transactions/{transaction_id}`
    - Uses auto-saved `transaction_id`
    - Expected: 200 OK with transaction details

21. **Get Recent Transactions**
    - Endpoint: `GET /api/transactions/recent`
    - Expected: 200 OK with recent transactions

22. **Send Transaction (Alternative)**
    - Endpoint: `POST /api/transactions/send`
    - Body: Complete transaction data
    - Expected: 200 OK with transaction result

## 🔥 Advanced Testing Scenarios

### **Error Handling Tests**

1. **Invalid Authentication**
   - Test with expired/invalid tokens
   - Expected: 401 Unauthorized

2. **Invalid Input**
   - Test with malformed JSON
   - Test with missing required fields
   - Expected: 400 Bad Request

3. **Wallet Not Found**
   - Test with non-existent wallet address
   - Expected: 404 Not Found

4. **Insufficient Balance**
   - Test transfer with amount > balance
   - Expected: 400 Bad Request with error message

### **Edge Cases**

1. **Same Wallet Transfer**
   - Try to transfer to same address
   - Expected: 400 Bad Request

2. **Zero Amount Transfer**
   - Try to transfer 0 ETH
   - Expected: 400 Bad Request

3. **Invalid Mnemonic**
   - Try to import invalid mnemonic
   - Expected: 400 Bad Request

4. **Invalid Signature**
   - Try to execute with wrong signature
   - Expected: 400 Bad Request

## 📊 Expected Response Formats

### **Success Response**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

### **Error Response**
```json
{
  "error": "Error message",
  "success": false
}
```

### **User Response**
```json
{
  "success": true,
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2024-01-01T00:00:00"
  },
  "access_token": "jwt_token",
  "refresh_token": "refresh_token"
}
```

### **Wallet Response**
```json
{
  "success": true,
  "wallet": {
    "id": "uuid",
    "address": "0x...",
    "balance": 5.123456,
    "wallet_name": "My Wallet",
    "is_primary": true
  },
  "mnemonic": "word1 word2 ... word12"
}
```

### **Transaction Response**
```json
{
  "success": true,
  "transaction": {
    "id": "uuid",
    "from_address": "0x...",
    "to_address": "0x...",
    "amount": 0.5,
    "status": "completed",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

## 🚨 Troubleshooting

### **Common Issues**

1. **Connection Refused**
   - Ensure backend is running on port 5001
   - Check if `base_url` is correct

2. **Authentication Errors**
   - Verify JWT tokens are being saved
   - Check if tokens are expired

3. **Wallet Not Found**
   - Ensure wallet was created successfully
   - Check if `wallet_address` is saved correctly

4. **Signature Verification Failed**
   - Ensure mnemonic matches wallet address
   - Check if message was prepared correctly

### **Debug Tips**

1. **Check Environment Variables**
   - Verify all auto-saved variables are populated
   - Manually set variables if needed

2. **Response Inspection**
   - Check response status codes
   - Read error messages carefully

3. **Request Body Validation**
   - Ensure JSON is properly formatted
   - Verify all required fields are present

## 🔥 STAY HARD!

This Postman collection is designed to TEST EVERYTHING. No endpoint is left untested. No scenario is ignored. 

**Run through this collection and DOMINATE your API testing!**

---

**Need help?** Check the backend logs for detailed error messages.
**Want more tests?** Add custom test scripts in Postman for additional validation.

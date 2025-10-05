# 🔥 FRONTEND MNEMONIC FLOW - COMPLETE GUIDE

## **CRITICAL SECURITY WARNING** ⚠️

**THIS IS DEVELOPMENT-ONLY FUNCTIONALITY!**

- **NEVER** use mnemonic endpoints in production
- **NEVER** store mnemonics in localStorage/sessionStorage
- **ALWAYS** use server-side signing for production

---

## **COMPLETE FRONTEND MNEMONIC FLOW**

### **Step 1: Wallet Creation**
```http
POST {{base_url}}/api/wallet/create
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "wallet_name": "My Wallet",
    "is_primary": true
}
```

**Response:**
```json
{
    "success": true,
    "wallet": {
        "address": "0xC1565Bbc800D86d4F28a7C55b2C53f6c42400721",
        "balance": 9.330582,
        "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
        "wallet_name": "My Wallet",
        "is_primary": true
    }
}
```

**Postman Auto-Saves:**
```javascript
pm.environment.set('wallet_address', pm.response.json().wallet.address);
pm.environment.set('mnemonic_phrase', pm.response.json().wallet.mnemonic);
```

### **Step 2: Wallet List (Get All Mnemonics)**
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
            "mnemonic": "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
            "wallet_name": "My Wallet"
        },
        {
            "address": "0xa7ac606529AbFa32F2fBb3Dad07a925D482Ee55D",
            "balance": 4.621475,
            "mnemonic": "protect road input panda abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about",
            "wallet_name": "My Second Wallet"
        }
    ]
}
```

### **Step 3: Sign Message (Use Mnemonic)**
```http
POST {{base_url}}/api/wallet/sign-message
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
    "message": "{{transfer_message}}",
    "wallet_address": "{{wallet_address}}",
    "mnemonic": "{{mnemonic_phrase}}"
}
```

**Response:**
```json
{
    "success": true,
    "signature": "0x1234567890abcdef...",
    "message": "Transfer 0.5 ETH to 0x... from 0x..."
}
```

---

## **FRONTEND IMPLEMENTATION STRATEGIES**

### **Strategy 1: Postman Environment Variables (Current)**
```javascript
// Auto-saved in Postman environment
pm.environment.set('mnemonic_phrase', pm.response.json().wallet.mnemonic);

// Used in subsequent requests
{
    "mnemonic": "{{mnemonic_phrase}}"
}
```

### **Strategy 2: JavaScript Frontend (Development)**
```javascript
class WalletManager {
    constructor() {
        this.walletMnemonics = new Map(); // Memory only!
    }
    
    async createWallet(walletName, isPrimary = false) {
        const response = await fetch('/api/wallet/create', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                wallet_name: walletName,
                is_primary: isPrimary
            })
        });
        
        const data = await response.json();
        if (data.success) {
            // Store mnemonic in memory (NOT localStorage!)
            this.walletMnemonics.set(data.wallet.address, data.wallet.mnemonic);
            return data.wallet;
        }
        throw new Error(data.error);
    }
    
    async loadAllWallets() {
        const response = await fetch('/api/wallet/list?include_mnemonics=true', {
            headers: {
                'Authorization': `Bearer ${this.token}`
            }
        });
        
        const data = await response.json();
        if (data.success) {
            // Store all mnemonics in memory
            data.wallets.forEach(wallet => {
                this.walletMnemonics.set(wallet.address, wallet.mnemonic);
            });
            return data.wallets;
        }
        throw new Error(data.error);
    }
    
    async signMessage(walletAddress, message) {
        const mnemonic = this.walletMnemonics.get(walletAddress);
        if (!mnemonic) {
            throw new Error('Mnemonic not found for wallet');
        }
        
        const response = await fetch('/api/wallet/sign-message', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${this.token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                wallet_address: walletAddress,
                mnemonic: mnemonic
            })
        });
        
        const data = await response.json();
        if (data.success) {
            return data.signature;
        }
        throw new Error(data.error);
    }
    
    // SECURITY: Clear mnemonics from memory
    clearMnemonics() {
        this.walletMnemonics.clear();
    }
}

// Usage
const walletManager = new WalletManager();
await walletManager.createWallet("My Wallet", true);
await walletManager.loadAllWallets();
const signature = await walletManager.signMessage(walletAddress, transferMessage);
```

### **Strategy 3: React Hook (Development)**
```javascript
import { useState, useCallback } from 'react';

export const useWalletMnemonics = (token) => {
    const [walletMnemonics, setWalletMnemonics] = useState(new Map());
    
    const loadWallets = useCallback(async () => {
        const response = await fetch('/api/wallet/list?include_mnemonics=true', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        
        const data = await response.json();
        if (data.success) {
            const mnemonicMap = new Map();
            data.wallets.forEach(wallet => {
                mnemonicMap.set(wallet.address, wallet.mnemonic);
            });
            setWalletMnemonics(mnemonicMap);
            return data.wallets;
        }
        throw new Error(data.error);
    }, [token]);
    
    const getMnemonic = useCallback((walletAddress) => {
        return walletMnemonics.get(walletAddress);
    }, [walletMnemonics]);
    
    const clearMnemonics = useCallback(() => {
        setWalletMnemonics(new Map());
    }, []);
    
    return {
        loadWallets,
        getMnemonic,
        clearMnemonics,
        hasMnemonics: walletMnemonics.size > 0
    };
};
```

---

## **SECURITY BEST PRACTICES**

### **✅ DO (Development):**
- Store mnemonics in **memory only**
- Use **Map** or **Set** for temporary storage
- **Clear mnemonics** when done
- **Log security warnings** when mnemonics are accessed
- Use **HTTPS** for all API calls

### **❌ NEVER DO:**
- Store mnemonics in **localStorage**
- Store mnemonics in **sessionStorage**
- Store mnemonics in **cookies**
- Store mnemonics in **database** (frontend)
- **Log mnemonics** to console
- **Send mnemonics** in URLs

### **🔒 Production Security:**
```javascript
// Production: Use server-side signing
const transferResponse = await fetch('/api/wallet/transfer/execute', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: JSON.stringify({
        from_address: walletAddress,
        to_address: recipientAddress,
        amount: amount
    })
});

// Server handles signing internally - no mnemonic exposure!
```

---

## **POSTMAN COLLECTION UPDATES**

The Postman collection now includes:

1. **Create Wallet** - Auto-saves `mnemonic_phrase`
2. **List Wallets (Safe)** - No mnemonics
3. **List Wallets (With Mnemonics)** - Includes mnemonics
4. **Sign Message** - Uses saved `mnemonic_phrase`

### **Environment Variables:**
- `{{wallet_address}}` - Current wallet address
- `{{mnemonic_phrase}}` - Current wallet mnemonic
- `{{transfer_message}}` - Transfer message to sign
- `{{signature}}` - Generated signature

---

## **TESTING FLOW**

1. **Create Wallet** → Saves mnemonic to environment
2. **List Wallets** → Verify mnemonic is available
3. **Prepare Transfer** → Creates transfer message
4. **Sign Message** → Uses saved mnemonic
5. **Execute Transfer** → Completes transaction

---

## **🚨 FINAL WARNING 🚨**

**THIS IS DEVELOPMENT-ONLY FUNCTIONALITY!**

**STAY HARD!** 🔥 But stay **SECURE**!

- **NEVER** expose mnemonic endpoints in production
- **ALWAYS** use server-side signing for production
- **NEVER** store mnemonics in persistent storage
- **ALWAYS** clear mnemonics from memory when done

The frontend gets mnemonics through:
1. **Wallet creation** response
2. **Wallet list** with `include_mnemonics=true`
3. **Manual input** for wallet import

But remember - this is **ONLY** for development and testing!

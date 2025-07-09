# Web3Forms Setup Instructions

## Getting a Valid Access Key

The current access key in your `.env` file appears to be invalid or expired. Here's how to get a new one:

### Step 1: Go to Web3Forms
1. Visit [https://web3forms.com](https://web3forms.com)
2. Enter your email address in the form
3. Click "Create Form"

### Step 2: Check Your Email
1. Check your email inbox for a message from Web3Forms
2. Click the activation/verification link in the email
3. This will take you to a page showing your access key

### Step 3: Copy Your Access Key
1. On the Web3Forms dashboard, you'll see your access key
2. It will look something like: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
3. Copy this key

### Step 4: Update Your .env File
Replace the current key in `backend/.env`:

```
# Replace this line:
WEB3FORMS_ACCESS_KEY=0500b0a1-da3f-4880-a533-d5fa938fffff

# With your new key:
WEB3FORMS_ACCESS_KEY=your_new_access_key_here
```

### Step 5: Restart Your Backend
After updating the access key, restart your backend server for the changes to take effect.

## Testing the Setup

1. Make sure your backend is running
2. Send a POST request to `/api/auth/forgot-password` with a test email
3. Check the server logs to see if the email was sent successfully

## Troubleshooting

If you still get errors:

1. **403 Forbidden**: Your access key might not be activated or might have restrictions
2. **Invalid Key**: Double-check that you copied the key correctly
3. **Rate Limiting**: Web3Forms has rate limits - wait a few minutes between tests

## Alternative: Use Development Mode Only

If you want to skip email sending for now, you can:

1. Set `ENVIRONMENT=development` in your `.env`
2. The system will only print reset links to the console
3. This is perfect for development and testing

The password reset functionality works perfectly in development mode!

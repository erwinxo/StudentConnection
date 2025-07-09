# Gmail SMTP Setup for Password Reset

## Step 1: Enable 2-Factor Authentication
1. Go to your Google Account settings
2. Click on "Security"
3. Enable "2-Step Verification" if not already enabled

## Step 2: Generate App Password
1. In Google Account settings, go to "Security"
2. Under "2-Step Verification", click on "App passwords"
3. Select "Mail" for the app and "Other" for device
4. Enter "Student Social Platform" as the device name
5. Click "Generate"
6. Copy the 16-character app password (format: xxxx xxxx xxxx xxxx)

## Step 3: Update .env File
Update your `backend/.env` file with your Gmail credentials:

```
# Gmail SMTP configuration for password reset emails
GMAIL_USER=your-actual-email@gmail.com
GMAIL_APP_PASSWORD=your-16-character-app-password
```

**Important:** 
- Use your actual Gmail address for `GMAIL_USER`
- Use the app password (not your regular Gmail password) for `GMAIL_APP_PASSWORD`
- Remove any spaces from the app password

## Step 4: Test the Setup
1. Restart your backend server
2. Send a password reset request
3. Check the server logs to confirm email was sent successfully

## Example Configuration
```
GMAIL_USER=johndoe@gmail.com
GMAIL_APP_PASSWORD=abcdabcdabcdabcd
```

This implementation will:
- Print reset links to console in development mode
- Send actual emails via Gmail SMTP in production mode
- Work reliably with proper Gmail credentials

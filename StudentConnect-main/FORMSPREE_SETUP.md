# How to Set Up Formspree for Password Resets

Follow these steps to get a Formspree URL to use in the backend for sending password reset emails.

### 1. Create a Formspree Account
- Go to [https://formspree.io/](https://formspree.io/) and sign up for a free account.

### 2. Create a New Form
- From your Formspree dashboard, click **+ New form**.
- Give your form a name (e.g., "Password Reset") and click **Create Form**.

### 3. Get Your Form Endpoint URL
- After creating the form, you will be taken to the **Integration** tab.
- You will see a URL that looks like this:
  ```
  https://formspree.io/f/YOUR_FORM_ID
  ```
- **Copy this entire URL.** This is what you will use in your `.env` file.

### 4. Update Your `.env` File
- Open the `backend/.env` file in your project.
- Add a new line for your Formspree URL and comment out the old Web3Forms key:
  ```env
  # ... other variables ...

  # Web3Forms configuration (no longer used)
  # WEB3FORMS_ACCESS_KEY=your-old-web3forms-key

  # Formspree configuration
  FORMSPREE_FORM_URL=https://formspree.io/f/YOUR_FORM_ID

  FRONTEND_URL=http://localhost:3000
  ```
- **Replace `https://formspree.io/f/YOUR_FORM_ID` with the actual URL you copied.**

### 5. Restart the Backend Server
- After you save the `.env` file, stop and restart the backend server.
- The application will now use Formspree to send emails.

### Important Note
- The first time you send an email via the API, Formspree may require you to check your email and verify that you want to allow submissions from your application.

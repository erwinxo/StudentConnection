import os
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from models.database import users_collection

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

RESET_TOKEN_EXPIRE_HOURS = 24

print("=== EMAIL UTILITY CONFIGURATION ===")
print(f"Environment: {ENVIRONMENT}")
print(f"Gmail configured: {bool(GMAIL_USER and GMAIL_APP_PASSWORD)}")
print(f"Frontend URL: {FRONTEND_URL}")
print("=== END CONFIGURATION ===")

def generate_reset_token() -> str:
    """Generate a secure reset token"""
    return secrets.token_urlsafe(32)

async def store_reset_token(email: str, token: str) -> bool:
    """Store reset token in database with expiration"""
    try:
        expiration = datetime.utcnow() + timedelta(hours=RESET_TOKEN_EXPIRE_HOURS)
        
        result = await users_collection.update_one(
            {"email": email},
            {
                "$set": {
                    "reset_token": token,
                    "reset_token_expires": expiration
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error storing reset token: {e}")
        return False

async def validate_reset_token(token: str):
    """Validate reset token and return user if valid"""
    try:
        user = await users_collection.find_one({
            "reset_token": token,
            "reset_token_expires": {"$gt": datetime.utcnow()}
        })
        return user
    except Exception as e:
        print(f"Error validating reset token: {e}")
        return None

async def clear_reset_token(email: str) -> bool:
    """Clear reset token after successful password reset"""
    try:
        result = await users_collection.update_one(
            {"email": email},
            {
                "$unset": {
                    "reset_token": "",
                    "reset_token_expires": ""
                }
            }
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Error clearing reset token: {e}")
        return False

def send_reset_email(email: str, token: str) -> bool:
    """Send password reset email using Gmail SMTP."""
    
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"
    
    # In development, we print the link to the console for easy testing
    if ENVIRONMENT == "development":
        print("=" * 60)
        print("📧 DEVELOPMENT MODE - PASSWORD RESET LINK")
        print("=" * 60)
        print(f"Reset link for {email}:")
        print(f"{reset_link}")
        print("=" * 60)
        print("Copy the above link to test password reset functionality.")
        print("=" * 60)
        
        # Also try to send email if Gmail is configured
        if GMAIL_USER and GMAIL_APP_PASSWORD and GMAIL_USER != "your-email@gmail.com":
            print("Also attempting to send email via Gmail SMTP...")
            success = _send_via_gmail(email, reset_link)
            if success:
                print("✅ Gmail SMTP email sent successfully!")
            else:
                print("❌ Gmail SMTP failed, but development link provided above.")
        
        return True

    # In production, we must send a real email
    if not GMAIL_USER or not GMAIL_APP_PASSWORD or GMAIL_USER == "your-email@gmail.com":
        print("❌ PRODUCTION ERROR: Gmail credentials are not configured.")
        return False

    print(f"🚀 Sending production password reset email to {email}...")
    return _send_via_gmail(email, reset_link)


def _send_via_gmail(email: str, reset_link: str) -> bool:
    """
    Send email using Gmail SMTP server.
    
    Args:
        email (str): The recipient's email address.
        reset_link (str): The full URL for the user to reset their password.
        
    Returns:
        bool: True if the email was sent successfully, False otherwise.
    """
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Password Reset Request - StudentConnect"
        msg['From'] = GMAIL_USER
        msg['To'] = email

        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Password Reset - Student Social</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 20px; background-color: #f4f4f4;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
                
                <!-- Header -->
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: 300;">🔐 Password Reset Request</h1>
                    <p style="margin: 10px 0 0 0; opacity: 0.9; font-size: 16px;">StudentConnect</p>
                </div>
                
                <!-- Content -->
                <div style="padding: 40px 30px; background-color: white;">
                    <p style="font-size: 16px; margin-bottom: 20px;">Hello,</p>
                    
                    <p style="font-size: 16px; margin-bottom: 20px;">We received a request to reset your password for your Student Social account. If you made this request, click the button below to create a new password:</p>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{reset_link}" style="display: inline-block; padding: 15px 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 16px;">
                            Reset My Password
                        </a>
                    </div>
                    
                    <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; color: #856404; padding: 20px; border-radius: 5px; margin: 25px 0;">
                        <strong>⚠️ Security Notice:</strong>
                        <ul style="margin: 10px 0; padding-left: 20px;">
                            <li>This link will expire in 24 hours for your security</li>
                            <li>If you didn't request this reset, please ignore this email</li>
                            <li>Never share this link with anyone</li>
                        </ul>
                    </div>
                    
                    <p style="font-size: 14px; margin-top: 30px;">If the button above doesn't work, copy and paste this link into your browser:</p>
                    <p style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; word-break: break-all; font-size: 14px;">
                        <a href="{reset_link}" style="color: #667eea; text-decoration: none;">{reset_link}</a>
                    </p>
                    
                    <p style="margin-top: 30px; color: #666; font-size: 14px;">
                        If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.
                    </p>
                </div>
                
                <!-- Footer -->
                <div style="padding: 30px 20px; text-align: center; color: #666; font-size: 14px; border-top: 1px solid #eee; background-color: #f9f9f9;">
                    <p style="margin: 0;">This is an automated message from StudentConnect.</p>
                    <p style="margin: 5px 0 0 0;">© 2025 StudentConnect. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to Gmail SMTP server and send email
        print(f"📧 Connecting to Gmail SMTP server...")
        
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable security
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            
            print(f"📤 Sending email to {email}...")
            server.send_message(msg)
            
        print(f"✅ Successfully sent password reset email to {email} via Gmail SMTP!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print(f"❌ Gmail SMTP Authentication failed. Check your email and app password.")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ Gmail SMTP error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error sending email: {e}")
        return False

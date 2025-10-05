"""
Email service for CypherD Wallet Backend
BULLETPROOF email notifications using proven SellMyShow configuration
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class EmailService:
    """Service class for email operations - BULLETPROOF configuration"""
    
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None):
        # Use proven SellMyShow configuration as default
        self.smtp_server = smtp_server or os.environ.get('SMTP_SERVER', 'mail.privateemail.com')
        self.smtp_port = smtp_port or int(os.environ.get('SMTP_PORT', 587))
        self.username = username or os.environ.get('SMTP_USERNAME', 'tickets@sellmyshow.com')
        self.password = password or os.environ.get('SMTP_PASSWORD', 'HarSah$Bt1ckets$')
        self.use_tls = True
    
    def send_transaction_notification(self, to_email, transaction_data):
        """Send transaction notification email using proven SellMyShow method"""
        try:
            if not self.username or not self.password:
                logger.warning("Email credentials not configured, skipping email notification")
                return {
                    'success': False,
                    'error': 'Email service not configured'
                }
            
            subject = f"CypherD Wallet - Transaction Notification"
            html_body = self._create_transaction_email_body(transaction_data)
            
            # Use proven SellMyShow email sending method
            return self._send_email(to_email, subject, html_body)
            
        except Exception as e:
            logger.error(f"Send transaction notification error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to send notification: {str(e)}'
            }
    
    def send_wallet_created_notification(self, to_email, wallet_data):
        """Send wallet created notification email using proven SellMyShow method"""
        try:
            if not self.username or not self.password:
                logger.warning("Email credentials not configured, skipping email notification")
                return {
                    'success': False,
                    'error': 'Email service not configured'
                }
            
            subject = f"CypherD Wallet - New Wallet Created"
            html_body = self._create_wallet_created_email_body(wallet_data)
            
            # Use proven SellMyShow email sending method
            return self._send_email(to_email, subject, html_body)
            
        except Exception as e:
            logger.error(f"Send wallet created notification error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to send notification: {str(e)}'
            }
    
    def _send_email(self, to_email, subject, html_body):
        """Core email sending method using proven SellMyShow approach"""
        try:
            # Create a multipart/alternative container (proven SellMyShow method)
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.username
            msg["To"] = to_email

            # Optional plain-text version
            text_body = "Please view this email in an HTML-compatible client."

            # Attach plain text and HTML versions
            msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            # Send using proven SellMyShow method
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return {
                'success': True,
                'message': 'Email sent successfully'
            }
            
        except Exception as e:
            logger.error(f"Email sending failed: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to send email: {str(e)}'
            }
    
    def _create_transaction_email_body(self, transaction_data):
        """Create HTML email body for transaction notification"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return f"""
        <html>
        <body style="margin:0; padding:0; font-family: 'Inter', Arial, sans-serif; background-color:#f8fafc; color:#111827;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:auto; background:#ffffff; border:1px solid #e5e7eb; box-shadow:0 4px 6px rgba(0,0,0,0.1); border-radius:8px; overflow:hidden;">
                <!-- Header -->
                <tr>
                    <td style="background-color:#dc2626; padding:20px; text-align:center; color:#ffffff; font-size:20px; font-weight:bold;">
                        CypherD Wallet - Transaction Notification
                    </td>
                </tr>

                <!-- Body -->
                <tr>
                    <td style="padding:20px;">
                        <p style="margin:0 0 15px 0;">Hello,</p>
                        <p style="margin:0 0 20px 0;">Your transaction has been completed successfully!</p>

                        <table cellpadding="6" cellspacing="0" style="width:100%; border-collapse:collapse; background-color:#f8fafc; border-radius:6px;">
                            <tr>
                                <td><strong>From Address:</strong></td>
                                <td>{transaction_data.get('from_address', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td><strong>To Address:</strong></td>
                                <td>{transaction_data.get('to_address', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td><strong>Amount:</strong></td>
                                <td>{transaction_data.get('amount', 0):.6f} ETH</td>
                            </tr>
                            <tr>
                                <td><strong>USD Value:</strong></td>
                                <td>${transaction_data.get('amount_usd', 0):.2f}</td>
                            </tr>
                            <tr>
                                <td><strong>Status:</strong></td>
                                <td>{transaction_data.get('status', 'completed')}</td>
                            </tr>
                            <tr>
                                <td><strong>Timestamp:</strong></td>
                                <td>{timestamp}</td>
                            </tr>
                        </table>

                        <div style="background-color:#ecfdf5; border:1px solid #10b981; padding:15px; border-radius:8px; margin:20px 0;">
                            <h4 style="color:#065f46; margin-top:0;">✅ Transaction Successful</h4>
                            <p style="color:#065f46; margin-bottom:0;">
                                Your transaction has been processed and confirmed on the blockchain.
                            </p>
                        </div>

                        <p style="font-size:14px; color:#6b7280; text-align:center;">
                            Thank you for using CypherD Wallet!<br>
                            Your Web3 transactions are secure and transparent.
                        </p>
                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td style="background-color:#1f2937; color:#ffffff; text-align:center; padding:15px; font-size:14px;">
                        STAY HARD! 🔥
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
    
    def _create_wallet_created_email_body(self, wallet_data):
        """Create HTML email body for wallet created notification"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return f"""
        <html>
        <body style="margin:0; padding:0; font-family: 'Inter', Arial, sans-serif; background-color:#f8fafc; color:#111827;">
            <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:auto; background:#ffffff; border:1px solid #e5e7eb; box-shadow:0 4px 6px rgba(0,0,0,0.1); border-radius:8px; overflow:hidden;">
                <!-- Header -->
                <tr>
                    <td style="background-color:#dc2626; padding:20px; text-align:center; color:#ffffff; font-size:20px; font-weight:bold;">
                        CypherD Wallet - New Wallet Created
                    </td>
                </tr>

                <!-- Body -->
                <tr>
                    <td style="padding:20px;">
                        <p style="margin:0 0 15px 0;">Hello,</p>
                        <p style="margin:0 0 20px 0;">Your new wallet has been created successfully!</p>

                        <table cellpadding="6" cellspacing="0" style="width:100%; border-collapse:collapse; background-color:#f8fafc; border-radius:6px;">
                            <tr>
                                <td><strong>Wallet Address:</strong></td>
                                <td>{wallet_data.get('address', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td><strong>Wallet Name:</strong></td>
                                <td>{wallet_data.get('wallet_name', 'N/A')}</td>
                            </tr>
                            <tr>
                                <td><strong>Initial Balance:</strong></td>
                                <td>{wallet_data.get('balance', 0):.6f} ETH</td>
                            </tr>
                            <tr>
                                <td><strong>Created:</strong></td>
                                <td>{timestamp}</td>
                            </tr>
                        </table>

                        <div style="background-color:#fff3cd; border:1px solid #ffeaa7; padding:15px; border-radius:8px; margin:20px 0;">
                            <h4 style="color:#856404; margin-top:0;">⚠️ Important Security Notice</h4>
                            <p style="color:#856404; margin-bottom:0;">
                                Your wallet has been created successfully. Please ensure you have securely stored your mnemonic phrase.
                                Never share your mnemonic phrase with anyone.
                            </p>
                        </div>

                        <p style="font-size:14px; color:#6b7280; text-align:center;">
                            Welcome to CypherD Wallet!<br>
                            Your Web3 journey starts now.
                        </p>
                    </td>
                </tr>

                <!-- Footer -->
                <tr>
                    <td style="background-color:#1f2937; color:#ffffff; text-align:center; padding:15px; font-size:14px;">
                        STAY HARD! 🔥
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

# Global instance - Initialize with configuration
import os
from dotenv import load_dotenv

load_dotenv()

email_service = EmailService(
    smtp_server=os.environ.get('SMTP_SERVER', 'smtp.gmail.com'),
    smtp_port=int(os.environ.get('SMTP_PORT', 587)),
    username=os.environ.get('SMTP_USERNAME'),
    password=os.environ.get('SMTP_PASSWORD')
)

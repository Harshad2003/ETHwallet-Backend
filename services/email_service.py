"""
Email service for CypherD Wallet Backend
BULLETPROOF email notifications for transactions
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    """Service class for email operations"""
    
    def __init__(self, smtp_server=None, smtp_port=None, username=None, password=None):
        self.smtp_server = smtp_server or 'smtp.gmail.com'
        self.smtp_port = smtp_port or 587
        self.username = username
        self.password = password
        self.use_tls = True
    
    def send_transaction_notification(self, to_email, transaction_data):
        """Send transaction notification email"""
        try:
            if not self.username or not self.password:
                logger.warning("Email credentials not configured, skipping email notification")
                return {
                    'success': False,
                    'error': 'Email service not configured'
                }
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = f"CypherD Wallet - Transaction Notification"
            
            # Create email body
            body = self._create_transaction_email_body(transaction_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            
            return {
                'success': True,
                'message': 'Transaction notification sent successfully'
            }
            
        except Exception as e:
            logger.error(f"Send transaction notification error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to send notification: {str(e)}'
            }
    
    def send_wallet_created_notification(self, to_email, wallet_data):
        """Send wallet created notification email"""
        try:
            if not self.username or not self.password:
                logger.warning("Email credentials not configured, skipping email notification")
                return {
                    'success': False,
                    'error': 'Email service not configured'
                }
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = f"CypherD Wallet - New Wallet Created"
            
            # Create email body
            body = self._create_wallet_created_email_body(wallet_data)
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            if self.use_tls:
                server.starttls()
            server.login(self.username, self.password)
            
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            
            return {
                'success': True,
                'message': 'Wallet created notification sent successfully'
            }
            
        except Exception as e:
            logger.error(f"Send wallet created notification error: {str(e)}")
            return {
                'success': False,
                'error': f'Failed to send notification: {str(e)}'
            }
    
    def _create_transaction_email_body(self, transaction_data):
        """Create HTML email body for transaction notification"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #1a1a1a; color: white; padding: 20px; text-align: center;">
                <h1>🔥 CypherD Wallet</h1>
            </div>
            
            <div style="padding: 20px; background-color: #f5f5f5;">
                <h2>Transaction Notification</h2>
                
                <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>Transaction Details</h3>
                    <p><strong>From:</strong> {transaction_data.get('from_address', 'N/A')}</p>
                    <p><strong>To:</strong> {transaction_data.get('to_address', 'N/A')}</p>
                    <p><strong>Amount:</strong> {transaction_data.get('amount', 0):.6f} ETH</p>
                    {f"<p><strong>USD Value:</strong> ${transaction_data.get('amount_usd', 0):.2f}</p>" if transaction_data.get('amount_usd') else ""}
                    <p><strong>Status:</strong> {transaction_data.get('status', 'N/A')}</p>
                    <p><strong>Timestamp:</strong> {timestamp}</p>
                </div>
                
                <div style="text-align: center; margin: 20px 0;">
                    <p style="color: #666; font-size: 14px;">
                        This is an automated notification from CypherD Wallet.<br>
                        If you didn't perform this transaction, please contact support immediately.
                    </p>
                </div>
            </div>
            
            <div style="background-color: #1a1a1a; color: white; padding: 20px; text-align: center;">
                <p>STAY HARD! 🔥</p>
            </div>
        </body>
        </html>
        """
    
    def _create_wallet_created_email_body(self, wallet_data):
        """Create HTML email body for wallet created notification"""
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        return f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #1a1a1a; color: white; padding: 20px; text-align: center;">
                <h1>🔥 CypherD Wallet</h1>
            </div>
            
            <div style="padding: 20px; background-color: #f5f5f5;">
                <h2>New Wallet Created</h2>
                
                <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3>Wallet Details</h3>
                    <p><strong>Address:</strong> {wallet_data.get('address', 'N/A')}</p>
                    <p><strong>Name:</strong> {wallet_data.get('wallet_name', 'N/A')}</p>
                    <p><strong>Balance:</strong> {wallet_data.get('balance', 0):.6f} ETH</p>
                    <p><strong>Created:</strong> {timestamp}</p>
                </div>
                
                <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <h4 style="color: #856404; margin-top: 0;">⚠️ Important Security Notice</h4>
                    <p style="color: #856404; margin-bottom: 0;">
                        Your wallet has been created successfully. Please ensure you have securely stored your mnemonic phrase.
                        Never share your mnemonic phrase with anyone.
                    </p>
                </div>
                
                <div style="text-align: center; margin: 20px 0;">
                    <p style="color: #666; font-size: 14px;">
                        Welcome to CypherD Wallet!<br>
                        Your Web3 journey starts now.
                    </p>
                </div>
            </div>
            
            <div style="background-color: #1a1a1a; color: white; padding: 20px; text-align: center;">
                <p>STAY HARD! 🔥</p>
            </div>
        </body>
        </html>
        """

# Global instance
email_service = EmailService()

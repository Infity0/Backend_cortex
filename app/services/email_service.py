import asyncio
from typing import Optional
from app.core.config import settings


class EmailService:
    """Email service for sending notifications"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
    
    async def send_email(self, to: str, subject: str, body: str):
        """Send email (mock implementation)"""
        # In production, use aiosmtplib to send real emails
        print(f"[EMAIL] To: {to}")
        print(f"[EMAIL] Subject: {subject}")
        print(f"[EMAIL] Body: {body}")
        print("-" * 50)
        
        # Mock delay
        await asyncio.sleep(0.1)
    
    async def send_verification_email(self, email: str, code: str):
        """Send email verification code"""
        subject = "Verify your Cortex AI account"
        body = f"""
        Welcome to Cortex AI!
        
        Your verification code is: {code}
        
        This code will expire in 24 hours.
        
        If you didn't create an account, please ignore this email.
        """
        await self.send_email(email, subject, body)
    
    async def send_password_reset_email(self, email: str, token: str):
        """Send password reset email"""
        reset_link = f"http://localhost:3000/reset-password?token={token}"
        subject = "Reset your Cortex AI password"
        body = f"""
        You requested to reset your password.
        
        Click the link below to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        """
        await self.send_email(email, subject, body)
    
    async def send_subscription_email(self, email: str, plan_name: str, success: bool):
        """Send subscription notification"""
        if success:
            subject = f"Welcome to {plan_name}!"
            body = f"""
            Your subscription to {plan_name} has been activated!
            
            You can now enjoy all the features of your plan.
            
            Thank you for choosing Cortex AI!
            """
        else:
            subject = "Payment Failed"
            body = f"""
            We couldn't process your payment for {plan_name}.
            
            Please check your payment method and try again.
            
            If you need help, contact our support team.
            """
        await self.send_email(email, subject, body)
    
    async def send_low_balance_notification(self, email: str, balance: int):
        """Send low token balance notification"""
        subject = "Low Token Balance"
        body = f"""
        Your token balance is running low: {balance} tokens remaining.
        
        Consider upgrading your subscription to continue generating images.
        
        Visit your dashboard to manage your subscription.
        """
        await self.send_email(email, subject, body)

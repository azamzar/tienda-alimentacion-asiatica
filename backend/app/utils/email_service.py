"""
Email service for sending emails using SMTP.
Supports HTML templates and attachments.
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional, Dict, Any
from jinja2 import Template

from app.config.settings import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending emails with templates"""

    def __init__(self):
        self.smtp_host = settings.EMAIL_HOST
        self.smtp_port = settings.EMAIL_PORT
        self.username = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD
        self.from_email = settings.EMAIL_FROM
        self.from_name = settings.EMAIL_FROM_NAME
        self.use_tls = settings.EMAIL_USE_TLS
        self.use_ssl = settings.EMAIL_USE_SSL
        self.enabled = settings.EMAIL_ENABLED

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        plain_content: Optional[str] = None,
        attachments: Optional[List[Path]] = None,
    ) -> bool:
        """
        Send an email with HTML content.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML content of the email
            plain_content: Plain text fallback (optional)
            attachments: List of file paths to attach (optional)

        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning("Email service is disabled. Skipping email send.")
            return False

        if not self.username or not self.password:
            logger.error("Email credentials not configured. Cannot send email.")
            return False

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{self.from_name} <{self.from_email}>"
            msg["To"] = to_email

            # Add plain text version (fallback)
            if plain_content:
                part1 = MIMEText(plain_content, "plain")
                msg.attach(part1)

            # Add HTML version
            part2 = MIMEText(html_content, "html")
            msg.attach(part2)

            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    if file_path.exists():
                        with open(file_path, "rb") as f:
                            part = MIMEBase("application", "octet-stream")
                            part.set_payload(f.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                "Content-Disposition",
                                f"attachment; filename={file_path.name}",
                            )
                            msg.attach(part)

            # Send email
            if self.use_ssl:
                with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                    server.login(self.username, self.password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                    if self.use_tls:
                        server.starttls()
                    server.login(self.username, self.password)
                    server.send_message(msg)

            logger.info(f"Email sent successfully to {to_email}")
            return True

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed. Check email credentials.")
            return False
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False

    def send_template_email(
        self,
        to_email: str,
        subject: str,
        template_name: str,
        context: Dict[str, Any],
    ) -> bool:
        """
        Send an email using a template.

        Args:
            to_email: Recipient email address
            subject: Email subject
            template_name: Name of the template file (without .html extension)
            context: Dictionary with template variables

        Returns:
            True if email was sent successfully, False otherwise
        """
        try:
            # Load template
            template_path = Path(__file__).parent.parent / "templates" / "emails" / f"{template_name}.html"

            if not template_path.exists():
                logger.error(f"Email template not found: {template_path}")
                return False

            with open(template_path, "r", encoding="utf-8") as f:
                template_content = f.read()

            # Render template with context
            template = Template(template_content)
            html_content = template.render(**context)

            # Send email
            return self.send_email(to_email, subject, html_content)

        except Exception as e:
            logger.error(f"Failed to send template email: {str(e)}")
            return False

    def send_password_reset_email(
        self,
        to_email: str,
        reset_token: str,
        user_name: Optional[str] = None,
    ) -> bool:
        """
        Send password reset email with link.

        Args:
            to_email: Recipient email address
            reset_token: Password reset token
            user_name: User's name (optional)

        Returns:
            True if email was sent successfully, False otherwise
        """
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"

        context = {
            "user_name": user_name or "Usuario",
            "reset_link": reset_link,
            "expire_minutes": settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES,
            "app_name": settings.APP_NAME,
            "frontend_url": settings.FRONTEND_URL,
        }

        return self.send_template_email(
            to_email=to_email,
            subject="Recuperación de Contraseña",
            template_name="password_reset",
            context=context,
        )

    def send_order_confirmation_email(
        self,
        to_email: str,
        order_id: int,
        customer_name: str,
        order_total: float,
        order_items: List[Dict[str, Any]],
    ) -> bool:
        """
        Send order confirmation email.

        Args:
            to_email: Customer email address
            order_id: Order ID
            customer_name: Customer's name
            order_total: Total order amount
            order_items: List of order items

        Returns:
            True if email was sent successfully, False otherwise
        """
        context = {
            "customer_name": customer_name,
            "order_id": order_id,
            "order_total": order_total,
            "order_items": order_items,
            "app_name": settings.APP_NAME,
            "frontend_url": settings.FRONTEND_URL,
        }

        return self.send_template_email(
            to_email=to_email,
            subject=f"Confirmación de Pedido #{order_id}",
            template_name="order_confirmation",
            context=context,
        )

    def send_order_status_update_email(
        self,
        to_email: str,
        order_id: int,
        customer_name: str,
        new_status: str,
        status_label: str,
    ) -> bool:
        """
        Send order status update email.

        Args:
            to_email: Customer email address
            order_id: Order ID
            customer_name: Customer's name
            new_status: New order status code
            status_label: Human-readable status label

        Returns:
            True if email was sent successfully, False otherwise
        """
        context = {
            "customer_name": customer_name,
            "order_id": order_id,
            "new_status": new_status,
            "status_label": status_label,
            "app_name": settings.APP_NAME,
            "frontend_url": settings.FRONTEND_URL,
        }

        return self.send_template_email(
            to_email=to_email,
            subject=f"Actualización de Pedido #{order_id}",
            template_name="order_status_update",
            context=context,
        )

    def send_welcome_email(
        self,
        to_email: str,
        user_name: str,
    ) -> bool:
        """
        Send welcome email to new users.

        Args:
            to_email: User email address
            user_name: User's name

        Returns:
            True if email was sent successfully, False otherwise
        """
        context = {
            "user_name": user_name,
            "app_name": settings.APP_NAME,
            "frontend_url": settings.FRONTEND_URL,
        }

        return self.send_template_email(
            to_email=to_email,
            subject=f"Bienvenido a {settings.APP_NAME}",
            template_name="welcome",
            context=context,
        )


# Global email service instance
email_service = EmailService()

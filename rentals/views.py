from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .models import Property, Inquiry, VisitorLog, EmailVerificationToken, LOCATION_CHOICES, PROPERTY_TYPE_CHOICES
from .forms import CustomUserRegistrationForm

import os
import json
import urllib.request
import urllib.error
import threading

def send_email_via_resend(to_email, subject, html_message, text_message=""):
    resend_api_key = getattr(settings, 'RESEND_API_KEY', '') or os.environ.get('RESEND_API_KEY', '')
    if not resend_api_key:
        print("Resend API delivery skipped: RESEND_API_KEY environment variable is missing.")
        return False, "RESEND_API_KEY not configured"
        
    from_email = getattr(settings, 'RESEND_FROM_EMAIL', 'onboarding@resend.dev')
    if 'onboarding@resend.dev' in from_email:
        from_email = 'onboarding@resend.dev'

    payload = {
        'from': from_email,
        'to': [to_email],
        'subject': subject,
        'html': html_message,
    }
    if text_message:
        payload['text'] = text_message
        
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request('https://api.resend.com/emails', data=data, headers={
            'Authorization': f'Bearer {resend_api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RentoraApp/1.0'
        })
        res = urllib.request.urlopen(req, timeout=8)
        resp_text = res.read().decode('utf-8')
        print(f"Email successfully delivered via Resend REST API! Response: {resp_text}")
        return True, "Email sent via Resend API"
    except urllib.error.HTTPError as http_err:
        err_body = http_err.read().decode('utf-8') if http_err.fp else str(http_err)
        print(f"Resend HTTP {http_err.code} Error: {err_body}")
        return False, f"Resend HTTP {http_err.code}: {err_body}"
    except Exception as e:
        print(f"Resend API delivery error: {e}")
        return False, str(e)

def send_email_via_brevo(to_email, subject, html_message, text_message=""):
    brevo_api_key = getattr(settings, 'BREVO_API_KEY', '') or os.environ.get('BREVO_API_KEY', '') or getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    if not brevo_api_key:
        return False, "BREVO_API_KEY not configured"
        
    sender_email = getattr(settings, 'EMAIL_HOST_USER', '') or os.environ.get('EMAIL_HOST_USER', '') or 'no-reply@rentora.com'
    if '@' not in sender_email:
        sender_email = 'no-reply@rentora.com'

    payload = {
        'sender': {'name': 'Rentora Luxury Concierge', 'email': sender_email},
        'to': [{'email': to_email}],
        'subject': subject,
        'htmlContent': html_message,
    }
    if text_message:
        payload['textContent'] = text_message
        
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request('https://api.brevo.com/v3/smtp/email', data=data, headers={
            'api-key': brevo_api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RentoraApp/1.0'
        })
        res = urllib.request.urlopen(req, timeout=8)
        resp_text = res.read().decode('utf-8')
        print(f"Email successfully delivered via Brevo REST API! Response: {resp_text}")
        return True, "Email sent via Brevo API"
    except urllib.error.HTTPError as http_err:
        err_body = http_err.read().decode('utf-8') if http_err.fp else str(http_err)
        print(f"Brevo HTTP {http_err.code} Error: {err_body}")
        return False, f"Brevo HTTP {http_err.code}: {err_body}"
    except Exception as e:
        print(f"Brevo API delivery error: {e}")
        return False, str(e)

def sync_brevo_contact(user, is_verified=False):
    brevo_api_key = getattr(settings, 'BREVO_API_KEY', '') or os.environ.get('BREVO_API_KEY', '') or getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    if not brevo_api_key or not getattr(user, 'email', None):
        return False
        
    payload = {
        'email': user.email,
        'attributes': {
            'FIRSTNAME': user.username,
            'VERIFIED': 'YES' if is_verified else 'PENDING'
        },
        'updateEnabled': True
    }
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request('https://api.brevo.com/v3/contacts', data=data, headers={
            'api-key': brevo_api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) RentoraApp/1.0'
        })
        res = urllib.request.urlopen(req, timeout=5)
        print(f"Brevo contact synced for {user.email} (Verified: {is_verified})")
        return True
    except Exception as e:
        print(f"Brevo Contact Sync Note: {e}")
        return False

def _async_send_mail_worker(to_email, subject, message, from_email, html_message):
    # 1. Try Brevo REST API if Brevo Key or EMAIL_HOST is brevo
    brevo_key = getattr(settings, 'BREVO_API_KEY', '') or os.environ.get('BREVO_API_KEY', '') or getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    email_host = getattr(settings, 'EMAIL_HOST', '') or os.environ.get('EMAIL_HOST', '')
    if brevo_key and ('brevo' in email_host.lower() or 'xkeysib-' in brevo_key or 'xsmtpsib-' in brevo_key or len(brevo_key) > 30):
        success, msg = send_email_via_brevo(to_email, subject, html_message, message)
        if success:
            return

    # 2. Try Resend REST API if Resend Key is present
    resend_key = getattr(settings, 'RESEND_API_KEY', '') or os.environ.get('RESEND_API_KEY', '')
    if resend_key:
        success, msg = send_email_via_resend(to_email, subject, html_message, message)
        if success:
            return
        if 'harshaljith1@gmail.com' not in to_email.lower():
            print(f"Retrying Resend delivery to authorized test recipient harshaljith1@gmail.com (Original target: {to_email})")
            send_email_via_resend('harshaljith1@gmail.com', f"[Fwd to {to_email}] {subject}", html_message, message)
            return

    # 3. Fallback to standard SMTP
    email_user = getattr(settings, 'EMAIL_HOST_USER', '')
    email_pass = getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    if email_user and email_pass:
        try:
            import socket
            socket.setdefaulttimeout(4.0)
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=[to_email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            print(f"SMTP delivery error: {e}")

def send_welcome_email(request, user):
    domain_url = "https://rentora-7gdf.onrender.com"
    explore_url = f"{domain_url}/properties/"
    user_name = user.first_name if user.first_name else user.username
    
    subject = "Welcome to Rentora"
    
    message = f"""Dear {user_name},

Thank you for creating an account with Rentora.

Your account is active. You can now explore our curated collection of private luxury estates across Kerala and manage your reservation requests.

Explore Properties:
{explore_url}

Best regards,
Rentora Team
Fort Kochi, Kerala, India
{domain_url}
"""

    html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #334155; margin: 0; padding: 40px 16px; -webkit-font-smoothing: antialiased;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center">
                <div style="max-width: 540px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 40px 36px; text-align: left;">
                    
                    <!-- Header Logo -->
                    <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 20px; margin-bottom: 24px;">
                        <div style="font-size: 18px; font-weight: 700; color: #0f172a; letter-spacing: 2.5px; text-transform: uppercase;">RENTORA</div>
                        <div style="font-size: 11px; color: #64748b; letter-spacing: 1px; margin-top: 2px; text-transform: uppercase;">Luxury Estates • Kerala</div>
                    </div>

                    <!-- Main Heading -->
                    <h1 style="font-size: 20px; font-weight: 600; color: #0f172a; margin: 0 0 16px 0; line-height: 1.3;">Welcome to Rentora</h1>

                    <p style="font-size: 14px; line-height: 1.6; color: #334155; margin: 0 0 20px 0;">
                        Dear <strong>{user_name}</strong>,<br><br>
                        Thank you for registering with Rentora. Your account is now active, giving you direct access to explore our portfolio of private backwater estates and luxury hillside retreats.
                    </p>

                    <!-- Features Box -->
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 18px 20px; margin-bottom: 24px;">
                        <div style="font-size: 13px; font-weight: 600; color: #0f172a; margin-bottom: 10px;">What you can do with your account:</div>
                        <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: #475569; line-height: 1.6;">
                            <li style="margin-bottom: 6px;">Browse verified luxury villas & private island estates</li>
                            <li style="margin-bottom: 6px;">Submit booking inquiries with custom stay requests</li>
                            <li style="margin-bottom: 0;">Track inquiry status & manage your profile from your dashboard</li>
                        </ul>
                    </div>

                    <!-- Action Button -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 28px;">
                        <tr>
                            <td align="center">
                                <a href="{explore_url}" target="_blank" style="display: inline-block; background-color: #0f172a; color: #ffffff !important; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 13px; font-weight: 600; letter-spacing: 0.5px;">Explore Properties</a>
                            </td>
                        </tr>
                    </table>

                    <!-- Footer -->
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center;">
                        <p style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin: 0;">
                            Rentora Luxury Rentals • Fort Kochi, Kerala, India<br>
                            Need help? Contact <a href="mailto:support@rentorakerala.com" style="color: #475569; text-decoration: underline;">support@rentorakerala.com</a>
                        </p>
                    </div>

                </div>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    from_email = getattr(settings, 'RESEND_FROM_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'Rentora <onboarding@resend.dev>'))

    t = threading.Thread(
        target=_async_send_mail_worker,
        args=(user.email, subject, message, from_email, html_message),
        daemon=False
    )
    t.start()
    t.join(timeout=3.0)

def send_verification_email(request, user, token_obj):
    if request:
        try:
            verify_url = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': token_obj.token})
            )
        except Exception:
            verify_url = f"https://rentora-7gdf.onrender.com/verify-email/{token_obj.token}/"
    else:
        verify_url = f"https://rentora-7gdf.onrender.com/verify-email/{token_obj.token}/"
    
    user_name = user.first_name if user.first_name else user.username
    subject = "Verify Your Email Address — Rentora"
    
    message = f"""Dear {user_name},

Thank you for registering with Rentora.

Please verify your email address by clicking the link below:
{verify_url}

If you did not create an account with Rentora, please ignore this email.

Best regards,
Rentora Team
https://rentora-7gdf.onrender.com
"""

    html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #334155; margin: 0; padding: 40px 16px; -webkit-font-smoothing: antialiased;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center">
                <div style="max-width: 540px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 40px 36px; text-align: left;">
                    
                    <!-- Header Logo -->
                    <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 20px; margin-bottom: 24px;">
                        <div style="font-size: 18px; font-weight: 700; color: #0f172a; letter-spacing: 2.5px; text-transform: uppercase;">RENTORA</div>
                        <div style="font-size: 11px; color: #64748b; letter-spacing: 1px; margin-top: 2px; text-transform: uppercase;">Account Security</div>
                    </div>

                    <!-- Main Heading -->
                    <h1 style="font-size: 20px; font-weight: 600; color: #0f172a; margin: 0 0 16px 0; line-height: 1.3;">Verify Your Email Address</h1>

                    <p style="font-size: 14px; line-height: 1.6; color: #334155; margin: 0 0 24px 0;">
                        Dear <strong>{user_name}</strong>,<br><br>
                        Please click the button below to verify your email address and activate your Rentora account:
                    </p>

                    <!-- Action Button -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 24px;">
                        <tr>
                            <td align="center">
                                <a href="{verify_url}" target="_blank" style="display: inline-block; background-color: #0f172a; color: #ffffff !important; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 13px; font-weight: 600; letter-spacing: 0.5px;">Verify Email Address</a>
                            </td>
                        </tr>
                    </table>

                    <!-- Direct Link Box -->
                    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 14px 16px; margin-bottom: 24px; word-break: break-all;">
                        <p style="font-size: 12px; color: #64748b; margin: 0 0 6px 0; line-height: 1.4;">If the button doesn't work, copy and paste this link into your browser:</p>
                        <a href="{verify_url}" target="_blank" style="font-size: 12px; color: #0284c7; text-decoration: underline;">{verify_url}</a>
                    </div>

                    <!-- Footer -->
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center;">
                        <p style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin: 0;">
                            If you did not request this email, no further action is required.<br>
                            Rentora Luxury Rentals • Fort Kochi, Kerala, India
                        </p>
                    </div>

                </div>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    from_email = getattr(settings, 'RESEND_FROM_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@rentora.com'))

    t = threading.Thread(
        target=_async_send_mail_worker,
        args=(user.email, subject, message, from_email, html_message),
        daemon=False
    )
    t.start()
    t.join(timeout=3.0)

def send_booking_inquiry_email(request, inquiry):
    domain_url = "https://rentora-7gdf.onrender.com"
    property_title = inquiry.property.title if inquiry.property else "Kerala Private Estate"
    property_location = inquiry.property.location_display_name if inquiry.property else "Kerala"
    
    subject = f"Booking Inquiry Received — {property_title}"
    
    if hasattr(inquiry.check_in, 'strftime'):
        check_in_str = inquiry.check_in.strftime('%B %d, %Y')
    elif inquiry.check_in:
        check_in_str = str(inquiry.check_in)
    else:
        check_in_str = "To be confirmed"

    if hasattr(inquiry.check_out, 'strftime'):
        check_out_str = inquiry.check_out.strftime('%B %d, %Y')
    elif inquiry.check_out:
        check_out_str = str(inquiry.check_out)
    else:
        check_out_str = "To be confirmed"
    
    message = f"""Dear {inquiry.name},

Thank you for your booking inquiry with Rentora.

We have received your inquiry for {property_title} ({property_location}).

Inquiry Details:
• Property: {property_title} ({property_location})
• Guest Name: {inquiry.name}
• Contact Phone: {inquiry.phone}
• Check-In: {check_in_str}
• Check-Out: {check_out_str}
• Guests: {inquiry.guests}
• Special Requests: {inquiry.message if inquiry.message else 'None'}

Our reservations team will review property availability and contact you shortly to confirm your booking.

Best regards,
Rentora Reservations Desk
Fort Kochi, Kerala, India
{domain_url}
"""

    html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #334155; margin: 0; padding: 40px 16px; -webkit-font-smoothing: antialiased;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0">
        <tr>
            <td align="center">
                <div style="max-width: 540px; margin: 0 auto; background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 40px 36px; text-align: left;">
                    
                    <!-- Header Logo -->
                    <div style="border-bottom: 1px solid #f1f5f9; padding-bottom: 20px; margin-bottom: 24px;">
                        <div style="font-size: 18px; font-weight: 700; color: #0f172a; letter-spacing: 2.5px; text-transform: uppercase;">RENTORA</div>
                        <div style="font-size: 11px; color: #64748b; letter-spacing: 1px; margin-top: 2px; text-transform: uppercase;">Reservations Desk</div>
                    </div>

                    <!-- Main Heading -->
                    <h1 style="font-size: 20px; font-weight: 600; color: #0f172a; margin: 0 0 16px 0; line-height: 1.3;">Booking Inquiry Received</h1>

                    <p style="font-size: 14px; line-height: 1.6; color: #334155; margin: 0 0 24px 0;">
                        Dear <strong>{inquiry.name}</strong>,<br><br>
                        Thank you for contacting Rentora. We have received your booking inquiry for <strong>{property_title}</strong>. Our reservations desk is currently reviewing property availability for your requested dates.
                    </p>

                    <!-- Clean Specification Table -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; margin-bottom: 24px;">
                        <tr>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 12px; font-weight: 600; color: #64748b; width: 35%;">Property</td>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 13px; font-weight: 600; color: #0f172a; text-align: right;">{property_title}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 12px; font-weight: 600; color: #64748b;">Location</td>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #0f172a; text-align: right;">{property_location}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 12px; font-weight: 600; color: #64748b;">Check-In</td>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #0f172a; text-align: right;">{check_in_str}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 12px; font-weight: 600; color: #64748b;">Check-Out</td>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #0f172a; text-align: right;">{check_out_str}</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 12px; font-weight: 600; color: #64748b;">Guests</td>
                            <td style="padding: 12px 16px; border-bottom: 1px solid #e2e8f0; font-size: 13px; color: #0f172a; text-align: right;">{inquiry.guests} Guest(s)</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 16px; font-size: 12px; font-weight: 600; color: #64748b;">Status</td>
                            <td style="padding: 12px 16px; font-size: 13px; font-weight: 600; color: #0284c7; text-align: right;">Under Review</td>
                        </tr>
                    </table>

                    <p style="font-size: 14px; line-height: 1.6; color: #334155; margin: 0 0 24px 0;">
                        Our host team will contact you shortly to confirm stay details and answer any questions you may have.
                    </p>

                    <!-- Action Button -->
                    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom: 28px;">
                        <tr>
                            <td align="center">
                                <a href="{domain_url}/dashboard/" target="_blank" style="display: inline-block; background-color: #0f172a; color: #ffffff !important; text-decoration: none; padding: 12px 28px; border-radius: 6px; font-size: 13px; font-weight: 600; letter-spacing: 0.5px;">View Dashboard</a>
                            </td>
                        </tr>
                    </table>

                    <!-- Footer -->
                    <div style="border-top: 1px solid #e2e8f0; padding-top: 20px; text-align: center;">
                        <p style="font-size: 12px; color: #94a3b8; line-height: 1.5; margin: 0;">
                            Rentora Luxury Rentals • Fort Kochi, Kerala, India<br>
                            If you have immediate questions, reply directly to this email.
                        </p>
                    </div>

                </div>
            </td>
        </tr>
    </table>
</body>
</html>
"""

    from_email = getattr(settings, 'RESEND_FROM_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@rentora.com'))

    t = threading.Thread(
        target=_async_send_mail_worker,
        args=(inquiry.email, subject, message, from_email, html_message),
        daemon=False
    )
    t.start()
    t.join(timeout=3.0)

    return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_visitor(request, property_obj=None):
    try:
        ip = get_client_ip(request)
        ua = request.META.get('HTTP_USER_AGENT', '')
        VisitorLog.objects.create(
            ip_address=ip,
            page_url=request.path,
            property=property_obj,
            user_agent=ua[:500]
        )
    except Exception:
        pass

def home_view(request):
    log_visitor(request)
    featured_properties = Property.objects.filter(is_featured=True)[:6]
    if not featured_properties.exists():
        featured_properties = Property.objects.all()[:6]

    locations = LOCATION_CHOICES
    property_types = PROPERTY_TYPE_CHOICES

    # Handle Hero Form Submissions (Register or Login or Quick Search)
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'register':
            try:
                form = CustomUserRegistrationForm(request.POST)
                if form.is_valid():
                    user = form.save(commit=False)
                    user.is_active = False
                    user.save()
                    
                    try:
                        token_obj, _ = EmailVerificationToken.objects.get_or_create(user=user)
                        send_verification_email(request, user, token_obj)
                        sync_brevo_contact(user, is_verified=False)
                    except Exception as email_err:
                        print(f"Non-fatal email/token notification error: {email_err}")
                    
                    request.session['pending_email'] = user.email
                    return redirect('verification_pending')
                else:
                    for errors in form.errors.values():
                        for error in errors:
                            messages.error(request, error)
            except Exception as reg_err:
                print(f"Registration error caught safely: {reg_err}")
                messages.error(request, "An unexpected error occurred while creating your account. Please try again or contact concierge support.")
                    
        elif action == 'login':
            username_input = request.POST.get('username', '').strip()
            password_input = request.POST.get('password', '')
            
            user = authenticate(request, username=username_input, password=password_input)
            if user is None and '@' in username_input:
                try:
                    user_obj = User.objects.filter(email__iexact=username_input).first()
                    if user_obj:
                        user = authenticate(request, username=user_obj.username, password=password_input)
                except Exception:
                    user = None

            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password. Please try again.")

        elif action == 'inquiry':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            guests = request.POST.get('guests', 2)
            
            Inquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                guests=guests,
                message=message,
                ip_address=get_client_ip(request)
            )
            messages.success(request, "Thank you! Our concierge team will contact you within 2 hours with curated options.")
            return redirect('home')

    context = {
        'featured_properties': featured_properties,
        'locations': locations,
        'property_types': property_types,
        'total_properties': Property.objects.count(),
    }
    return render(request, 'rentals/index.html', context)

def dashboard_view(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please sign in to access your member dashboard.")
        return redirect('login')

    log_visitor(request)
    
    # Retrieve user's inquiries/bookings
    user_inquiries = Inquiry.objects.filter(
        Q(email__iexact=request.user.email) | Q(name__icontains=request.user.username)
    ).distinct()

    if not user_inquiries.exists():
        user_inquiries = Inquiry.objects.all()[:5]

    # Property Search & Filter
    properties = Property.objects.all()
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    property_type = request.GET.get('property_type', '')
    max_price = request.GET.get('max_price', '')
    guests = request.GET.get('guests', '')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_display_name__icontains=query)
        )

    if location:
        properties = properties.filter(location=location)

    if property_type:
        properties = properties.filter(property_type=property_type)

    if max_price and max_price.isdigit():
        properties = properties.filter(price_per_night__lte=int(max_price))

    if guests and guests.isdigit():
        properties = properties.filter(max_guests__gte=int(guests))

    # Featured Properties (Compact Display)
    featured_properties = properties.filter(is_featured=True)[:4]
    if not featured_properties.exists():
        featured_properties = properties[:4]

    context = {
        'user_inquiries': user_inquiries,
        'featured_properties': featured_properties,
        'properties': properties,
        'locations': LOCATION_CHOICES,
        'property_types': PROPERTY_TYPE_CHOICES,
        'selected_location': location,
        'selected_type': property_type,
        'query': query,
        'max_price': max_price,
        'guests': guests,
    }
    return render(request, 'rentals/dashboard.html', context)

def properties_view(request):
    log_visitor(request)
    properties = Property.objects.all()

    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    property_type = request.GET.get('property_type', '')
    max_price = request.GET.get('max_price', '')
    guests = request.GET.get('guests', '')

    if query:
        properties = properties.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_display_name__icontains=query)
        )

    if location:
        properties = properties.filter(location=location)

    if property_type:
        properties = properties.filter(property_type=property_type)

    if max_price and max_price.isdigit():
        properties = properties.filter(price_per_night__lte=int(max_price))

    if guests and guests.isdigit():
        properties = properties.filter(max_guests__gte=int(guests))

    context = {
        'properties': properties,
        'locations': LOCATION_CHOICES,
        'property_types': PROPERTY_TYPE_CHOICES,
        'selected_location': location,
        'selected_type': property_type,
        'query': query,
        'max_price': max_price,
        'guests': guests,
    }
    return render(request, 'rentals/properties.html', context)

def property_detail_view(request, slug):
    property_obj = get_object_or_404(Property, slug=slug)
    log_visitor(request, property_obj=property_obj)
    similar_properties = Property.objects.filter(location=property_obj.location).exclude(id=property_obj.id)[:3]
    
    if not similar_properties.exists():
        similar_properties = Property.objects.exclude(id=property_obj.id)[:3]

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        check_in = request.POST.get('check_in') or None
        check_out = request.POST.get('check_out') or None
        guests = request.POST.get('guests', 2)
        message = request.POST.get('message', '')

        inquiry_obj = Inquiry.objects.create(
            property=property_obj,
            name=name,
            email=email,
            phone=phone,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            message=message,
            ip_address=get_client_ip(request)
        )

        try:
            send_booking_inquiry_email(request, inquiry_obj)
        except Exception as email_err:
            print(f"Non-fatal booking inquiry email notification error: {email_err}")

        messages.success(request, f"Your booking inquiry for '{property_obj.title}' has been submitted! A confirmation email has been sent to {email}.")
        return redirect('property_detail', slug=property_obj.slug)

    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
    }
    return render(request, 'rentals/property_detail.html', context)

def register_view(request):
    log_visitor(request)
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            form = CustomUserRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                try:
                    token_obj, _ = EmailVerificationToken.objects.get_or_create(user=user)
                    send_verification_email(request, user, token_obj)
                    sync_brevo_contact(user, is_verified=False)
                except Exception as email_err:
                    print(f"Non-fatal email/token notification error: {email_err}")

                request.session['pending_email'] = user.email
                return redirect('verification_pending')
            else:
                for errors in form.errors.values():
                    for error in errors:
                        messages.error(request, error)
        except Exception as reg_err:
            print(f"Registration error in register_view: {reg_err}")
            messages.error(request, "An unexpected error occurred while creating your account. Please try again or contact concierge support.")
            form = CustomUserRegistrationForm(request.POST)
    else:
        form = CustomUserRegistrationForm()

    return render(request, 'rentals/register.html', {'form': form})

def verification_pending_view(request):
    log_visitor(request)
    pending_email = request.session.get('pending_email', '')
    return render(request, 'rentals/verification_pending.html', {'pending_email': pending_email})

def login_view(request):
    log_visitor(request)
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username_input = request.POST.get('username', '').strip()
        password_input = request.POST.get('password', '').strip()

        user_obj = User.objects.filter(Q(username__iexact=username_input) | Q(email__iexact=username_input)).first()
        if user_obj and user_obj.check_password(password_input):
            if not user_obj.is_active:
                messages.warning(
                    request, 
                    f"Your account ({user_obj.email}) has not been verified yet. Please check your inbox for the activation link or click below to resend."
                )
                request.session['pending_email'] = user_obj.email
                return redirect('verification_pending')

            login(request, user_obj)
            messages.success(request, f"Welcome back, {user_obj.username}!")
            return redirect('dashboard')

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_active:
                messages.warning(
                    request, 
                    f"Your account ({user.email}) has not been verified yet. Please check your inbox for the activation link."
                )
                request.session['pending_email'] = user.email
                return redirect('verification_pending')

            login(request, user)
            messages.success(request, f"Logged in as {user.username}.")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'rentals/login.html', {'form': form})

def verify_email_view(request, token):
    log_visitor(request)
    token_obj = EmailVerificationToken.objects.filter(token=token).first()
    
    if not token_obj:
        messages.error(request, "Invalid or expired email verification link.")
        return redirect('login')

    user = token_obj.user
    if user.is_active or token_obj.is_verified:
        user.is_active = True
        user.save()
        token_obj.is_verified = True
        token_obj.save()
        login(request, user)
        messages.info(request, f"Welcome back to your VIP Dashboard, {user.username}.")
        return redirect('dashboard')

    user.is_active = True
    user.save()

    token_obj.is_verified = True
    token_obj.save()

    try:
        sync_brevo_contact(user, is_verified=True)
        send_welcome_email(request, user)
    except Exception as e:
        print(f"Post verification error: {e}")

    login(request, user)
    messages.success(request, f"Email verified successfully! Welcome to your Rentora VIP Dashboard, {user.username}.")
    return redirect('dashboard')

def resend_verification_view(request):
    log_visitor(request)
    if request.method == 'POST':
        email_or_username = request.POST.get('email_or_username', '').strip()
        user = User.objects.filter(Q(email__iexact=email_or_username) | Q(username__iexact=email_or_username)).first()

        if user:
            token_obj, _ = EmailVerificationToken.objects.get_or_create(user=user)
            send_welcome_email(request, user)
            send_verification_email(request, user, token_obj)
            messages.success(request, f"VIP Welcome and Verification emails have been dispatched to {user.email}.")
            return redirect('login')
        else:
            messages.error(request, "No account found matching that email address or username.")

    return render(request, 'rentals/resend_verification.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

def custom_404_view(request, exception=None):
    return render(request, 'rentals/404.html', status=404)


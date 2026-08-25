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

def _async_send_mail_worker(to_email, subject, message, from_email, html_message):
    # 1. Try Brevo REST API if Brevo Key is present
    brevo_key = getattr(settings, 'BREVO_API_KEY', '') or os.environ.get('BREVO_API_KEY', '') or getattr(settings, 'EMAIL_HOST_PASSWORD', '')
    if brevo_key and ('xkeysib-' in brevo_key or 'xsmtpsib-' in brevo_key):
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
    
    subject = "Welcome to Rentora — Your VIP Membership is Active ✦"
    
    message = f"""Dear {user.username},

Welcome to Rentora — Kerala's Sanctuary of Bespoke Private Estates.

Your VIP member account has been successfully created and activated. You now have exclusive access to our private estate collection, presidential backwater yacht charters, and 24/7 dedicated personal hosts across Kerala.

Explore Private Collection:
{explore_url}

Warm regards,
Rentora Private Concierge Team
{domain_url}
"""

    html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0C0C0C; color: #D7E2EA; margin: 0; padding: 40px 20px; }}
        .email-card {{ max-width: 600px; margin: 0 auto; background: #141414; border: 1px solid #D4AF37; border-radius: 24px; padding: 44px 36px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.85); }}
        .brand-title {{ font-size: 28px; font-weight: 800; color: #E8CE92; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 6px; font-family: Georgia, serif; }}
        .brand-sub {{ font-size: 11px; color: #D4AF37; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 32px; font-weight: 700; }}
        .welcome-badge {{ display: inline-block; background: rgba(212,175,55,0.15); border: 1px solid #D4AF37; color: #F5D77F; font-size: 12px; font-weight: 800; letter-spacing: 2px; padding: 6px 18px; border-radius: 30px; text-transform: uppercase; margin-bottom: 24px; }}
        .content-text {{ font-size: 15px; line-height: 1.7; color: #D8D0C5; margin-bottom: 28px; text-align: left; }}
        .privilege-box {{ background: #0C0C0C; border: 1px solid rgba(212,175,55,0.25); border-radius: 16px; padding: 20px; text-align: left; margin-bottom: 32px; }}
        .privilege-item {{ font-size: 14px; color: #FFFFFF; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }}
        .privilege-item:last-child {{ margin-bottom: 0; }}
        .btn-gold-cta {{ display: inline-block; background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%); color: #0C0C0C; text-decoration: none; padding: 16px 40px; border-radius: 50px; font-weight: 800; font-size: 13px; letter-spacing: 2px; text-transform: uppercase; box-shadow: 0 10px 30px rgba(212, 175, 55, 0.4); margin-bottom: 28px; }}
        .footer-text {{ font-size: 12px; color: #788895; margin-top: 24px; line-height: 1.5; }}
    </style>
</head>
<body>
    <div class="email-card">
        <div class="brand-title">RENTORA</div>
        <div class="brand-sub">SANCTUARY OF BESPOKE PRIVATE ESTATES</div>
        
        <div class="welcome-badge">✦ VIP MEMBERSHIP CONFIRMED</div>

        <p class="content-text">
            Dear <strong>{user.username}</strong>,<br><br>
            Welcome to Rentora. Your VIP member account is officially active. You now hold direct access to Kerala’s finest unlisted private cliffside estates, tea plantation manors, and presidential backwater yachts.
        </p>

        <div class="privilege-box">
            <div class="privilege-item">👑 <strong>Unlisted Private Estates:</strong> 100% verified cliffside villas & tea manors.</div>
            <div class="privilege-item">👨‍🍳 <strong>In-Villa Master Chefs:</strong> Bespoke sea-to-table & Ayurvedic gastronomy.</div>
            <div class="privilege-item">🚁 <strong>VIP Logistics:</strong> Private helipads & 24/7 personal estate concierge.</div>
        </div>

        <a href="{explore_url}" class="btn-gold-cta" target="_blank">EXPLORE PRIVATE COLLECTION</a>

        <div class="footer-text">
            Rentora Luxury Hospitality Group • Kerala, India<br>
            Need assistance? Reply directly to this email or contact your 24/7 personal host.
        </div>
    </div>
</body>
</html>
"""

    from_email = getattr(settings, 'RESEND_FROM_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'Rentora Luxury Concierge <onboarding@resend.dev>'))

    t = threading.Thread(
        target=_async_send_mail_worker,
        args=(user.email, subject, message, from_email, html_message),
        daemon=True
    )
    t.start()

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
    
    subject = "Verify Your VIP Email — Rentora Luxury Hospitality"
    
    message = f"""Dear {user.username},

Thank you for registering your VIP account with Rentora — Kerala's Sanctuary of Bespoke Private Estates.

Please verify your email address by clicking the link below to activate your exclusive membership:
{verify_url}

If you did not create a Rentora account, please ignore this email.

Warm regards,
Rentora Private Concierge Team
https://rentora-7gdf.onrender.com
"""

    html_message = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0C0C0C; color: #D7E2EA; margin: 0; padding: 40px 20px; }}
        .email-card {{ max-width: 580px; margin: 0 auto; background: #141414; border: 1px solid #D4AF37; border-radius: 20px; padding: 40px; text-align: center; box-shadow: 0 15px 40px rgba(0,0,0,0.8); }}
        .brand-title {{ font-size: 28px; font-weight: 800; color: #E8CE92; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 8px; }}
        .brand-sub {{ font-size: 13px; color: #D4AF37; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 30px; }}
        .content-text {{ font-size: 16px; line-height: 1.6; color: #D8D0C5; margin-bottom: 30px; }}
        .btn-verify {{ display: inline-block; background: linear-gradient(135deg, #D4AF37 0%, #AA7C11 100%); color: #0C0C0C; text-decoration: none; padding: 14px 36px; border-radius: 50px; font-weight: 700; font-size: 14px; letter-spacing: 2px; text-transform: uppercase; box-shadow: 0 8px 25px rgba(212, 175, 55, 0.35); margin-bottom: 30px; }}
        .url-text {{ font-size: 12px; color: #8898A5; word-break: break-all; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="email-card">
        <div class="brand-title">RENTORA</div>
        <div class="brand-sub">Sanctuary of Bespoke Private Estates</div>
        
        <p class="content-text">
            Dear <strong>{user.username}</strong>,<br><br>
            Thank you for creating your VIP membership account with Rentora. Please click the button below to verify your email address and unlock access to private estate collections, in-villa culinary dining, and 24/7 concierge services.
        </p>

        <a href="{verify_url}" class="btn-verify" target="_blank">VERIFY EMAIL ADDRESS</a>

        <p class="content-text" style="font-size: 13px; color: #A0B0BC;">
            Or copy and paste this verification URL into your browser:
        </p>
        <p class="url-text"><a href="{verify_url}" style="color: #D4AF37;">{verify_url}</a></p>
    </div>
</body>
</html>
"""

    from_email = getattr(settings, 'RESEND_FROM_EMAIL', getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@rentora.com'))

    # Dispatch email in detached daemon thread
    t = threading.Thread(
        target=_async_send_mail_worker,
        args=(user.email, subject, message, from_email, html_message),
        daemon=True
    )
    t.start()

    return verify_url

    return verify_url


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
                    user.is_active = True
                    user.save()
                    
                    try:
                        token_obj, _ = EmailVerificationToken.objects.get_or_create(user=user)
                        send_welcome_email(request, user)
                        send_verification_email(request, user, token_obj)
                    except Exception as email_err:
                        print(f"Non-fatal email/token notification error: {email_err}")
                    
                    login(request, user)
                    messages.success(
                        request, 
                        f"Welcome to Rentora, {user.username}! Your VIP account has been successfully created and activated."
                    )
                    return redirect('dashboard')
                else:
                    for errors in form.errors.values():
                        for error in errors:
                            messages.error(request, error)
            except Exception as reg_err:
                print(f"Registration error caught safely: {reg_err}")
                messages.error(request, "An unexpected error occurred while creating your account. Please try again or contact concierge support.")
                    
        elif action == 'login':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
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

        Inquiry.objects.create(
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
        messages.success(request, f"Your booking inquiry for '{property_obj.title}' has been submitted! Our concierge will get back to you shortly.")
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
                user.is_active = True
                user.save()

                try:
                    token_obj, _ = EmailVerificationToken.objects.get_or_create(user=user)
                    send_welcome_email(request, user)
                    send_verification_email(request, user, token_obj)
                except Exception as email_err:
                    print(f"Non-fatal email/token notification error: {email_err}")

                login(request, user)
                messages.success(
                    request, 
                    f"Welcome to Rentora, {user.username}! Your VIP account has been successfully created and activated."
                )
                return redirect('dashboard')
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

def login_view(request):
    log_visitor(request)
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username_input = request.POST.get('username', '').strip()
        password_input = request.POST.get('password', '').strip()

        # Auto-activate user account if user exists and password matches
        user_obj = User.objects.filter(Q(username__iexact=username_input) | Q(email__iexact=username_input)).first()
        if user_obj and not user_obj.is_active and user_obj.check_password(password_input):
            user_obj.is_active = True
            user_obj.save()
            login(request, user_obj)
            messages.success(request, f"Welcome to Rentora, {user_obj.username}! Your account has been activated.")
            return redirect('dashboard')

        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
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
        messages.info(request, "Your email address is already verified. Please sign in.")
        return redirect('login')

    user.is_active = True
    user.save()

    token_obj.is_verified = True
    token_obj.save()

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


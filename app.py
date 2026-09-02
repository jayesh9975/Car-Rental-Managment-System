import os
from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'car_rental_jayesh_bhavsar_bulletproof_final_2026'

# --- Admin Credentials ---
ADMIN_USER = {
    "email": "jayeshbhavsar997@gmail.com",
    "password_hash": generate_password_hash("Shiv@99")
}

# --- Owner Info ---
OWNER_INFO = {
    "name": "Jayesh Harish Bhavsar",
    "company": "Car Rental Management System",
    "sub_title": "By Jayesh Bhavsar",
    "phone": "+919765432442",
    "phone_display": "+91 9765432442",
    "email": "jayeshbhavsar997@gmail.com",
    "address": "Gohil Nagar, Amalner, Maharashtra, India"
}

# --- Bank & Withdrawal Info Storage (Default) ---
ADMIN_BANK_INFO = {
    "account_name": "Jayesh Harish Bhavsar",
    "bank_name": "BANK OF BARODA",
    "account_number": "1228000012608",
    "ifsc_code": "BARB0AMALNE",
    "upi_id": "jayeshbhavsar@oksbi"
}

VID_SAMPLE = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"

# --- CAR MODELS DATABASE ---
CARS_DATA = [
    {"name": "Maruti WagonR", "price": 1500, "type": "Hatchback", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=800&q=80"},
    {"name": "Maruti Dzire", "price": 1650, "type": "Sedan", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80"},
    {"name": "Maruti Ertiga", "price": 1900, "type": "MUV / SUV", "seats": "7 Seater", "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80"},
    {"name": "Tata Punch", "price": 1550, "type": "Mini SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&q=80"},
    {"name": "Tata Nexon", "price": 1800, "type": "Compact SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80"},
    {"name": "Mahindra Scorpio", "price": 2400, "type": "SUV", "seats": "7 Seater", "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80"},
    {"name": "Maruti Eeco", "price": 1400, "type": "Van / Multi-utility", "seats": "7 Seater", "image": "https://images.unsplash.com/photo-1485291571150-772bcfc10da5?auto=format&fit=crop&w=800&q=80"},
    {"name": "Maruti Fronx", "price": 1700, "type": "Crossover SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80"},
    {"name": "Hyundai Venue", "price": 1750, "type": "Compact SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80"},
    {"name": "Toyota Innova", "price": 2800, "type": "Premium MUV", "seats": "7 Seater", "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80"},
    {"name": "Maruti Baleno", "price": 1600, "type": "Premium Hatchback", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=800&q=80"},
    {"name": "Mahindra Thar", "price": 2600, "type": "Off-road SUV", "seats": "4 Seater", "image": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=800&q=80"},
    {"name": "Mahindra XUV700", "price": 2700, "type": "Luxury SUV", "seats": "7 Seater", "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=800&q=80"},
    {"name": "Maruti Grand Vitara", "price": 2200, "type": "Hybrid SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1563720223185-11003d516935?auto=format&fit=crop&w=800&q=80"},
    {"name": "Mahindra XUV 3XO", "price": 1850, "type": "Compact SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=800&q=80"},
    {"name": "Mahindra Bolero", "price": 1700, "type": "Rugged SUV", "seats": "7 Seater", "image": "https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&q=80"},
    {"name": "Tata Tiago", "price": 1450, "type": "Hatchback", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=800&q=80"},
    {"name": "Tata Curvv", "price": 2300, "type": "Coupe SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80"},
    {"name": "Toyota Hyryder", "price": 2250, "type": "Hybrid SUV", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=800&q=80"},
    {"name": "Hyundai i10 Nios", "price": 1500, "type": "City Hatchback", "seats": "5 Seater", "image": "https://images.unsplash.com/photo-1580273916550-e323be2ae537?auto=format&fit=crop&w=800&q=80"}
]

CARS = []
for idx, item in enumerate(CARS_DATA, start=1):
    main_img = item["image"]
    photos = [main_img, main_img, main_img, main_img, main_img]
    videos = [VID_SAMPLE] * 5
    CARS.append({
        "id": idx,
        "name": item["name"],
        "type": item["type"],
        "seats": item["seats"],
        "price": item["price"],
        "available": True,
        "image": main_img,
        "photos": photos,
        "videos": videos
    })

USERS_DB = {}
BOOKINGS = []
BREAKDOWN_REQUESTS = []

LANDING_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JAY CARS - Car Rental Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Plus Jakarta Sans', sans-serif; scroll-behavior: smooth; }
        body { background-color: #0b0f19; color: #ffffff; overflow-x: hidden; }

        .bg-carousel { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -2; }
        .bg-slide { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-size: cover; background-position: center; opacity: 0; transition: opacity 1.5s ease-in-out; }
        .bg-slide.active { opacity: 1; }
        .bg-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(135deg, rgba(11, 15, 25, 0.94) 0%, rgba(15, 23, 42, 0.88) 100%); z-index: -1; }

        nav { display: flex; justify-content: space-between; align-items: center; padding: 18px 6%; background: rgba(11, 15, 25, 0.85); backdrop-filter: blur(12px); position: fixed; top: 0; left: 0; right: 0; z-index: 1000; border-bottom: 1px solid rgba(255,255,255,0.08); }
        
        /* Logo Styling with JAY'S CARS Badge */
        .logo-box { display: flex; align-items: center; gap: 14px; text-decoration: none; }
        .logo-icon-wrap { width: 45px; height: 45px; background: linear-gradient(135deg, #2563eb, #1d4ed8); border-radius: 12px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(37,99,235,0.4); }
        .logo-icon-wrap i { color: #ffffff; font-size: 1.3rem; }
        .logo-text h2 { font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: 0.5px; }
        .logo-text span { font-size: 0.72rem; color: #94a3b8; display: block; font-weight: 500; }

        .nav-links { display: flex; gap: 25px; align-items: center; }
        .nav-links a { color: #94a3b8; text-decoration: none; font-size: 0.9rem; font-weight: 600; transition: color 0.3s; }
        .nav-links a:hover { color: #ffffff; }
        .btn-primary-land { background: #2563eb; color: white; text-decoration: none; font-weight: 600; font-size: 0.9rem; padding: 10px 24px; border-radius: 8px; box-shadow: 0 4px 15px rgba(37,99,235,0.4); transition: all 0.3s; }
        .btn-primary-land:hover { background: #1d4ed8; transform: translateY(-2px); }

        .hero { min-height: 100vh; display: flex; align-items: center; justify-content: space-between; padding: 140px 6% 80px 6%; }
        .hero-left { max-width: 650px; }
        .badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(37,99,235,0.2); color: #60a5fa; padding: 6px 14px; border-radius: 30px; font-size: 0.85rem; font-weight: 700; margin-bottom: 25px; border: 1px solid rgba(37,99,235,0.4); }
        .hero-left h1 { font-size: 3.5rem; font-weight: 800; line-height: 1.15; margin-bottom: 20px; letter-spacing: -1px; }
        .hero-left h1 span { color: #3b82f6; }
        .hero-left p { font-size: 1.1rem; color: #cbd5e1; line-height: 1.7; margin-bottom: 35px; }
        .hero-btns { display: flex; gap: 15px; }
        .cta-main { background: #2563eb; color: white; padding: 16px 32px; border-radius: 10px; font-weight: 700; text-decoration: none; font-size: 1rem; display: inline-flex; align-items: center; gap: 10px; box-shadow: 0 10px 25px rgba(37,99,235,0.4); transition: all 0.3s; }
        .cta-main:hover { background: #1d4ed8; transform: translateY(-3px); }
        .cta-sec { background: rgba(255,255,255,0.08); color: white; padding: 16px 32px; border-radius: 10px; font-weight: 700; text-decoration: none; font-size: 1rem; border: 1px solid rgba(255,255,255,0.15); transition: all 0.3s; }
        .cta-sec:hover { background: rgba(255,255,255,0.15); }

        .hero-right { position: relative; }
        .floating-card { background: rgba(30, 41, 59, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.12); padding: 30px; border-radius: 20px; width: 420px; box-shadow: 0 25px 50px rgba(0,0,0,0.5); }
        .floating-card h3 { font-size: 1.25rem; font-weight: 700; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
        .stat-row { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px; }
        .stat-box { background: rgba(15, 23, 42, 0.7); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06); }
        .stat-box h4 { font-size: 1.5rem; font-weight: 800; color: #60a5fa; }
        .stat-box p { font-size: 0.8rem; color: #94a3b8; margin-top: 4px; }

        .features-section { padding: 80px 6%; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(10px); border-top: 1px solid rgba(255,255,255,0.08); }
        .section-title { text-align: center; max-width: 600px; margin: 0 auto 60px auto; }
        .section-title h2 { font-size: 2.3rem; font-weight: 800; margin-bottom: 15px; letter-spacing: -0.5px; }
        .section-title p { color: #94a3b8; font-size: 1rem; }
        
        .grid-features { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 30px; }
        .feature-card-land { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.08); padding: 35px 30px; border-radius: 16px; transition: transform 0.3s, border-color 0.3s; }
        .feature-card-land:hover { transform: translateY(-8px); border-color: rgba(37,99,235,0.6); background: rgba(30, 41, 59, 0.8); }
        .feature-card-land i { font-size: 2.2rem; color: #3b82f6; margin-bottom: 20px; background: rgba(59,130,246,0.15); padding: 16px; border-radius: 12px; }
        .feature-card-land h3 { font-size: 1.2rem; font-weight: 700; margin-bottom: 10px; }
        .feature-card-land p { font-size: 0.9rem; color: #94a3b8; line-height: 1.6; }

        .policy-section { padding: 80px 6%; background: rgba(11, 15, 25, 0.95); border-top: 1px solid rgba(255,255,255,0.08); }
        .policy-container { max-width: 900px; margin: 0 auto; background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255,255,255,0.1); padding: 50px; border-radius: 20px; backdrop-filter: blur(10px); }
        .policy-container h2 { font-size: 2rem; font-weight: 800; margin-bottom: 10px; color: #ffffff; }
        .policy-container .last-updated { font-size: 0.85rem; color: #60a5fa; margin-bottom: 30px; display: block; }
        .policy-container h3 { font-size: 1.15rem; font-weight: 700; margin: 25px 0 10px 0; color: #38bdf8; }
        .policy-container p { font-size: 0.95rem; color: #94a3b8; line-height: 1.7; margin-bottom: 15px; }
        .policy-container ul { margin-left: 20px; color: #94a3b8; margin-bottom: 15px; font-size: 0.95rem; line-height: 1.6; }
        .policy-container li { margin-bottom: 8px; }

        footer { padding: 40px 6%; text-align: center; background: #070a12; border-top: 1px solid rgba(255,255,255,0.05); color: #64748b; font-size: 0.88rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; }
        footer span { color: #ffffff; font-weight: 600; }
        .footer-links { display: flex; gap: 20px; }
        .footer-links a { color: #94a3b8; text-decoration: none; font-size: 0.85rem; transition: color 0.3s; }
        .footer-links a:hover { color: #ffffff; }
    </style>
</head>
<body>

    <div class="bg-carousel">
        <div class="bg-slide active" style="background-image: url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1920&q=80');"></div>
        <div class="bg-slide" style="background-image: url('https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1920&q=80');"></div>
        <div class="bg-slide" style="background-image: url('https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=1920&q=80');"></div>
        <div class="bg-slide" style="background-image: url('https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1920&q=80');"></div>
    </div>
    <div class="bg-overlay"></div>

    <nav>
        <a href="/" class="logo-box">
            <div class="logo-icon-wrap">
                <i class="fa-solid fa-car-side"></i>
            </div>
            <div class="logo-text">
                <h2>JAY'S CARS</h2>
                <span>Car Rental Management System</span>
            </div>
        </a>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="#privacy-policy">Privacy Policy</a>
            <a href="/home" class="btn-primary-land"><i class="fa-solid fa-compass"></i> Open App / Fleet</a>
        </div>
    </nav>

    <section class="hero">
        <div class="hero-left">
            <div class="badge"><i class="fa-solid fa-bolt"></i> Maharashtra's Premier Mobility Platform</div>
            <h1>Smart, Safe & Seamless <span>Car Rental Management System</span> on Demand</h1>
            <p>Experience ultra-modern travel with verified fleet vehicles, live GPS telemetry tracking, transparent daily pricing, and 24/7 dedicated roadside assistance managed by Jayesh Bhavsar.</p>
            <div class="hero-btns">
                <a href="/home" class="cta-main"><i class="fa-solid fa-compass"></i> Explore Fleet Now <i class="fa-solid fa-arrow-right"></i></a>
                <a href="/customer/register" class="cta-sec">Create Account</a>
            </div>
        </div>

        <div class="hero-right">
            <div class="floating-card">
                <h3><i class="fa-solid fa-shield-halved" style="color: #10b981;"></i> Trusted System Specs</h3>
                <div class="stat-row">
                    <div class="stat-box">
                        <h4>20+</h4>
                        <p>Verified Vehicles</p>
                    </div>
                    <div class="stat-box">
                        <h4>24/7</h4>
                        <p>SOS Support</p>
                    </div>
                </div>
                <div style="background: rgba(15,23,42,0.7); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);">
                    <div style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 6px;"><i class="fa-solid fa-location-dot" style="color: #ef4444;"></i> Operations Hub</div>
                    <div style="font-size: 0.9rem; font-weight: 600; color: white;">Gohil Nagar, Amalner, Maharashtra</div>
                </div>
            </div>
        </div>
    </section>

    <section id="features" class="features-section">
        <div class="section-title">
            <h2>Designed for Ultimate Reliability</h2>
            <p>Everything you need for a comfortable trip or secure business rental management.</p>
        </div>
        <div class="grid-features">
            <div class="feature-card-land">
                <i class="fa-solid fa-satellite-dish"></i>
                <h3>Live GPS Telemetry</h3>
                <p>Track your rented vehicles in real-time right from your customer dashboard with live map markers.</p>
            </div>
            <div class="feature-card-land">
                <i class="fa-solid fa-headset"></i>
                <h3>Instant Roadside SOS</h3>
                <p>Encountered a flat tyre or engine issue? Request emergency assistance with automated admin dispatch.</p>
            </div>
            <div class="feature-card-land">
                <i class="fa-solid fa-indian-rupee-sign"></i>
                <h3>Zero Hidden Fees</h3>
                <p>Crystal-clear rental rates per day with total cost previews and instant WhatsApp booking confirmation.</p>
            </div>
        </div>
    </section>

    <section id="privacy-policy" class="policy-section">
        <div class="policy-container">
            <h2>Privacy Policy & Terms of Service</h2>
            <span class="last-updated">Effective Date: January 1, 2026 | Managed by Jayesh Bhavsar</span>
            
            <p>Welcome to <strong>JAY'S CARS (Car Rental Management System)</strong>. We value your trust and are committed to protecting your personal information. This Privacy Policy outlines how we collect, use, and safeguard your data when you use our platform and rental services in Amalner and across Maharashtra.</p>

            <h3>1. Information We Collect</h3>
            <p>To provide seamless vehicle rentals and support, we may collect the following details:</p>
            <ul>
                <li><strong>Personal Identification Data:</strong> Full name, email address, phone number, and residential address.</li>
                <li><strong>Verification Documents:</strong> Valid Driving License details and government-approved identification for legal rental compliance.</li>
                <li><strong>Trip & Location Data:</strong> Pickup/drop-off locations, rental dates, and live GPS telemetry data during active bookings for safety and tracking.</li>
            </ul>

            <h3>2. How We Use Your Information</h3>
            <p>Your data is strictly utilized for core operational purposes, which include:</p>
            <ul>
                <li>Processing and verifying vehicle bookings and rental agreements.</li>
                <li>Providing live GPS tracking for active trips and facilitating 24/7 roadside breakdown assistance.</li>
                <li>Communicating booking confirmations, safety notices, and updates via direct messaging or WhatsApp.</li>
            </ul>

            <h3>3. Data Security & Protection</h3>
            <p>We implement robust administrative and technical safeguards (including password hashing and secure session controls) to protect your data from unauthorized access, alteration, or disclosure. Your payment and bank records are handled with high security standards.</p>

            <h3>4. Contact & Support</h3>
            <p>If you have any questions, concerns, or requests regarding this Privacy Policy or your data privacy, you can directly reach out to our administration office:</p>
            <ul>
                <li><strong>Owner:</strong> Jayesh Harish Bhavsar</li>
                <li><strong>Location:</strong> Gohil Nagar, Amalner, Maharashtra, India</li>
                <li><strong>Helpline:</strong> +91 9765432442 | jayeshbhavsar997@gmail.com</li>
            </ul>
        </div>
    </section>

    <footer>
        <p>&copy; 2026 <span>JAY'S CARS (Car Rental Management System)</span>. Built & Managed by Jayesh Bhavsar. All rights reserved.</p>
        <div class="footer-links">
            <a href="#privacy-policy">Privacy Policy</a>
            <a href="/contact">Support Center</a>
            <a href="/home">App Dashboard</a>
        </div>
    </footer>

    <script>
        let slides = document.querySelectorAll('.bg-slide');
        let currentSlide = 0;
        
        function nextSlide() {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }
        
        setInterval(nextSlide, 5000);
    </script>
</body>
</html>
"""

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JAY'S CARS - Car Rental Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        :root { --sidebar-bg: #0f172a; --sidebar-active: #2563eb; --bg-main: #f8fafc; --text-dark: #1e293b; --text-muted: #64748b; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-dark); display: flex; min-height: 100vh; overflow-x: hidden; }

        .content-body { animation: fadeInUp 0.4s ease-in-out; }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .sidebar { width: 250px; background: var(--sidebar-bg); color: white; display: flex; flex-direction: column; padding: 20px 15px; flex-shrink: 0; }
        .sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 10px 5px 25px 5px; border-bottom: 1px solid #1e293b; }
        .sidebar-brand i { font-size: 1.8rem; color: #2563eb; }
        .sidebar-brand div { font-size: 1.1rem; font-weight: 700; }
        .sidebar-brand span { font-size: 0.75rem; color: #94a3b8; display: block; }

        .sidebar-top-auth { margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #1e293b; }

        .nav-list { list-style: none; margin-top: 10px; display: flex; flex-direction: column; gap: 6px; }
        .nav-item a { display: flex; align-items: center; gap: 14px; padding: 12px 16px; color: #94a3b8; text-decoration: none; font-size: 0.9rem; font-weight: 500; border-radius: 8px; transition: all 0.3s ease; }
        .nav-item.active a, .nav-item a:hover { background: var(--sidebar-active); color: white; transform: translateX(4px); }
        .sidebar-footer { margin-top: auto; padding-top: 20px; border-top: 1px solid #1e293b; font-size: 0.85rem; color: #64748b; }

        .main-wrapper { flex: 1; display: flex; flex-direction: column; }
        .top-header { background: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
        .top-header h2 { font-size: 1.3rem; font-weight: 700; color: #0f172a; }
        .content-body { padding: 25px 30px; flex: 1; }

        .hero-banner { background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%); color: white; padding: 50px 40px; border-radius: 16px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px; box-shadow: 0 10px 25px rgba(37,99,235,0.15); }
        .hero-content { max-width: 600px; }
        .hero-content h1 { font-size: 2.2rem; font-weight: 700; margin-bottom: 12px; line-height: 1.2; }
        .hero-content p { font-size: 1rem; color: #cbd5e1; margin-bottom: 20px; line-height: 1.6; }
        .hero-btn { background: #2563eb; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; display: inline-block; transition: all 0.3s ease; box-shadow: 0 4px 12px rgba(37,99,235,0.3); }
        .hero-btn:hover { background: #1d4ed8; transform: translateY(-2px); }

        .hero-icon-anim { font-size: 7rem; color: #3b82f6; animation: floatCar 3s ease-in-out infinite; }
        @keyframes floatCar {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }

        .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 35px; }
        .feature-box { background: white; padding: 22px; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center; transition: all 0.3s ease; }
        .feature-box:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.06); }
        .feature-box i { font-size: 2rem; color: #2563eb; margin-bottom: 12px; }
        .feature-box h4 { font-size: 1rem; font-weight: 600; margin-bottom: 6px; }
        .feature-box p { font-size: 0.85rem; color: #64748b; }

        .car-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
        .car-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; cursor: pointer; display: flex; flex-direction: column; transition: all 0.35s ease; }
        .car-card:hover { transform: translateY(-6px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
        .car-card img { width: 100%; height: 180px; object-fit: cover; background: #ffffff; transition: transform 0.5s ease; border-bottom: 1px solid #f1f5f9; }
        .car-card:hover img { transform: scale(1.04); }
        .car-card-body { padding: 18px; display: flex; flex-direction: column; flex: 1; }
        .btn-book { display: block; width: 100%; text-align: center; background: #2563eb; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: 600; margin-top: auto; transition: background 0.3s; }
        .btn-book:hover { background: #1d4ed8; }

        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
        .stat-card { background: white; padding: 20px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; border: 1px solid #f1f5f9; }
        .stat-info h4 { font-size: 0.85rem; color: var(--text-muted); }
        .stat-info .num { font-size: 1.6rem; font-weight: 700; margin: 5px 0; }
        .stat-icon { width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: white; }

        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(15,23,42,0.85); overflow-y: auto; }
        .modal-content { background: white; margin: 30px auto; padding: 25px; border-radius: 16px; max-width: 800px; width: 90%; position: relative; }

        .close { position: absolute; right: 20px; top: 15px; font-size: 24px; cursor: pointer; }
        .close:hover { color: #ef4444; }
        .tab-btn { padding: 8px 16px; border-radius: 6px; border: 1px solid #cbd5e1; background: white; cursor: pointer; font-weight: 600; margin-right: 8px; margin-bottom: 15px; }
        .tab-btn.active { background: #2563eb; color: white; border-color: #2563eb; }
        .main-media { width: 100%; height: 350px; object-fit: cover; border-radius: 12px; margin-bottom: 15px; background: #fff; border: 1px solid #e2e8f0; }
        .thumbs { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
        .thumb-img { width: 100%; height: 70px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 2px solid transparent; }
        .thumb-img.active { border-color: #2563eb; }

        .form-box { background: white; padding: 30px; border-radius: 12px; max-width: 500px; margin: 20px auto; border: 1px solid #e2e8f0; box-shadow: 0 4px 15px rgba(0,0,0,0.03); }
        .form-group { margin-bottom: 18px; position: relative; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.88rem; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 12px; border: 1.5px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem; }
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: #2563eb; outline: none; }
        .btn-submit { width: 100%; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: background 0.3s; }
        .btn-submit:hover { background: #1d4ed8; }

        .suggestions-list { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-top: none; border-radius: 0 0 6px 6px; max-height: 180px; overflow-y: auto; z-index: 99; box-shadow: 0 6px 12px rgba(0,0,0,0.08); }
        .suggestion-item { padding: 10px 12px; font-size: 0.88rem; cursor: pointer; border-bottom: 1px solid #f1f5f9; }
        .suggestion-item:hover { background: #eff6ff; color: #2563eb; }

        #liveMap { width: 100%; height: 350px; border-radius: 10px; margin-top: 15px; border: 1px solid #cbd5e1; }
        .table-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #f1f5f9; margin-bottom: 25px; }
        table { width: 100%; border-collapse: collapse; text-align: left; }
        th { font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); padding: 12px 10px; border-bottom: 1px solid #e2e8f0; }
        td { font-size: 0.88rem; padding: 12px 10px; border-bottom: 1px solid #f1f5f9; }
    </style>
</head>
<body>

    <div class="sidebar">
        <div class="sidebar-brand">
            <i class="fa-solid fa-car-side"></i>
            <div>JAY'S CARS<span>Management System</span></div>
        </div>

        <div class="sidebar-top-auth" style="margin-top: 15px;">
            {% if session.get('customer_user') %}
                <div style="background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <p style="font-size: 0.85rem; color: #94a3b8;"><i class="fa-solid fa-circle-user" style="color: #3b82f6;"></i> Logged In As:</p>
                    <p style="font-size: 0.9rem; font-weight: 600; color: white; margin: 4px 0;">{{ session['customer_user']['name'] }}</p>
                    <a href="/customer/logout" style="color: #ef4444; text-decoration: none; font-size: 0.82rem; font-weight: 600; display: inline-block; margin-top: 4px;"><i class="fa-solid fa-right-from-bracket"></i> Logout</a>
                </div>
            {% elif session.get('admin_logged_in') %}
                <div style="background: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155;">
                    <p style="font-size: 0.85rem; color: #94a3b8;"><i class="fa-solid fa-user-shield" style="color: #10b981;"></i> Admin Panel Active</p>
                    <a href="/admin/logout" style="color: #ef4444; text-decoration: none; font-size: 0.82rem; font-weight: 600; display: inline-block; margin-top: 4px;"><i class="fa-solid fa-right-from-bracket"></i> Admin Logout</a>
                </div>
            {% else %}
                <div style="display: flex; flex-direction: column; gap: 6px;">
                    <a href="/customer/login" style="background: #2563eb; color: white; text-decoration: none; font-size: 0.85rem; font-weight: 600; padding: 8px 12px; border-radius: 6px; text-align: center;"><i class="fa-solid fa-right-to-bracket"></i> Customer Login</a>
                    <a href="/customer/register" style="background: #334155; color: white; text-decoration: none; font-size: 0.82rem; font-weight: 500; padding: 6px 12px; border-radius: 6px; text-align: center;"><i class="fa-solid fa-user-plus"></i> Register</a>
                </div>
            {% endif %}
        </div>

        <ul class="nav-list">
            <li class="nav-item">
                <a href="/"><i class="fa-solid fa-globe"></i> Landing Page</a>
            </li>
            <li class="nav-item {% if page == 'home' %}active{% endif %}">
                <a href="/home"><i class="fa-solid fa-house"></i> Home & Fleet</a>
            </li>
            {% if session.get('customer_user') %}
            <li class="nav-item {% if page == 'my_bookings' %}active{% endif %}">
                <a href="/customer/my-bookings"><i class="fa-solid fa-receipt"></i> My Bookings</a>
            </li>
            <li class="nav-item {% if page == 'breakdown_request' %}active{% endif %}">
                <a href="/customer/breakdown"><i class="fa-solid fa-triangle-exclamation"></i> Breakdown Support</a>
            </li>
            {% endif %}
            
            <li class="nav-item {% if page == 'dashboard' %}active{% endif %}">
                <a href="/admin/dashboard"><i class="fa-solid fa-gauge"></i> Admin Dashboard</a>
            </li>

            {% if session.get('admin_logged_in') %}
            <li class="nav-item {% if page == 'admin_bank' %}active{% endif %}">
                <a href="/admin/bank-payments"><i class="fa-solid fa-building-columns"></i> Bank & Payments</a>
            </li>
            {% endif %}
            <li class="nav-item {% if page == 'contact' %}active{% endif %}">
                <a href="/contact"><i class="fa-solid fa-address-book"></i> Contact Us</a>
            </li>
        </ul>

        <div class="sidebar-footer">
            {% if not session.get('customer_user') and not session.get('admin_logged_in') %}
                <a href="/admin/login" style="color: #94a3b8; text-decoration: none; font-size: 0.85rem; display: block;"><i class="fa-solid fa-user-shield"></i> Admin Login</a>
            {% endif %}
        </div>
    </div>

    <div class="main-wrapper">
        <div class="top-header">
            <h2>{{ title }}</h2>
            <div style="display: flex; align-items: center; gap: 12px;">
                {% if session.get('customer_user') %}
                    <span style="font-weight: 600; color: #2563eb; display: flex; align-items: center; gap: 6px;">
                        <i class="fa-solid fa-circle-user"></i> {{ session['customer_user']['name'] }}
                    </span>
                    <a href="/customer/logout" style="background: #fee2e2; color: #991b1b; padding: 5px 12px; border-radius: 6px; text-decoration: none; font-size: 0.82rem; font-weight: 600;">
                        <i class="fa-solid fa-right-from-bracket"></i> Logout
                    </a>
                {% elif session.get('admin_logged_in') %}
                    <span style="font-weight: 600; color: #10b981;"><i class="fa-solid fa-user-shield"></i> Admin Panel</span>
                    <a href="/admin/logout" style="background: #fee2e2; color: #991b1b; padding: 5px 12px; border-radius: 6px; text-decoration: none; font-size: 0.82rem; font-weight: 600;">
                        Logout
                    </a>
                {% else %}
                    <a href="/customer/login" style="text-decoration: none; font-weight: 600; color: #2563eb; margin-right: 15px;">Customer Login</a>
                    <a href="/admin/login" style="text-decoration: none; font-weight: 600; color: #64748b;">Admin Login</a>
                {% endif %}
            </div>
        </div>

        <div class="content-body">
            {% for message in get_flashed_messages() %}
                <div style="padding: 15px; background: #d1fae5; color: #065f46; border-radius: 8px; margin-bottom: 20px; font-weight: 600; box-shadow: 0 3px 10px rgba(0,0,0,0.04);">
                    <i class="fa-solid fa-circle-check"></i> {{ message }}
                    {% if session.get('last_booking_msg') %}
                    <div style="margin-top: 10px;">
                        <a href="https://wa.me/919765432442?text={{ session.get('last_booking_msg') }}" target="_blank" style="background: #10b981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 6px; display: inline-block;"><i class="fa-brands fa-whatsapp"></i> Send WhatsApp Booking to Owner (+919765432442)</a>
                    </div>
                    {% endif %}
                    {% if session.get('last_breakdown_msg') %}
                    <div style="margin-top: 10px;">
                        <a href="https://wa.me/919765432442?text={{ session.get('last_breakdown_msg') }}" target="_blank" style="background: #ef4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 6px; display: inline-block;"><i class="fa-brands fa-whatsapp"></i> Send Emergency WhatsApp SOS to Owner</a>
                    </div>
                    {% endif %}
                </div>
            {% endfor %}

            {% if page == 'home' %}
                <div class="hero-banner">
                    <div class="hero-content">
                        <h1>Experience the Best Car Rental Service in Maharashtra</h1>
                        <p>Choose from our top-tier fleet of 20 verified vehicles. Enjoy seamless booking, live GPS route tracking, and 24/7 roadside breakdown assistance managed by Jayesh Bhavsar.</p>
                        <a href="#fleetSection" class="hero-btn"><i class="fa-solid fa-car"></i> Explore Fleet Now</a>
                    </div>
                    <div>
                        <i class="fa-solid fa-car-side hero-icon-anim"></i>
                    </div>
                </div>

                <div class="features-grid">
                    <div class="feature-box">
                        <i class="fa-solid fa-shield-halved"></i>
                        <h4>100% Safe & Verified</h4>
                        <p>All cars undergo rigorous safety checks and sanitization before every ride.</p>
                    </div>
                    <div class="feature-box">
                        <i class="fa-solid fa-map-location-dot"></i>
                        <h4>Live GPS Tracking</h4>
                        <p>Real-time vehicle movement tracking for both customers and admin.</p>
                    </div>
                    <div class="feature-box">
                        <i class="fa-solid fa-headset"></i>
                        <h4>24/7 Breakdown Support</h4>
                        <p>Instant mechanic dispatch and live administrative support replies.</p>
                    </div>
                    <div class="feature-box">
                        <i class="fa-solid fa-indian-rupee-sign"></i>
                        <h4>Transparent Pricing</h4>
                        <p>Affordable daily rental rates with zero hidden charges.</p>
                    </div>
                </div>

                <div id="fleetSection" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h2 style="font-size: 1.3rem;">Top Selling Fleet Vehicles</h2>
                    <span style="color: #64748b; font-size: 0.9rem;">Showing all available models</span>
                </div>

                <div class="car-grid">
                    {% for car in cars %}
                    <div class="car-card" onclick="openModal('{{ car['name'] }}', {{ car['photos']|tojson }}, {{ car['videos']|tojson }})">
                        <img src="{{ car['image'] }}" alt="{{ car['name'] }}">
                        <div class="car-card-body">
                            <h3 style="font-size: 1.1rem;">{{ car['name'] }}</h3>
                            <p style="color: var(--text-muted); font-size: 0.85rem; margin: 5px 0;">{{ car['type'] }} | {{ car['seats'] }}</p>
                            <p style="color: #64748b; font-size: 0.8rem;"><i class="fa-solid fa-camera"></i> 5 Photos | <i class="fa-solid fa-video"></i> 5 Videos</p>
                            <div style="font-size: 1.2rem; font-weight: 700; color: #2563eb; margin: 8px 0;">₹{{ car['price'] }} / day</div>
                            <div onclick="event.stopPropagation();">
                                <a href="/book/{{ car['id'] }}" class="btn-book"><i class="fa-solid fa-car-side"></i> Book Vehicle</a>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>

                <div id="galleryModal" class="modal">
                    <div class="modal-content">
                        <span class="close" onclick="closeModal()">&times;</span>
                        <h3 id="modalName" style="margin-bottom: 10px;">Vehicle Media</h3>
                        <div>
                            <button id="btnPhotos" class="tab-btn active" onclick="switchMediaMode('photos')"><i class="fa-solid fa-images"></i> 5 Photos</button>
                            <button id="btnVideos" class="tab-btn" onclick="switchMediaMode('videos')"><i class="fa-solid fa-video"></i> 5 Videos</button>
                        </div>
                        <img id="mainImg" class="main-media" src="" alt="Main Image">
                        <video id="mainVideo" class="main-media" controls style="display: none;"></video>
                        <div class="thumbs" id="thumbsContainer"></div>
                    </div>
                </div>

            {% elif page == 'customer_login' %}
                <div class="form-box">
                    <h2 style="text-align: center; margin-bottom: 20px;">Customer Sign In</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label>Email Address</label>
                            <input type="email" name="email" required placeholder="name@example.com">
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" name="password" required placeholder="••••••••">
                        </div>
                        <button type="submit" class="btn-submit">Sign In</button>
                    </form>
                    <p style="text-align: center; margin-top: 15px; font-size: 0.88rem;">
                        New Customer? <a href="/customer/register" style="color: #2563eb; font-weight: 600;">Register Account</a>
                    </p>
                </div>

            {% elif page == 'customer_register' %}
                <div class="form-box">
                    <h2 style="text-align: center; margin-bottom: 20px;">Create Customer Account</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label>Full Name</label>
                            <input type="text" name="name" required placeholder="Rahul Patil">
                        </div>
                        <div class="form-group">
                            <label>Mobile Number</label>
                            <input type="tel" name="phone" required placeholder="10-digit number">
                        </div>
                        <div class="form-group">
                            <label>Driving License Number</label>
                            <input type="text" name="license" required placeholder="MH-19-2023-XXXXXXX">
                        </div>
                        <div class="form-group">
                            <label>Email Address</label>
                            <input type="email" name="email" required placeholder="name@example.com">
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" name="password" required placeholder="••••••••">
                        </div>
                        <button type="submit" class="btn-submit">Register Account</button>
                    </form>
                </div>

            {% elif page == 'my_bookings' %}
                <div class="table-card">
                    <h3 style="margin-bottom: 15px;">My Rental Bookings & Live Tracking</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Booking ID</th>
                                <th>Vehicle</th>
                                <th>Pickup / Drop</th>
                                <th>Days & Cost</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for b in my_bookings %}
                            <tr>
                                <td><b>{{ b['id'] }}</b></td>
                                <td>{{ b['vehicle'] }}</td>
                                <td><small><i class="fa-solid fa-location-dot" style="color: #10b981;"></i> {{ b['start_location'] }}<br><i class="fa-solid fa-flag-checkered" style="color: #ef4444;"></i> {{ b['end_location'] }}</small></td>
                                <td>{{ b['days'] }} Days<br><b>₹{{ b['total_cost'] }}</b></td>
                                <td>
                                    {% if b['status'] == 'Confirmed' %}
                                        <span style="background: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 12px; font-weight: 600;">Confirmed</span>
                                    {% elif b['status'] == 'Rejected' %}
                                        <span style="background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 12px; font-weight: 600;">Rejected</span>
                                    {% elif b['status'] == 'Cancelled' %}
                                        <span style="background: #f1f5f9; color: #64748b; padding: 4px 10px; border-radius: 12px; font-weight: 600;">Cancelled</span>
                                    {% else %}
                                        <span style="background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 12px; font-weight: 600;">Pending Approval</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <div style="display: flex; gap: 6px;">
                                        {% if b['status'] == 'Confirmed' %}
                                            <a href="/track/{{ b['clean_id'] }}" style="background: #2563eb; color: white; padding: 5px 10px; text-decoration: none; border-radius: 6px; font-size: 0.78rem; font-weight: 600;"><i class="fa-solid fa-satellite-dish"></i> Track</a>
                                        {% endif %}
                                        {% if b['status'] != 'Cancelled' and b['status'] != 'Rejected' %}
                                            <a href="/customer/cancel/{{ b['id'] }}" onclick="return confirm('Are you sure you want to cancel this booking?');" style="background: #ef4444; color: white; padding: 5px 10px; text-decoration: none; border-radius: 6px; font-size: 0.78rem; font-weight: 600;"><i class="fa-solid fa-ban"></i> Cancel</a>
                                        {% endif %}
                                    </div>
                                </td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" style="text-align: center; color: #64748b; padding: 25px;">No active bookings found.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="table-card" style="margin-top: 20px;">
                    <h3 style="margin-bottom: 15px;"><i class="fa-solid fa-headset" style="color: #ef4444;"></i> Breakdown Assistance Status & Admin Messages</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Request ID</th>
                                <th>Vehicle</th>
                                <th>Issue</th>
                                <th>Location</th>
                                <th>Admin Support Reply</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for br in my_breakdowns %}
                            <tr>
                                <td><b>{{ br['id'] }}</b></td>
                                <td>{{ br['vehicle'] }}</td>
                                <td><span style="background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; font-weight: 600;">{{ br['issue'] }}</span></td>
                                <td>{{ br['location'] }}</td>
                                <td>
                                    {% if br['admin_reply'] %}
                                        <div style="background: #eff6ff; color: #1e40af; padding: 8px 12px; border-radius: 6px; font-weight: 600; border-left: 4px solid #2563eb;">
                                            <i class="fa-solid fa-user-shield"></i> {{ br['admin_reply'] }}
                                        </div>
                                    {% else %}
                                        <span style="color: #d97706; font-style: italic; font-weight: 500;">Awaiting mechanic assignment & reply...</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% else %}
                            <tr><td colspan="5" style="text-align: center; color: #64748b; padding: 20px;">No breakdown requests submitted yet.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

            {% elif page == 'track_booking' %}
                <div class="form-box" style="max-width: 700px;">
                    <h3 style="margin-bottom: 5px;"><i class="fa-solid fa-satellite-dish" style="color: #2563eb;"></i> Live Vehicle Tracking</h3>
                    <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 15px;">Booking ID: <b>{{ booking['id'] }}</b> | Vehicle: <b>{{ booking['vehicle'] }}</b></p>
                    <div style="font-size: 0.85rem; margin-bottom: 10px;">
                        <span style="color: #10b981; font-weight: 600;">● Start:</span> {{ booking['start_location'] }}<br>
                        <span style="color: #ef4444; font-weight: 600;">● Destination:</span> {{ booking['end_location'] }}
                    </div>
                    <div id="liveMap"></div>
                    <div style="margin-top: 15px; text-align: center;">
                        <a href="/customer/my-bookings" class="btn-submit" style="display: inline-block; text-decoration: none; background: #64748b; width: auto; padding: 8px 20px;">Back to Bookings</a>
                    </div>
                </div>
                <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        var map = L.map('liveMap').setView([21.0503, 75.0601], 13);
                        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                            maxZoom: 19,
                        }).addTo(map);

                        var carIcon = L.divIcon({
                            html: '<i class="fa-solid fa-car-side" style="font-size: 24px; color: #2563eb; background: white; padding: 6px; border-radius: 50%; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"></i>',
                            className: 'dummy-car-icon',
                            iconSize: [36, 36],
                            iconAnchor: [18, 18]
                        });

                        var marker = L.marker([21.0503, 75.0601], {icon: carIcon}).addTo(map);
                        marker.bindPopup("<b>{{ booking['vehicle'] }}</b><br>Status: On the Move (Live GPS)").openPopup();

                        let lat = 21.0503, lng = 75.0601;
                        setInterval(() => {
                            lat += (Math.random() - 0.5) * 0.002;
                            lng += (Math.random() - 0.5) * 0.002;
                            marker.setLatLng([lat, lng]);
                            map.panTo([lat, lng]);
                        }, 3000);
                    });
                </script>

            {% elif page == 'breakdown_request' %}
                <div class="form-box" style="max-width: 550px;">
                    <h2 style="margin-bottom: 8px;"><i class="fa-solid fa-triangle-exclamation" style="color: #ef4444;"></i> Vehicle Breakdown Assistance</h2>
                    <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 20px;">Stranded or facing a mechanical problem? Send an instant emergency assistance request.</p>
                    <form method="POST">
                        <div class="form-group">
                            <label>Select Your Booking / Vehicle</label>
                            <select name="booking_id" required>
                                <option value="">-- Select Active Booking --</option>
                                {% for b in my_bookings %}
                                <option value="{{ b['id'] }}">{{ b['id'] }} - {{ b['vehicle'] }} (Pickup: {{ b['start_location'] }})</option>
                                {% endfor %}
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Issue Category</label>
                            <select name="issue_type" required>
                                <option value="Engine Failure / Won't Start">Engine Failure / Won't Start</option>
                                <option value="Flat Tyre / Puncture">Flat Tyre / Puncture</option>
                                <option value="Battery Dead / Electrical Issue">Battery Dead / Electrical Issue</option>
                                <option value="Accident / Collision Damage">Accident / Collision Damage</option>
                                <option value="Overheating / Coolant Leak">Overheating / Coolant Leak</option>
                                <option value="Other Mechanical Problem">Other Mechanical Problem</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label>Current Breakdown Location / Landmark</label>
                            <input type="text" name="breakdown_location" required placeholder="e.g., Near Bus Stand, Amalner">
                        </div>
                        <div class="form-group">
                            <label>Describe the Problem (Optional)</label>
                            <textarea name="description" rows="3" placeholder="Provide extra details..."></textarea>
                        </div>
                        <button type="submit" class="btn-submit" style="background: #ef4444;"><i class="fa-solid fa-headset"></i> Request Emergency Assistance</button>
                    </form>
                </div>

            {% elif page == 'dashboard' %}
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-info">
                            <h4>Total Bookings</h4>
                            <div class="num">{{ total_bookings }}</div>
                        </div>
                        <div class="stat-icon" style="background: #8b5cf6;"><i class="fa-solid fa-calendar-days"></i></div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-info">
                            <h4>Total Vehicles</h4>
                            <div class="num">20</div>
                        </div>
                        <div class="stat-icon" style="background: #10b981;"><i class="fa-solid fa-car"></i></div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-info">
                            <h4>Breakdown Alerts</h4>
                            <div class="num" style="color: #ef4444;">{{ total_breakdowns }}</div>
                        </div>
                        <div class="stat-icon" style="background: #ef4444;"><i class="fa-solid fa-triangle-exclamation"></i></div>
                    </div>

                    <div class="stat-card">
                        <div class="stat-info">
                            <h4>Total Revenue</h4>
                            <div class="num">₹ {{ total_revenue }}</div>
                        </div>
                        <div class="stat-icon" style="background: #2563eb;"><i class="fa-solid fa-indian-rupee-sign"></i></div>
                    </div>
                </div>

                <div class="table-card">
                    <h3 style="margin-bottom: 15px;"><i class="fa-solid fa-triangle-exclamation" style="color: #ef4444;"></i> Breakdown & Roadside Assistance Logs (Admin Control)</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Request ID</th>
                                <th>Customer</th>
                                <th>Vehicle</th>
                                <th>Issue / Location</th>
                                <th>Current Status</th>
                                <th>Send Quick Reply</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for br in breakdowns %}
                            <tr>
                                <td><b>{{ br['id'] }}</b></td>
                                <td>{{ br['customer_name'] }}<br><small style="color: #64748b;">{{ br['customer_phone'] }}</small></td>
                                <td>{{ br['vehicle'] }}</td>
                                <td><span style="background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; font-weight: 600;">{{ br['issue'] }}</span><br><small>{{ br['location'] }}</small></td>
                                <td>
                                    <span style="background: #fef3c7; color: #92400e; padding: 3px 8px; border-radius: 12px; font-weight: 600; display: inline-block; margin-bottom: 5px;">{{ br['status'] }}</span>
                                    {% if br['admin_reply'] %}
                                    <div style="font-size: 0.8rem; color: #1e40af; background: #eff6ff; padding: 4px; border-radius: 4px;"><strong>Last Reply:</strong> {{ br['admin_reply'] }}</div>
                                    {% endif %}
                                </td>
                                <td>
                                    <form action="/admin/breakdown/reply" method="POST" style="display: flex; gap: 5px; flex-direction: column;">
                                        <input type="hidden" name="breakdown_id" value="{{ br['id'] }}">
                                        <select name="reply_text" style="padding: 6px; font-size: 0.8rem; border-radius: 4px; border: 1px solid #cbd5e1;" required>
                                            <option value="">-- Choose Quick Reply --</option>
                                            <option value="Mechanic is dispatched to your location, please wait 15 mins.">Mechanic dispatched, please wait 15 mins.</option>
                                            <option value="We have received your alert. Backup vehicle is on the way.">Backup vehicle on the way.</option>
                                            <option value="Please stay calm at your location. Roadside assistance team is calling you now.">Assistance team is calling you.</option>
                                        </select>
                                        <button type="submit" style="background: #2563eb; color: white; border: none; padding: 6px 10px; border-radius: 4px; font-size: 0.78rem; font-weight: 600; cursor: pointer;">Send Reply</button>
                                    </form>
                                </td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" style="text-align: center; color: #64748b; padding: 20px;">No breakdown assistance requests recorded.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="table-card">
                    <h3 style="margin-bottom: 15px;">Customer Bookings Approval Management</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Booking ID</th>
                                <th>Customer Name</th>
                                <th>Vehicle</th>
                                <th>Route / Days</th>
                                <th>Status</th>
                                <th>Admin Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for b in bookings %}
                            <tr>
                                <td><b>{{ b['id'] }}</b></td>
                                <td>{{ b['customer'] }}<br><small>{{ b['phone'] }}</small></td>
                                <td>{{ b['vehicle'] }}</td>
                                <td>{{ b['start_location'] }} ➔ {{ b['end_location'] }}<br>({{ b['days'] }} Days | ₹{{ b['total_cost'] }})</td>
                                <td>
                                    {% if b['status'] == 'Confirmed' %}
                                        <span style="background: #d1fae5; color: #065f46; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Confirmed</span>
                                    {% elif b['status'] == 'Rejected' %}
                                        <span style="background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Rejected</span>
                                    {% elif b['status'] == 'Cancelled' %}
                                        <span style="background: #f1f5f9; color: #64748b; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Cancelled</span>
                                    {% else %}
                                        <span style="background: #fef3c7; color: #92400e; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Pending Review</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <div style="display: flex; gap: 6px;">
                                        <a href="/admin/booking/action/{{ b['id'] }}/confirm" style="background: #10b981; color: white; padding: 5px 10px; text-decoration: none; border-radius: 6px; font-size: 0.78rem; font-weight: 600;">Confirm</a>
                                        <a href="/admin/booking/action/{{ b['id'] }}/reject" style="background: #ef4444; color: white; padding: 5px 10px; text-decoration: none; border-radius: 6px; font-size: 0.78rem; font-weight: 600;">Reject</a>
                                    </div>
                                </td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" style="text-align: center; color: #64748b; padding: 20px;">No bookings recorded yet.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

            {% elif page == 'admin_bank' %}
                <div class="form-box" style="max-width: 550px;">
                    <h2 style="margin-bottom: 8px;"><i class="fa-solid fa-building-columns" style="color: #2563eb;"></i> Owner Bank & Withdrawal Details</h2>
                    <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 20px;">Configure owner account information for earnings withdrawals and payouts.</p>
                    <form method="POST">
                        <div class="form-group">
                            <label>Account Holder / Owner Name</label>
                            <input type="text" name="account_name" required value="{{ bank_info['account_name'] }}">
                        </div>
                        <div class="form-group">
                            <label>Bank Name</label>
                            <input type="text" name="bank_name" required value="{{ bank_info['bank_name'] }}">
                        </div>
                        <div class="form-group">
                            <label>Account Number</label>
                            <input type="text" name="account_number" required value="{{ bank_info['account_number'] }}">
                        </div>
                        <div class="form-group">
                            <label>IFSC Code</label>
                            <input type="text" name="ifsc_code" required value="{{ bank_info['ifsc_code'] }}">
                        </div>
                        <div class="form-group">
                            <label>UPI ID</label>
                            <input type="text" name="upi_id" required value="{{ bank_info['upi_id'] }}">
                        </div>
                        <button type="submit" class="btn-submit"><i class="fa-solid fa-floppy-disk"></i> Save Withdrawal Details</button>
                    </form>
                </div>

            {% elif page == 'login' %}
                <div class="form-box">
                    <h2 style="text-align: center; margin-bottom: 20px;">Admin Login</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label>Admin Email</label>
                            <input type="email" name="email" required placeholder="jayeshbhavsar997@gmail.com">
                        </div>
                        <div class="form-group">
                            <label>Password</label>
                            <input type="password" name="password" required placeholder="••••••••">
                        </div>
                        <button type="submit" class="btn-submit">Sign In to Dashboard</button>
                    </form>
                </div>

            {% elif page == 'contact' %}
                <div class="form-box" style="max-width: 600px;">
                    <h2><i class="fa-solid fa-headset" style="color: #2563eb;"></i> 24/7 Support & Contact Center</h2>
                    <p style="color: var(--text-muted); font-size: 0.9rem; margin: 8px 0 20px 0;">Need immediate help or booking assistance? Reach out to us anytime through the options below:</p>
                    
                    <div style="display: flex; flex-direction: column; gap: 14px;">
                        <div style="background: #f1f5f9; padding: 15px; border-radius: 10px; border-left: 4px solid #2563eb;">
                            <p style="font-size: 0.95rem; font-weight: 700; color: #0f172a;">{{ owner['name'] }}</p>
                            <p style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">{{ owner['address'] }}</p>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;">
                            <a href="tel:9765432442" style="background: #2563eb; color: white; padding: 12px 10px; border-radius: 8px; text-decoration: none; font-size: 0.85rem; font-weight: 600; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 5px; box-shadow: 0 4px 10px rgba(37,99,235,0.2);">
                                <i class="fa-solid fa-phone" style="font-size: 1.1rem;"></i> Call Now
                            </a>

                            <a href="https://wa.me/919765432442?text=Hello%20Jayesh,%20I%20need%20assistance%20with%20car%20rental." target="_blank" style="background: #10b981; color: white; padding: 12px 10px; border-radius: 8px; text-decoration: none; font-size: 0.85rem; font-weight: 600; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 5px; box-shadow: 0 4px 10px rgba(16,185,129,0.2);">
                                <i class="fa-brands fa-whatsapp" style="font-size: 1.2rem;"></i> WhatsApp
                            </a>

                            <a href="mailto:jayeshbhavsar997@gmail.com?subject=Car%20Rental%20Support%20Inquiry" style="background: #8b5cf6; color: white; padding: 12px 10px; border-radius: 8px; text-decoration: none; font-size: 0.85rem; font-weight: 600; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 5px; box-shadow: 0 4px 10px rgba(139,92,246,0.2);">
                                <i class="fa-solid fa-envelope" style="font-size: 1.1rem;"></i> Send Email
                            </a>
                        </div>
                    </div>
                </div>

            {% elif page == 'book' %}
                <div class="form-box" style="max-width: 600px;">
                    <h2>Book {{ car['name'] }}</h2>
                    <p style="color: var(--text-muted); margin-bottom: 20px;">Rate: <strong>₹ {{ car['price'] }} / day</strong></p>
                    <form method="POST">
                        <div class="form-group">
                            <label>Customer Name</label>
                            <input type="text" name="customer_name" required value="{{ session.get('customer_user', {}).get('name', '') }}">
                        </div>
                        <div class="form-group">
                            <label>Mobile Number</label>
                            <input type="tel" name="phone" required value="{{ session.get('customer_user', {}).get('phone', '') }}">
                        </div>

                        <div class="form-group" style="position: relative;">
                            <label><i class="fa-solid fa-location-dot" style="color: #10b981;"></i> Starting Location (Pickup)</label>
                            <input type="text" id="start_location" name="start_location" autocomplete="off" required placeholder="Enter starting city, landmark...">
                            <div id="start_suggestions" class="suggestions-list" style="display: none;"></div>
                        </div>

                        <div class="form-group" style="position: relative;">
                            <label><i class="fa-solid fa-flag-checkered" style="color: #ef4444;"></i> Ending Location (Drop-off)</label>
                            <input type="text" id="end_location" name="end_location" autocomplete="off" required placeholder="Enter destination city, landmark...">
                            <div id="end_suggestions" class="suggestions-list" style="display: none;"></div>
                        </div>

                        <div class="form-group">
                            <label>Rental Start Date</label>
                            <input type="date" name="start_date" min="{{ min_date }}" required>
                        </div>
                        <div class="form-group">
                            <label>Rental Days</label>
                            <input type="number" name="days" value="1" min="1" max="30" required>
                        </div>
                        <button type="submit" class="btn-submit">Confirm Booking</button>
                    </form>
                </div>

                <script>
                    function setupLocationAutocomplete(inputId, containerId) {
                        const input = document.getElementById(inputId);
                        const container = document.getElementById(containerId);
                        let timeout = null;

                        input.addEventListener('input', function() {
                            clearTimeout(timeout);
                            const query = this.value.trim();
                            if (query.length < 3) {
                                container.style.display = 'none';
                                return;
                            }

                            timeout = setTimeout(() => {
                                fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&countrycodes=in&limit=5`)
                                    .then(response => response.json())
                                    .then(data => {
                                        container.innerHTML = '';
                                        if (data.length > 0) {
                                            container.style.display = 'block';
                                            data.forEach(item => {
                                                const div = document.createElement('div');
                                                div.className = 'suggestion-item';
                                                div.innerText = item.display_name;
                                                div.onclick = function() {
                                                    input.value = item.display_name;
                                                    container.style.display = 'none';
                                                };
                                                container.appendChild(div);
                                            });
                                        } else {
                                            container.style.display = 'none';
                                        }
                                    })
                                    .catch(err => console.log('Location fetch error'));
                            }, 300);
                        });

                        document.addEventListener('click', function(e) {
                            if (!input.contains(e.target) && !container.contains(e.target)) {
                                container.style.display = 'none';
                            }
                        });
                    }

                    window.onload = function() {
                        setupLocationAutocomplete('start_location', 'start_suggestions');
                        setupLocationAutocomplete('end_location', 'end_suggestions');
                    };
                </script>
            {% endif %}
        </div>
    </div>

    <script>
        var currentPhotos = [];
        var currentVideos = [];

        function openModal(name, photos, videos) {
            document.getElementById('modalName').innerText = name + " - Media Gallery";
            currentPhotos = photos;
            currentVideos = videos;
            switchMediaMode('photos');
            document.getElementById('galleryModal').style.display = "block";
        }

        function closeModal() {
            var v = document.getElementById('mainVideo');
            if(v) v.pause();
            document.getElementById('galleryModal').style.display = "none";
        }

        function switchMediaMode(mode) {
            var btnP = document.getElementById('btnPhotos');
            var btnV = document.getElementById('btnVideos');
            var imgEl = document.getElementById('mainImg');
            var vidEl = document.getElementById('mainVideo');
            var thumbsEl = document.getElementById('thumbsContainer');

            thumbsEl.innerHTML = '';
            if(vidEl) vidEl.pause();

            if(mode === 'photos') {
                btnP.classList.add('active');
                btnV.classList.remove('active');
                imgEl.style.display = 'block';
                vidEl.style.display = 'none';

                imgEl.src = currentPhotos[0];
                currentPhotos.forEach(function(src, idx) {
                    var thumb = document.createElement('img');
                    thumb.src = src;
                    thumb.className = 'thumb-img' + (idx === 0 ? ' active' : '');
                    thumb.onclick = function() {
                        imgEl.src = src;
                        document.querySelectorAll('.thumb-img').forEach(function(t){ t.classList.remove('active'); });
                        thumb.classList.add('active');
                    };
                    thumbsEl.appendChild(thumb);
                });
            } else {
                btnV.classList.add('active');
                btnP.classList.remove('active');
                imgEl.style.display = 'none';
                vidEl.style.display = 'block';

                vidEl.src = currentVideos[0];
                currentVideos.forEach(function(src, idx) {
                    var btn = document.createElement('button');
                    btn.className = 'tab-btn' + (idx === 0 ? ' active' : '');
                    btn.innerText = 'Video ' + (idx + 1);
                    btn.onclick = function() {
                        vidEl.src = src;
                        vidEl.play();
                    };
                    thumbsEl.appendChild(btn);
                });
            }
        }
    </script>
</body>
</html>
"""

# --- Flask Routes ---
@app.route("/")
def landing_page():
    return render_template_string(LANDING_TEMPLATE)

@app.route("/home")
def home():
    return render_template_string(HTML_LAYOUT, page="home", title="Home & Fleet", owner=OWNER_INFO, cars=CARS)

@app.route("/customer/register", methods=["GET", "POST"])
def customer_register():
    if session.get("admin_logged_in"):
        flash("Please log out from Admin panel first.")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        license_num = request.form.get("license")
        email = request.form.get("email")
        password = request.form.get("password")

        if email in USERS_DB:
            flash("Email already registered. Please log in.")
            return redirect(url_for("customer_login"))

        USERS_DB[email] = {
            "name": name,
            "phone": phone,
            "license": license_num,
            "email": email,
            "password_hash": generate_password_hash(password)
        }
        flash("Registration successful! Please sign in.")
        return redirect(url_for("customer_login"))

    return render_template_string(HTML_LAYOUT, page="customer_register", title="Customer Registration", owner=OWNER_INFO)

@app.route("/customer/login", methods=["GET", "POST"])
def customer_login():
    if session.get("admin_logged_in"):
        flash("Please log out from Admin panel first.")
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = USERS_DB.get(email)
        if user and check_password_hash(user['password_hash'], password):
            session["customer_user"] = {
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"]
            }
            flash(f"Welcome back, {user['name']}!")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password.")

    return render_template_string(HTML_LAYOUT, page="customer_login", title="Customer Sign In", owner=OWNER_INFO)

@app.route("/customer/logout")
def customer_logout():
    session.pop("customer_user", None)
    flash("You have been logged out.")
    return redirect(url_for("landing_page"))

@app.route("/customer/my-bookings")
def my_bookings():
    if not session.get("customer_user"):
        flash("Please log in to view your bookings.")
        return redirect(url_for("customer_login"))

    current_email = session["customer_user"]["email"]
    user_bookings = [b for b in BOOKINGS if b.get("customer_email") == current_email]
    user_breakdowns = [br for br in BREAKDOWN_REQUESTS if br.get("customer_email") == current_email]

    return render_template_string(HTML_LAYOUT, page="my_bookings", title="My Bookings & Assistance", owner=OWNER_INFO, my_bookings=user_bookings, my_breakdowns=user_breakdowns)

@app.route("/customer/cancel/<booking_id>")
def cancel_booking(booking_id):
    if not session.get("customer_user"):
        flash("Please log in.")
        return redirect(url_for("customer_login"))

    for b in BOOKINGS:
        if b["id"] == booking_id and b["customer_email"] == session["customer_user"]["email"]:
            b["status"] = "Cancelled"
            flash(f"Booking {booking_id} has been cancelled successfully.")
            break
    return redirect(url_for("my_bookings"))

@app.route("/book/<int:car_id>", methods=["GET", "POST"])
def book_car(car_id):
    if not session.get("customer_user"):
        flash("Please log in or register before booking a vehicle.")
        return redirect(url_for("customer_login"))

    car = next((c for c in CARS if c["id"] == car_id), None)
    if not car:
        flash("Vehicle not found.")
        return redirect(url_for("home"))

    current_date = datetime.now().strftime('%Y-%m-%d')

    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        phone = request.form.get("phone")
        start_location = request.form.get("start_location")
        end_location = request.form.get("end_location")
        start_date = request.form.get("start_date")
        days = int(request.form.get("days", 1))

        if start_date < current_date:
            flash("Past dates cannot be selected for rental booking.")
            return redirect(url_for("book_car", car_id=car_id))

        booking_id = f"BK-{len(BOOKINGS) + 1001}"
        clean_id = f"CLN-{len(BOOKINGS) + 1001}"
        total_cost = days * car["price"]

        customer_email = session.get("customer_user", {}).get("email")

        booking_data = {
            "id": booking_id,
            "clean_id": clean_id,
            "customer": customer_name,
            "customer_email": customer_email,
            "phone": phone,
            "vehicle": car["name"],
            "start_location": start_location,
            "end_location": end_location,
            "start_date": start_date,
            "days": days,
            "total_cost": total_cost,
            "status": "Pending Review"
        }
        BOOKINGS.append(booking_data)

        whatsapp_text = f"Hello, I have booked a {car['name']} (ID: {booking_id}) from {start_location} to {end_location} for {days} days. Total: ₹{total_cost}."
        session["last_booking_msg"] = whatsapp_text

        flash(f"Booking {booking_id} submitted for admin review! Total Amount: ₹{total_cost}")
        return redirect(url_for("home"))

    return render_template_string(HTML_LAYOUT, page="book", title=f"Book {car['name']}", owner=OWNER_INFO, car=car, min_date=current_date)

@app.route("/track/<clean_id>")
def track_booking(clean_id):
    booking = next((b for b in BOOKINGS if b["clean_id"] == clean_id), None)
    if not booking:
        flash("Booking tracking reference not found.")
        return redirect(url_for("home"))

    return render_template_string(HTML_LAYOUT, page="track_booking", title="Live Vehicle Tracking", owner=OWNER_INFO, booking=booking)

@app.route("/customer/breakdown", methods=["GET", "POST"])
def breakdown_request():
    if not session.get("customer_user"):
        flash("Please log in to request breakdown assistance.")
        return redirect(url_for("customer_login"))

    current_email = session["customer_user"]["email"]
    user_bookings = [b for b in BOOKINGS if b.get("customer_email") == current_email]

    if request.method == "POST":
        booking_id = request.form.get("booking_id")
        issue_type = request.form.get("issue_type")
        location = request.form.get("breakdown_location")
        description = request.form.get("description", "")

        selected_booking = next((b for b in BOOKINGS if b["id"] == booking_id), None)
        vehicle_name = selected_booking["vehicle"] if selected_booking else "Unknown Vehicle"

        req_id = f"BRK-{len(BREAKDOWN_REQUESTS) + 501}"
        breakdown_obj = {
            "id": req_id,
            "booking_id": booking_id,
            "customer_name": session["customer_user"]["name"],
            "customer_email": current_email,
            "customer_phone": session["customer_user"]["phone"],
            "vehicle": vehicle_name,
            "issue": issue_type,
            "location": location,
            "description": description,
            "status": "Pending Dispatch",
            "admin_reply": ""
        }
        BREAKDOWN_REQUESTS.append(breakdown_obj)

        sos_msg = f"EMERGENCY SOS: Breakdown for {vehicle_name} (Booking {booking_id}). Issue: {issue_type} at {location}."
        session["last_breakdown_msg"] = sos_msg

        flash("Emergency assistance request sent to admin successfully!")
        return redirect(url_for("my_bookings"))

    return render_template_string(HTML_LAYOUT, page="breakdown_request", title="Roadside Breakdown Support", owner=OWNER_INFO, my_bookings=user_bookings)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("customer_user"):
        flash("Please log out from Customer account first.")
        return redirect(url_for("home"))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email == ADMIN_USER["email"] and check_password_hash(ADMIN_USER["password_hash"], password):
            session["admin_logged_in"] = True
            flash("Logged in as Administrator.")
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Invalid admin credentials.")

    return render_template_string(HTML_LAYOUT, page="login", title="Admin Login", owner=OWNER_INFO)

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("Admin logged out successfully.")
    return redirect(url_for("landing_page"))

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        flash("Admin access required.")
        return redirect(url_for("admin_login"))

    total_revenue = sum(b.get("total_cost", 0) for b in BOOKINGS if b.get("status") == "Confirmed")

    return render_template_string(HTML_LAYOUT, page="dashboard", title="Admin Control Dashboard", owner=OWNER_INFO, bookings=BOOKINGS, breakdowns=BREAKDOWN_REQUESTS, total_bookings=len(BOOKINGS), total_breakdowns=len(BREAKDOWN_REQUESTS), total_revenue=total_revenue)

@app.route("/admin/booking/action/<booking_id>/<action>")
def admin_booking_action(booking_id, action):
    if not session.get("admin_logged_in"):
        flash("Admin access required.")
        return redirect(url_for("admin_login"))

    for b in BOOKINGS:
        if b["id"] == booking_id:
            if action == "confirm":
                b["status"] = "Confirmed"
                flash(f"Booking {booking_id} has been Confirmed.")
            elif action == "reject":
                b["status"] = "Rejected"
                flash(f"Booking {booking_id} has been Rejected.")
            break
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/breakdown/reply", methods=["POST"])
def admin_breakdown_reply():
    if not session.get("admin_logged_in"):
        flash("Admin access required.")
        return redirect(url_for("admin_login"))

    breakdown_id = request.form.get("breakdown_id")
    reply_text = request.form.get("reply_text")

    for br in BREAKDOWN_REQUESTS:
        if br["id"] == breakdown_id:
            br["admin_reply"] = reply_text
            br["status"] = "Mechanic Dispatched"
            flash(f"Reply sent for breakdown request {breakdown_id}.")
            break

    return redirect(url_for("admin_dashboard"))

@app.route("/admin/bank-payments", methods=["GET", "POST"])
def admin_bank():
    global ADMIN_BANK_INFO
    if not session.get("admin_logged_in"):
        flash("Admin access required.")
        return redirect(url_for("admin_login"))

    if request.method == "POST":
        ADMIN_BANK_INFO = {
            "account_name": request.form.get("account_name"),
            "bank_name": request.form.get("bank_name"),
            "account_number": request.form.get("account_number"),
            "ifsc_code": request.form.get("ifsc_code"),
            "upi_id": request.form.get("upi_id"),
        }
        flash("Bank and withdrawal information updated successfully!")
        return redirect(url_for("admin_bank"))

    return render_template_string(HTML_LAYOUT, page="admin_bank", title="Bank & Payment Settings", owner=OWNER_INFO, bank_info=ADMIN_BANK_INFO)

@app.route("/contact")
def contact():
    return render_template_string(HTML_LAYOUT, page="contact", title="24/7 Contact Us", owner=OWNER_INFO)

if __name__ == "__main__":
    app.run(debug=True, port=5000)

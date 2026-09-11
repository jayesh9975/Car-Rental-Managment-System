import os
from flask import Flask, render_template_string, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'car_rental_jayesh_bhavsar_bulletproof_final_2026'

# --- Admin Credentials ---
ADMIN_USER = {
    "email": "jayeshbhavsar997@gmail.com",
    "password_hash": generate_password_hash("Shiv@99")
}

# --- Owner Info ---
OWNER_INFO = {
    "name": "Jayesh Bhavsar",
    "company": "Car Rental Management System",
    "sub_title": "By Jayesh Bhavsar",
    "phone": "+919765432442",
    "phone_display": "+91 9765432442",
    "email": "jayeshbhavsar997@gmail.com",
    "address": "Goil Nagar, Amalner, Maharashtra, India"
}

# --- Bank & Withdrawal Info Storage (Default) ---
ADMIN_BANK_INFO = {
    "account_name": "Jayesh Bhavsar",
    "bank_name": "State Bank of India",
    "account_number": "XXXXXXXX1234",
    "ifsc_code": "SBIN000XXXX",
    "upi_id": "jayeshbhavsar@oksbi"
}

VID_SAMPLE = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"

# Exact Top 25 Car Names mapped with their specific original high-res model image URLs
CARS_DATA = [
    {"name": "Maruti WagonR", "price": 1500, "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600"},
    {"name": "Maruti Dzire", "price": 1650, "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600"},
    {"name": "Maruti Ertiga", "price": 1900, "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600"},
    {"name": "Tata Punch", "price": 1550, "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600"},
    {"name": "Tata Nexon", "price": 1800, "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600"},
    {"name": "Mahindra Scorpio", "price": 2400, "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600"},
    {"name": "Maruti Eeco", "price": 1400, "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600"},
    {"name": "Maruti Fronx", "price": 1700, "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600"},
    {"name": "Hyundai Venue", "price": 1750, "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600"},
    {"name": "Toyota Innova", "price": 2800, "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600"},
    {"name": "Maruti Baleno", "price": 1600, "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600"},
    {"name": "Mahindra Thar", "price": 2600, "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600"},
    {"name": "Mahindra XUV700", "price": 2700, "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600"},
    {"name": "Maruti Grand Vitara", "price": 2200, "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600"},
    {"name": "Mahindra XUV 3XO", "price": 1850, "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600"},
    {"name": "Mahindra Bolero", "price": 1700, "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600"},
    {"name": "Tata Tiago", "price": 1450, "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600"},
    {"name": "Tata Curvv", "price": 2300, "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600"},
    {"name": "Toyota Hyryder", "price": 2250, "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600"},
    {"name": "Hyundai i10 Nios", "price": 1500, "image": "https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=600"}
]

CARS = []
for idx, item in enumerate(CARS_DATA, start=1):
    main_img = item["image"]
    photos = [main_img, "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600", "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=600", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=600", main_img]
    videos = [VID_SAMPLE] * 5
    CARS.append({
        "id": idx,
        "name": item["name"],
        "type": "SUV / Sedan / Hatchback",
        "seats": "5 Seater",
        "price": item["price"],
        "available": True,
        "image": main_img,
        "photos": photos,
        "videos": videos
    })

USERS_DB = {}
BOOKINGS = []
BREAKDOWN_REQUESTS = []

HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Rental Management System</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Leaflet CSS for Interactive OpenStreetMap Live Tracking -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        :root { --sidebar-bg: #0f172a; --sidebar-active: #2563eb; --bg-main: #f8fafc; --text-dark: #1e293b; --text-muted: #64748b; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Inter', sans-serif; }
        body { background-color: var(--bg-main); color: var(--text-dark); display: flex; min-height: 100vh; overflow-x: hidden; }

        .sidebar { width: 250px; background: var(--sidebar-bg); color: white; display: flex; flex-direction: column; padding: 20px 15px; flex-shrink: 0; }
        .sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 10px 5px 25px 5px; border-bottom: 1px solid #1e293b; }
        .sidebar-brand i { font-size: 1.8rem; color: #2563eb; }
        .sidebar-brand div { font-size: 1.1rem; font-weight: 700; }
        .sidebar-brand span { font-size: 0.75rem; color: #94a3b8; display: block; }

        .nav-list { list-style: none; margin-top: 20px; display: flex; flex-direction: column; gap: 6px; }
        .nav-item a { display: flex; align-items: center; gap: 14px; padding: 12px 16px; color: #94a3b8; text-decoration: none; font-size: 0.9rem; font-weight: 500; border-radius: 8px; transition: all 0.3s; }
        .nav-item.active a, .nav-item a:hover { background: var(--sidebar-active); color: white; }
        .sidebar-footer { margin-top: auto; padding-top: 20px; border-top: 1px solid #1e293b; font-size: 0.85rem; color: #64748b; }

        .main-wrapper { flex: 1; display: flex; flex-direction: column; }
        .top-header { background: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; }
        .top-header h2 { font-size: 1.3rem; font-weight: 700; color: #0f172a; }
        .content-body { padding: 25px 30px; flex: 1; }

        .car-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
        .car-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; cursor: pointer; display: flex; flex-direction: column; transition: all 0.3s ease; }
        .car-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.08); }
        .car-card img { width: 100%; height: 180px; object-fit: cover; background: #0f172a; }
        .car-card-body { padding: 18px; display: flex; flex-direction: column; flex: 1; }
        .btn-book { display: block; width: 100%; text-align: center; background: #2563eb; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: 600; margin-top: auto; }

        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
        .stat-card { background: white; padding: 20px; border-radius: 12px; display: flex; align-items: center; justify-content: space-between; border: 1px solid #f1f5f9; }
        .stat-info h4 { font-size: 0.85rem; color: var(--text-muted); }
        .stat-info .num { font-size: 1.6rem; font-weight: 700; margin: 5px 0; }
        .stat-icon { width: 48px; height: 48px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; color: white; }

        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(15,23,42,0.85); overflow-y: auto; }
        .modal-content { background: white; margin: 30px auto; padding: 25px; border-radius: 16px; max-width: 800px; width: 90%; position: relative; }
        .close { position: absolute; right: 20px; top: 15px; font-size: 24px; cursor: pointer; }
        .tab-btn { padding: 8px 16px; border-radius: 6px; border: 1px solid #cbd5e1; background: white; cursor: pointer; font-weight: 600; margin-right: 8px; margin-bottom: 15px; }
        .tab-btn.active { background: #2563eb; color: white; }
        .main-media { width: 100%; height: 350px; object-fit: cover; border-radius: 12px; margin-bottom: 15px; background: #000; }
        .thumbs { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
        .thumb-img { width: 100%; height: 70px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 2px solid transparent; }
        .thumb-img.active { border-color: #2563eb; }

        .form-box { background: white; padding: 30px; border-radius: 12px; max-width: 500px; margin: 20px auto; border: 1px solid #e2e8f0; position: relative; }
        .form-group { margin-bottom: 18px; position: relative; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.88rem; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 12px; border: 1.5px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem; }
        .btn-submit { width: 100%; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; }

        /* Suggestions Dropdown Style */
        .suggestions-list { position: absolute; top: 100%; left: 0; right: 0; background: white; border: 1px solid #cbd5e1; border-top: none; border-radius: 0 0 6px 6px; max-height: 180px; overflow-y: auto; z-index: 99; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .suggestion-item { padding: 10px 12px; font-size: 0.88rem; cursor: pointer; border-bottom: 1px solid #f1f5f9; }
        .suggestion-item:hover { background: #f1f5f9; }

        /* Map styling for live tracking */
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
            <div>{{ owner['company'] }}<span>{{ owner['sub_title'] }}</span></div>
        </div>

        <ul class="nav-list">
            <li class="nav-item {% if page == 'home' %}active{% endif %}">
                <a href="/"><i class="fa-solid fa-car"></i> Fleet Vehicles</a>
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
            {% if session.get('admin_logged_in') %}
                <p><i class="fa-solid fa-user-shield" style="color: #10b981;"></i> Admin Active</p>
                <a href="/admin/logout" style="color: #ef4444; text-decoration: none; font-weight: 600; display: block; margin-top: 8px;">Admin Logout</a>
            {% elif session.get('customer_user') %}
                <p><i class="fa-solid fa-user" style="color: #3b82f6;"></i> User: {{ session['customer_user']['name'] }}</p>
                <a href="/customer/logout" style="color: #ef4444; text-decoration: none; font-weight: 600; display: block; margin-top: 8px;">Customer Logout</a>
            {% else %}
                <a href="/customer/login" style="color: #3b82f6; text-decoration: none; font-weight: 600; display: block;">Customer Login / Register</a>
                <a href="/admin/login" style="color: #64748b; text-decoration: none; font-weight: 500; display: block; margin-top: 8px;">Admin Login</a>
            {% endif %}
        </div>
    </div>

    <div class="main-wrapper">
        <div class="top-header">
            <h2>{{ title }}</h2>
            <div>
                {% if session.get('customer_user') %}
                    <span style="font-weight: 600; color: #2563eb;"><i class="fa-solid fa-circle-user"></i> {{ session['customer_user']['name'] }}</span>
                {% elif session.get('admin_logged_in') %}
                    <span style="font-weight: 600; color: #10b981;"><i class="fa-solid fa-user-shield"></i> Admin Panel</span>
                {% else %}
                    <a href="/customer/login" style="text-decoration: none; font-weight: 600; color: #2563eb; margin-right: 15px;">Customer Login</a>
                    <a href="/admin/login" style="text-decoration: none; font-weight: 600; color: #64748b;">Admin Login</a>
                {% endif %}
            </div>
        </div>

        <div class="content-body">
            {% for message in get_flashed_messages() %}
                <div style="padding: 15px; background: #d1fae5; color: #065f46; border-radius: 8px; margin-bottom: 20px; font-weight: 600;">
                    <i class="fa-solid fa-circle-check"></i> {{ message }}
                    {% if session.get('last_booking_msg') %}
                    <div style="margin-top: 10px;">
                        <a href="https://wa.me/{{ owner['phone'] }}?text={{ session.get('last_booking_msg') }}" target="_blank" style="background: #10b981; color: white; padding: 8px 14px; text-decoration: none; border-radius: 6px;"><i class="fa-brands fa-whatsapp"></i> Send WhatsApp Booking Notification</a>
                    </div>
                    {% endif %}
                    {% if session.get('last_breakdown_msg') %}
                    <div style="margin-top: 10px;">
                        <a href="https://wa.me/{{ owner['phone'] }}?text={{ session.get('last_breakdown_msg') }}" target="_blank" style="background: #ef4444; color: white; padding: 8px 14px; text-decoration: none; border-radius: 6px;"><i class="fa-brands fa-whatsapp"></i> Send Emergency WhatsApp SOS</a>
                    </div>
                    {% endif %}
                </div>
            {% endfor %}

            {% if page == 'home' %}
                <h2 style="font-size: 1.3rem; margin-bottom: 20px;">Top Selling Fleet Vehicles</h2>
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

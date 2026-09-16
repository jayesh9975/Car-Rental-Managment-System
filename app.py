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

        .form-box { background: white; padding: 30px; border-radius: 12px; max-width: 450px; margin: 20px auto; border: 1px solid #e2e8f0; }
        .form-group { margin-bottom: 18px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.88rem; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 12px; border: 1.5px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem; }
        .btn-submit { width: 100%; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; }

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
                    <h3 style="margin-bottom: 15px;">My Rental Bookings</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Booking ID</th>
                                <th>Vehicle</th>
                                <th>Pickup Location</th>
                                <th>Rental Days</th>
                                <th>Status</th>
                                <th>Amount Paid</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for b in my_bookings %}
                            <tr>
                                <td><b>{{ b['id'] }}</b></td>
                                <td>{{ b['vehicle'] }}</td>
                                <td>{{ b['location'] }}</td>
                                <td>{{ b['days'] }} Days</td>
                                <td><span style="background: #d1fae5; color: #065f46; padding: 4px 10px; border-radius: 12px; font-weight: 600;">Confirmed</span></td>
                                <td><b>₹ {{ b['amount'] }}</b></td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" style="text-align: center; color: #64748b; padding: 25px;">No active bookings found.</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

            {% elif page == 'breakdown_request' %}
                <div class="form-box" style="max-width: 550px;">
                    <h2 style="margin-bottom: 8px;"><i class="fa-solid fa-triangle-exclamation" style="color: #ef4444;"></i> Vehicle Breakdown Assistance</h2>
                    <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 20px;">Stranded or facing a mechanical problem? Send an instant emergency assistance request to support.</p>
                    <form method="POST">
                        <div class="form-group">
                            <label>Select Your Booking / Vehicle</label>
                            <select name="booking_id" required>
                                <option value="">-- Select Active Booking --</option>
                                {% for b in my_bookings %}
                                <option value="{{ b['id'] }}">{{ b['id'] }} - {{ b['vehicle'] }} (Location: {{ b['location'] }})</option>
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
                            <input type="text" name="breakdown_location" required placeholder="e.g., Near Bus Stand, Amalner / Highway NH-52">
                        </div>
                        <div class="form-group">
                            <label>Describe the Problem (Optional details)</label>
                            <textarea name="description" rows="3" placeholder="Provide extra details for quick mechanic assistance..."></textarea>
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
                            <div class="num">25</div>
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
                    <h3 style="margin-bottom: 15px;"><i class="fa-solid fa-triangle-exclamation" style="color: #ef4444;"></i> Vehicle Breakdown & Roadside Assistance Logs</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Request ID</th>
                                <th>Booking ID</th>
                                <th>Customer</th>
                                <th>Vehicle</th>
                                <th>Issue Type</th>
                                <th>Breakdown Location</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for br in breakdowns %}
                            <tr>
                                <td><b>{{ br['id'] }}</b></td>
                                <td>{{ br['booking_id'] }}</td>
                                <td>{{ br['customer_name'] }}</td>
                                <td>{{ br['vehicle'] }}</td>
                                <td><span style="background: #fee2e2; color: #991b1b; padding: 3px 8px; border-radius: 12px; font-weight: 600;">{{ br['issue'] }}</span></td>
                                <td>{{ br['location'] }}</td>
                                <td><span style="background: #fef3c7; color: #92400e; padding: 3px 8px; border-radius: 12px; font-weight: 600;">{{ br['status'] }}</span></td>
                            </tr>
                            {% else %}
                            <tr><td colspan="7" style="text-align: center; color: #64748b; padding: 20px;">No breakdown assistance requests recorded. (All vehicles running smoothly)</td></tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>

                <div class="table-card">
                    <h3 style="margin-bottom: 15px;">Recent Bookings</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Booking ID</th>
                                <th>Customer Name</th>
                                <th>Vehicle</th>
                                <th>Pickup Location</th>
                                <th>Status</th>
                                <th>Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for b in bookings %}
                            <tr>
                                <td><b>{{ b['id'] }}</b></td>
                                <td>{{ b['customer'] }}</td>
                                <td>{{ b['vehicle'] }}</td>
                                <td>{{ b['location'] }}</td>
                                <td><span style="background: #d1fae5; color: #065f46; padding: 3px 8px; border-radius: 12px; font-weight: 600;">Confirmed</span></td>
                                <td><b>₹ {{ b['amount'] }}</b></td>
                            </tr>
                            {% else %}
                            <tr><td colspan="6" style="text-align: center; color: #64748b; padding: 20px;">No bookings recorded yet. (Zero Bookings)</td></tr>
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
                            <input type="text" name="account_name" required value="{{ bank_info['account_name'] }}" placeholder="Jayesh Bhavsar">
                        </div>
                        <div class="form-group">
                            <label>Bank Name</label>
                            <input type="text" name="bank_name" required value="{{ bank_info['bank_name'] }}" placeholder="State Bank of India">
                        </div>
                        <div class="form-group">
                            <label>Account Number</label>
                            <input type="text" name="account_number" required value="{{ bank_info['account_number'] }}" placeholder="Enter Bank Account Number">
                        </div>
                        <div class="form-group">
                            <label>IFSC Code</label>
                            <input type="text" name="ifsc_code" required value="{{ bank_info['ifsc_code'] }}" placeholder="SBIN000XXXX">
                        </div>
                        <div class="form-group">
                            <label>UPI ID (For Instant Payouts)</label>
                            <input type="text" name="upi_id" required value="{{ bank_info['upi_id'] }}" placeholder="username@oksbi">
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
                <div class="form-box" style="max-width: 550px;">
                    <h2>Office Contact Info</h2>
                    <div style="margin-top: 15px; line-height: 1.8;">
                        <p><strong>Owner Name:</strong> {{ owner['name'] }}</p>
                        <p><strong>Mobile / WhatsApp:</strong> {{ owner['phone_display'] }}</p>
                        <p><strong>Official Email:</strong> {{ owner['email'] }}</p>
                        <p><strong>Office Address:</strong> {{ owner['address'] }}</p>
                    </div>
                </div>

            {% elif page == 'book' %}
                <div class="form-box">
                    <h2>Book {{ car['name'] }}</h2>
                    <p style="color: var(--text-muted); margin-bottom: 20px;">Rate: <strong>₹ {{ car['price'] }} / day</strong></p>
                    <form method="POST">
                        <div class="form-group">
                            <label>Customer Name</label>
                            <input type="text" name="customer_name" required value="{{ session.get('customer_user', {}).get('name', '') }}" placeholder="Rahul Patil">
                        </div>
                        <div class="form-group">
                            <label>Mobile Number</label>
                            <input type="tel" name="phone" required value="{{ session.get('customer_user', {}).get('phone', '') }}" placeholder="10-digit number">
                        </div>
                        <div class="form-group">
                            <label>Pickup Location / City</label>
                            <input type="text" name="location" required placeholder="e.g., Amalner, Goil Nagar / Railway Station">
                        </div>
                        <div class="form-group">
                            <label>Rental Start Date</label>
                            <input type="date" name="start_date" required>
                        </div>
                        <div class="form-group">
                            <label>Rental Days</label>
                            <input type="number" name="days" value="1" min="1" max="30" required>
                        </div>
                        <button type="submit" class="btn-submit">Confirm Booking</button>
                    </form>
                </div>
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

@app.route('/')
def home():
    return render_template_string(HTML_LAYOUT, page='home', title='Top Selling Fleet Vehicles', cars=CARS, owner=OWNER_INFO)

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    if request.method == 'POST':
        email = request.form.get('email')
        if email in USERS_DB:
            flash("Account with this email already exists! Please Login.")
            return redirect(url_for('customer_login'))

        USERS_DB[email] = {
            "name": request.form.get('name'),
            "phone": request.form.get('phone'),
            "license": request.form.get('license'),
            "email": email,
            "password_hash": generate_password_hash(request.form.get('password'))
        }
        flash("Customer Account Created Successfully! Please Login.")
        return redirect(url_for('customer_login'))

    return render_template_string(HTML_LAYOUT, page='customer_register', title='Customer Registration', owner=OWNER_INFO)

@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = USERS_DB.get(email)

        if user and check_password_hash(user['password_hash'], password):
            session['customer_user'] = {"email": user['email'], "name": user['name'], "phone": user['phone']}
            flash(f"Welcome back, {user['name']}!")
            return redirect(url_for('home'))
        else:
            flash("Invalid Customer Email or Password!")

    return render_template_string(HTML_LAYOUT, page='customer_login', title='Customer Login', owner=OWNER_INFO)

@app.route('/customer/my-bookings')
def my_bookings():
    if not session.get('customer_user'):
        flash("Please login to view your bookings!")
        return redirect(url_for('customer_login'))

    user_email = session['customer_user']['email']
    user_b = [b for b in BOOKINGS if b.get('customer_email') == user_email]
    return render_template_string(HTML_LAYOUT, page='my_bookings', title='My Bookings', my_bookings=user_b, owner=OWNER_INFO)

@app.route('/customer/breakdown', methods=['GET', 'POST'])
def customer_breakdown():
    if not session.get('customer_user'):
        flash("Please login to request breakdown assistance!")
        return redirect(url_for('customer_login'))

    user_email = session['customer_user']['email']
    user_b = [b for b in BOOKINGS if b.get('customer_email') == user_email]

    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        issue_type = request.form.get('issue_type')
        location = request.form.get('breakdown_location')
        description = request.form.get('description', '')

        selected_booking = next((b for b in BOOKINGS if b['id'] == booking_id), None)
        vehicle_name = selected_booking['vehicle'] if selected_booking else 'Unknown Vehicle'
        customer_name = session['customer_user']['name']
        customer_phone = session['customer_user']['phone']

        br_id = f"#BR{1000 + len(BREAKDOWN_REQUESTS) + 1}"
        BREAKDOWN_REQUESTS.append({
            "id": br_id,
            "booking_id": booking_id,
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "vehicle": vehicle_name,
            "issue": issue_type,
            "location": location,
            "description": description,
            "status": "Pending Dispatch"
        })

        wa_msg = f"🚨 EMERGENCY ROADWAY ASSISTANCE!\nReq ID: {br_id}\nBooking: {booking_id}\nVehicle: {vehicle_name}\nCustomer: {customer_name} ({customer_phone})\nIssue: {issue_type}\nLocation: {location}\nDesc: {description}"
        session['last_breakdown_msg'] = wa_msg
        flash("Breakdown SOS request registered successfully! Support team alerted.")
        return redirect(url_for('my_bookings'))

    return render_template_string(HTML_LAYOUT, page='breakdown_request', title='Vehicle Breakdown Assistance', my_bookings=user_b, owner=OWNER_INFO)

@app.route('/customer/logout')
def customer_logout():
    session.pop('customer_user', None)
    flash("Customer Logged Out Successfully!")
    return redirect(url_for('home'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email == ADMIN_USER['email'] and check_password_hash(ADMIN_USER['password_hash'], password):
            session['admin_logged_in'] = ADMIN_USER['email']
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin Email or Password!")
    return render_template_string(HTML_LAYOUT, page='login', title='Admin Login', owner=OWNER_INFO)

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        flash("Please login to access Admin Dashboard!")
        return redirect(url_for('admin_login'))

    total_rev = sum(b['amount'] for b in BOOKINGS)
    return render_template_string(
        HTML_LAYOUT,
        page='dashboard',
        title='Admin Dashboard',
        bookings=BOOKINGS,
        breakdowns=BREAKDOWN_REQUESTS,
        total_bookings=len(BOOKINGS),
        total_customers=len(USERS_DB),
        total_breakdowns=len(BREAKDOWN_REQUESTS),
        total_revenue=total_rev,
        owner=OWNER_INFO
    )

@app.route('/admin/bank-payments', methods=['GET', 'POST'])
def admin_bank_payments():
    global ADMIN_BANK_INFO
    if not session.get('admin_logged_in'):
        flash("Please login to access Bank & Payments settings!")
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        ADMIN_BANK_INFO = {
            "account_name": request.form.get('account_name'),
            "bank_name": request.form.get('bank_name'),
            "account_number": request.form.get('account_number'),
            "ifsc_code": request.form.get('ifsc_code'),
            "upi_id": request.form.get('upi_id')
        }
        flash("Owner Bank and Withdrawal details updated successfully!")
        return redirect(url_for('admin_bank_payments'))

    return render_template_string(
        HTML_LAYOUT,
        page='admin_bank',
        title='Admin Bank & Payments',
        bank_info=ADMIN_BANK_INFO,
        owner=OWNER_INFO
    )

@app.route('/contact')
def contact():
    return render_template_string(HTML_LAYOUT, page='contact', title='Contact Details', owner=OWNER_INFO)

@app.route('/book/<int:car_id>', methods=['GET', 'POST'])
def book_car(car_id):
    car = next((c for c in CARS if c['id'] == car_id), None)
    if request.method == 'POST':
        c_name = request.form.get('customer_name')
        c_phone = request.form.get('phone')
        location = request.form.get('location')
        days = int(request.form.get('days', 1))
        amount = days * car['price']

        b_id = f"#BK{1000 + len(BOOKINGS) + 1}"
        c_email = session.get('customer_user', {}).get('email', 'guest')

        BOOKINGS.append({
            "id": b_id,
            "customer": c_name,
            "customer_email": c_email,
            "vehicle": car['name'],
            "location": location,
            "days": days,
            "amount": amount
        })

        wa_msg = f"New Ride Booking!\nID: {b_id}\nVehicle: {car['name']}\nCustomer: {c_name}\nPhone: {c_phone}\nPickup Location: {location}\nTotal: ₹{amount}"
        session['last_booking_msg'] = wa_msg
        flash(f"Booking confirmed for {car['name']}! Total: ₹{amount}")
        return redirect(url_for('home'))

    return render_template_string(HTML_LAYOUT, page='book', title='Book Vehicle', car=car, owner=OWNER_INFO)

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash("Admin Logged Out Successfully!")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

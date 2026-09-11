import os
from flask import Flask, render_template_string, request, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Resolve static assets relative to this file so thumbnails work under
# Gunicorn even when the process is started from a different working folder.
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"), static_url_path="/static")
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
    {"name": "Maruti WagonR", "price": 1500, "type": "Hatchback", "seats": "5 Seater", "image": "maruti_wagonr.jpg"},
    {"name": "Maruti Dzire", "price": 1650, "type": "Sedan", "seats": "5 Seater", "image": "maruti_dzire.jpg"},
    {"name": "Maruti Ertiga", "price": 1900, "type": "MUV / SUV", "seats": "7 Seater", "image": "maruti_ertiga.jpg"},
    {"name": "Tata Punch", "price": 1550, "type": "Mini SUV", "seats": "5 Seater", "image": "tata_punch.jpg"},
    {"name": "Tata Nexon", "price": 1800, "type": "Compact SUV", "seats": "5 Seater", "image": "tata_nexon.jpg"},
    {"name": "Mahindra Scorpio", "price": 2400, "type": "SUV", "seats": "7 Seater", "image": "mahindra_scorpio.jpg"},
    {"name": "Maruti Eeco", "price": 1400, "type": "Van / Multi-utility", "seats": "7 Seater", "image": "maruti_eeco.jpg"},
    {"name": "Maruti Fronx", "price": 1700, "type": "Crossover SUV", "seats": "5 Seater", "image": "maruti_fronx.jpg"},
    {"name": "Hyundai Venue", "price": 1750, "type": "Compact SUV", "seats": "5 Seater", "image": "hyundai_venue.jpg"},
    {"name": "Toyota Innova", "price": 2800, "type": "Premium MUV", "seats": "7 Seater", "image": "toyota_innova.jpg"},
    {"name": "Maruti Baleno", "price": 1600, "type": "Premium Hatchback", "seats": "5 Seater", "image": "maruti_suzuki_baleno.jpg"},
    {"name": "Mahindra Thar", "price": 2600, "type": "Off-road SUV", "seats": "4 Seater", "image": "mahindra_thar.jpg"},
    {"name": "Mahindra XUV700", "price": 2700, "type": "Luxury SUV", "seats": "7 Seater", "image": "mahindra_xuv700.jpg"},
    {"name": "Maruti Grand Vitara", "price": 2200, "type": "Hybrid SUV", "seats": "5 Seater", "image": "maruti_suzuki_grand_vitara.jpg"},
    {"name": "Mahindra XUV 3XO", "price": 1850, "type": "Compact SUV", "seats": "5 Seater", "image": "mahindra_xuv_3xo.jpg"},
    {"name": "Mahindra Bolero", "price": 1700, "type": "Rugged SUV", "seats": "7 Seater", "image": "mahindra_bolero.jpg"},
    {"name": "Tata Tiago", "price": 1450, "type": "Hatchback", "seats": "5 Seater", "image": "tata_tiago.jpg"},
    {"name": "Tata Curvv", "price": 2300, "type": "Coupe SUV", "seats": "5 Seater", "image": "tata_curvv.jpg"},
    {"name": "Toyota Hyryder", "price": 2250, "type": "Hybrid SUV", "seats": "5 Seater", "image": "toyota_hyryder.jpg"},
    {"name": "Hyundai i10 Nios", "price": 1500, "type": "City Hatchback", "seats": "5 Seater", "image": "hyundai_grand_i10_nios.jpg"}
]

CARS = []
for idx, item in enumerate(CARS_DATA, start=1):
    img_name = item["image"]
    # Direct access path for car thumbnails inside static/car_thumbnails/
    main_img = f"/car-thumb/{img_name}"
    
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
    </style>
</head>
<body>
    <nav>
        <a href="/" class="logo-box">
            <div class="logo-icon-wrap"><i class="fa-solid fa-car-side"></i></div>
            <div class="logo-text"><h2>JAY'S CARS</h2><span>Car Rental Management System</span></div>
        </a>
        <div class="nav-links">
            <a href="/home" class="btn-primary-land"><i class="fa-solid fa-compass"></i> Open App / Fleet</a>
        </div>
    </nav>
    <section class="hero">
        <div class="hero-left">
            <div class="badge"><i class="fa-solid fa-bolt"></i> Maharashtra's Premier Mobility Platform</div>
            <h1>Smart, Safe & Seamless <span>Car Rental Management System</span></h1>
            <p>Experience ultra-modern travel with verified fleet vehicles and 24/7 support managed by Jayesh Bhavsar.</p>
            <div class="hero-btns"><a href="/home" class="cta-main">Explore Fleet Now <i class="fa-solid fa-arrow-right"></i></a></div>
        </div>
    </section>
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

        .sidebar { width: 250px; background: var(--sidebar-bg); color: white; display: flex; flex-direction: column; padding: 20px 15px; flex-shrink: 0; }
        .sidebar-brand { display: flex; align-items: center; gap: 12px; padding: 10px 5px 25px 5px; border-bottom: 1px solid #1e293b; }
        .sidebar-brand i { font-size: 1.8rem; color: #2563eb; }
        .sidebar-brand div { font-size: 1.1rem; font-weight: 700; }
        .sidebar-brand span { font-size: 0.75rem; color: #94a3b8; display: block; }

        .nav-list { list-style: none; margin-top: 10px; display: flex; flex-direction: column; gap: 6px; }
        .nav-item a { display: flex; align-items: center; gap: 14px; padding: 12px 16px; color: #94a3b8; text-decoration: none; font-size: 0.9rem; font-weight: 500; border-radius: 8px; transition: all 0.3s ease; }
        .nav-item.active a, .nav-item a:hover { background: var(--sidebar-active); color: white; transform: translateX(4px); }

        .main-wrapper { flex: 1; display: flex; flex-direction: column; }
        .top-header { background: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; }
        .content-body { padding: 25px 30px; flex: 1; }

        .car-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
        .car-card { background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; cursor: pointer; display: flex; flex-direction: column; transition: all 0.35s ease; }
        .car-card:hover { transform: translateY(-6px); box-shadow: 0 12px 24px rgba(0,0,0,0.1); }
        .car-card .car-thumb { position: relative; height: 180px; overflow: hidden; background: #ffffff; border-bottom: 1px solid #f1f5f9; }
        .car-card .car-thumb img { width: 100%; height: 100%; object-fit: cover; background: #ffffff; }
        .car-card-body { padding: 18px; display: flex; flex-direction: column; flex: 1; }
        .btn-book { display: block; width: 100%; text-align: center; background: #2563eb; color: white; padding: 10px; border-radius: 6px; text-decoration: none; font-weight: 600; margin-top: auto; }
        .btn-book:hover { background: #1d4ed8; }

        .modal { display: none; position: fixed; z-index: 1000; left: 0; top: 0; width: 100%; height: 100%; background: rgba(15,23,42,0.85); overflow-y: auto; }
        .modal-content { background: white; margin: 30px auto; padding: 25px; border-radius: 16px; max-width: 800px; width: 90%; position: relative; }
        .close { position: absolute; right: 20px; top: 15px; font-size: 24px; cursor: pointer; }
        .main-media { width: 100%; height: 350px; object-fit: cover; border-radius: 12px; margin-bottom: 15px; border: 1px solid #e2e8f0; }
        .thumbs { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
        .thumb-img { width: 100%; height: 70px; object-fit: cover; border-radius: 8px; cursor: pointer; border: 2px solid transparent; }
        .thumb-img.active { border-color: #2563eb; }

        .form-box { background: white; padding: 30px; border-radius: 12px; max-width: 500px; margin: 20px auto; border: 1px solid #e2e8f0; }
        .form-group { margin-bottom: 18px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.88rem; }
        .form-group input, .form-group select, .form-group textarea { width: 100%; padding: 10px 12px; border: 1.5px solid #cbd5e1; border-radius: 6px; }
        .btn-submit { width: 100%; padding: 12px; background: #2563eb; color: white; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-brand">
            <i class="fa-solid fa-car-side"></i>
            <div>JAY'S CARS<span>Management System</span></div>
        </div>
        <ul class="nav-list">
            <li class="nav-item"><a href="/"><i class="fa-solid fa-globe"></i> Landing Page</a></li>
            <li class="nav-item {% if page == 'home' %}active{% endif %}"><a href="/home"><i class="fa-solid fa-house"></i> Home & Fleet</a></li>
            <li class="nav-item {% if page == 'dashboard' %}active{% endif %}"><a href="/admin/dashboard"><i class="fa-solid fa-gauge"></i> Admin Dashboard</a></li>
        </ul>
    </div>
    <div class="main-wrapper">
        <div class="top-header">
            <h2>{{ title }}</h2>
            <div>
                {% if session.get('customer_user') %}
                    <span>{{ session['customer_user']['name'] }}</span> | <a href="/customer/logout" style="color: #ef4444;">Logout</a>
                {% else %}
                    <a href="/customer/login" style="color: #2563eb;">Login</a>
                {% endif %}
            </div>
        </div>
        <div class="content-body">
            {% for message in get_flashed_messages() %}
                <div style="padding: 15px; background: #d1fae5; color: #065f46; border-radius: 8px; margin-bottom: 20px; font-weight: 600;">
                    <i class="fa-solid fa-circle-check"></i> {{ message }}
                </div>
            {% endfor %}

            {% if page == 'home' %}
                <div style="margin-bottom: 15px;"><h2>Top Selling Fleet Vehicles</h2></div>
                <div class="car-grid">
                    {% for car in cars %}
                    <div class="car-card" onclick="openModal('{{ car['name'] }}', {{ car['photos']|tojson }})">
                        <div class="car-thumb"><img src="{{ car['image'] }}" alt="{{ car['name'] }}"></div>
                        <div class="car-card-body">
                            <h3>{{ car['name'] }}</h3>
                            <p style="color: #64748b; font-size: 0.85rem; margin: 5px 0;">{{ car['type'] }} | {{ car['seats'] }}</p>
                            <div style="font-size: 1.2rem; font-weight: 700; color: #2563eb; margin: 8px 0;">₹{{ car['price'] }} / day</div>
                            <div onclick="event.stopPropagation();"><a href="/book/{{ car['id'] }}" class="btn-book">Book Vehicle</a></div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
                <div id="galleryModal" class="modal">
                    <div class="modal-content">
                        <span class="close" onclick="closeModal()">&times;</span>
                        <h3 id="modalName">Vehicle Gallery</h3>
                        <img id="mainImg" class="main-media" src="" alt="Main Image">
                        <div class="thumbs" id="thumbsContainer"></div>
                    </div>
                </div>
            {% elif page == 'customer_login' %}
                <div class="form-box">
                    <h2>Customer Sign In</h2>
                    <form method="POST">
                        <div class="form-group"><label>Email</label><input type="email" name="email" required></div>
                        <div class="form-group"><label>Password</label><input type="password" name="password" required></div>
                        <button type="submit" class="btn-submit">Sign In</button>
                    </form>
                </div>
            {% elif page == 'book' %}
                <div class="form-box">
                    <h2>Book {{ car['name'] }}</h2>
                    <form method="POST">
                        <div class="form-group"><label>Customer Name</label><input type="text" name="customer_name" required></div>
                        <div class="form-group"><label>Phone</label><input type="tel" name="phone" required></div>
                        <div class="form-group"><label>Pickup Location</label><input type="text" name="start_location" required></div>
                        <div class="form-group"><label>Drop Location</label><input type="text" name="end_location" required></div>
                        <div class="form-group"><label>Days</label><input type="number" name="days" value="1" min="1" required></div>
                        <button type="submit" class="btn-submit">Confirm Booking</button>
                    </form>
                </div>
            {% elif page == 'dashboard' %}
                <div style="background: white; padding: 20px; border-radius: 12px;">
                    <h3>Admin Dashboard - Total Bookings: {{ total_bookings }} | Revenue: ₹{{ total_revenue }}</h3>
                </div>
            {% endif %}
        </div>
    </div>
    <script>
        function openModal(name, photos) {
            document.getElementById('modalName').innerText = name + " Gallery";
            document.getElementById('mainImg').src = photos[0];
            var thumbs = document.getElementById('thumbsContainer');
            thumbs.innerHTML = '';
            photos.forEach((src, idx) => {
                var t = document.createElement('img');
                t.src = src;
                t.className = 'thumb-img' + (idx === 0 ? ' active' : '');
                t.onclick = () => { document.getElementById('mainImg').src = src; };
                thumbs.appendChild(t);
            });
            document.getElementById('galleryModal').style.display = "block";
        }
        function closeModal() { document.getElementById('galleryModal').style.display = "none"; }
    </script>
</body>
</html>
"""

# --- Flask Routes ---
@app.route("/")
def landing_page():
    return render_template_string(LANDING_TEMPLATE)

@app.route("/car-thumb/<path:filename>")
def car_thumbnail(filename):
    """Explicit route to serve files directly from static/car_thumbnails/"""
    return send_from_directory(os.path.join(app.static_folder, "car_thumbnails"), filename)

@app.route("/home")
def home():
    return render_template_string(HTML_LAYOUT, page="home", title="Home & Fleet", owner=OWNER_INFO, cars=CARS)

@app.route("/customer/login", methods=["GET", "POST"])
def customer_login():
    if request.method == "POST":
        email = request.form.get("email")
        session["customer_user"] = {"name": "Customer", "email": email}
        return redirect(url_for("home"))
    return render_template_string(HTML_LAYOUT, page="customer_login", title="Customer Sign In", owner=OWNER_INFO)

@app.route("/customer/logout")
def customer_logout():
    session.pop("customer_user", None)
    return redirect(url_for("landing_page"))

@app.route("/book/<int:car_id>", methods=["GET", "POST"])
def book_car(car_id):
    car = next((c for c in CARS if c["id"] == car_id), None)
    if request.method == "POST":
        booking_id = f"BK-{len(BOOKINGS) + 1001}"
        BOOKINGS.append({
            "id": booking_id,
            "customer": request.form.get("customer_name"),
            "vehicle": car["name"],
            "total_cost": int(request.form.get("days", 1)) * car["price"],
            "status": "Confirmed"
        })
        flash(f"Booking {booking_id} confirmed!")
        return redirect(url_for("home"))
    return render_template_string(HTML_LAYOUT, page="book", title=f"Book {car['name']}", owner=OWNER_INFO, car=car)

@app.route("/admin/dashboard")
def admin_dashboard():
    return render_template_string(HTML_LAYOUT, page="dashboard", title="Admin Dashboard", owner=OWNER_INFO, total_bookings=len(BOOKINGS), total_revenue=sum(b["total_cost"] for b in BOOKINGS))

if __name__ == "__main__":
    app.run(debug=True, port=5000)

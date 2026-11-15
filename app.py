import json
import urllib.parse
from pathlib import Path
from datetime import date

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
CONFIG_FILE = APP_DIR / "saved_filters.json"

DEFAULTS = {
    "keywords": "",
    "make": "",
    "model": "",
    "year_from": 2005,
    "year_to": 2018,
    "engine_min": 0.9,
    "engine_max": 2.5,
    "fuel": "Petrol",
    "transmission": "Manual",
    "max_price": 2000,
    "max_miles": 100000,
    "postcode": "London",
    "radius": 50,
    "condition": "Any",
}

FUEL_OPTIONS = ["Any", "Petrol", "Diesel", "Hybrid", "Electric", "LPG"]
GEARBOX_OPTIONS = ["Any", "Manual", "Automatic"]
CONDITION_OPTIONS = ["Any", "Used", "Non-runner / spares or repairs"]

def load_saved():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}

def save_saved(data):
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

def clean(value):
    return str(value or "").strip()

def build_query(f):
    bits = []
    for key in ("make", "model", "keywords"):
        if clean(f.get(key)):
            bits.append(clean(f[key]))
    if f.get("fuel") and f["fuel"] != "Any":
        bits.append(f["fuel"])
    if f.get("transmission") and f["transmission"] != "Any":
        bits.append(f["transmission"])
    if f.get("engine_min") and f.get("engine_max"):
        bits.append(f'{f["engine_min"]:.1f}L-{f["engine_max"]:.1f}L')
    return " ".join(bits) or "used cars"

def ebay_url(f):
    q = urllib.parse.quote_plus(build_query(f))
    params = {
        "_nkw": build_query(f),
        "_udhi": int(f["max_price"]),
        "_sacat": "9801",
        "_sop": "10",
    }
    return "https://www.ebay.co.uk/sch/i.html?" + urllib.parse.urlencode(params)

def gumtree_url(f):
    params = {
        "q": build_query(f),
        "search_category": "cars",
        "max_price": int(f["max_price"]),
    }
    return "https://www.gumtree.com/search?" + urllib.parse.urlencode(params)

def facebook_url(f):
    q = urllib.parse.quote(build_query(f))
    return f'https://www.facebook.com/marketplace/{urllib.parse.quote(f["postcode"])}/search/?query={q}'

def pounds(n):
    return f"£{n:,.0f}"

st.set_page_config(page_title="Car Finder Pro", page_icon="🚗", layout="wide")
st.title("🚗 Car Finder Pro")
st.caption("Flexible marketplace searches, saved filters, deal calculator and a vehicle-risk worksheet.")

saved = load_saved()
settings = {**DEFAULTS, **saved}

with st.sidebar:
    st.header("1. Search filters")
    st.caption("Leave a field blank or choose Any when you don't want to restrict it.")
    make = st.text_input("Make", value=settings["make"], placeholder="e.g. Toyota")
    model = st.text_input("Model", value=settings["model"], placeholder="e.g. Auris")
    keywords = st.text_input("Extra keywords", value=settings["keywords"], placeholder="e.g. 1.6 VVT-i, full history")
    a, b = st.columns(2)
    with a:
        year_from = st.number_input("Year from", min_value=1980, max_value= date.today().year + 1, value=int(settings["year_from"]), step=1)
    with b:
        year_to = st.number_input("Year to", min_value=1980, max_value=date.today().year + 1, value=int(settings["year_to"]), step=1)
    a, b = st.columns(2)
    with a:
        engine_min = st.number_input("Engine min (L)", min_value=0.0, max_value=10.0, value=float(settings["engine_min"]), step=0.1, format="%.1f")
    with b:
        engine_max = st.number_input("Engine max (L)", min_value=0.0, max_value=10.0, value=float(settings["engine_max"]), step=0.1, format="%.1f")
    fuel = st.selectbox("Fuel", FUEL_OPTIONS, index=FUEL_OPTIONS.index(settings["fuel"]) if settings["fuel"] in FUEL_OPTIONS else 0)
    transmission = st.selectbox("Transmission", GEARBOX_OPTIONS, index=GEARBOX_OPTIONS.index(settings["transmission"]) if settings["transmission"] in GEARBOX_OPTIONS else 0)
    condition = st.selectbox("Condition", CONDITION_OPTIONS, index=CONDITION_OPTIONS.index(settings["condition"]) if settings["condition"] in CONDITION_OPTIONS else 0)
    max_price = st.number_input("Maximum price (£)", min_value=0, max_value=200000, value=int(settings["max_price"]), step=100)
    max_miles = st.number_input("Maximum mileage", min_value=0, max_value=500000, value=int(settings["max_miles"]), step=5000)
    postcode = st.text_input("Search location / town / postcode", value=settings["postcode"])
    radius = st.selectbox("Radius (miles)", [5, 10, 25, 50, 75, 100, 150, 200], index=[5,10,25,50,75,100,150,200].index(int(settings["radius"])) if int(settings["radius"]) in [5,10,25,50,75,100,150,200] else 3)

    filters = {
        "make": make, "model": model, "keywords": keywords,
        "year_from": int(year_from), "year_to": int(year_to),
        "engine_min": float(engine_min), "engine_max": float(engine_max),
        "fuel": fuel, "transmission": transmission, "condition": condition,
        "max_price": int(max_price), "max_miles": int(max_miles),
        "postcode": postcode, "radius": int(radius),
    }
    c1, c2 = st.columns(2)
    with c1:
        if st.button("💾 Save filters", use_container_width=True):
            save_saved(filters)
            st.success("Saved on this device/server.")
    with c2:
        if st.button("↩ Reset", use_container_width=True):
            save_saved(DEFAULTS)
            st.rerun()

tab_search, tab_deal, tab_risk, tab_alerts = st.tabs(["🔎 Search cars", "🧮 Deal calculator", "🛠️ Vehicle risk check", "🔔 Alerts & Android"])

with tab_search:
    st.subheader("Your search")
    st.write(f"**Search phrase:** {build_query(filters)}")
    cols = st.columns(4)
    cols[0].metric("Max price", pounds(max_price))
    cols[1].metric("Max mileage", f"{max_miles:,}")
    cols[2].metric("Year range", f"{year_from}–{year_to}")
    cols[3].metric("Radius", f"{radius} miles")
    st.info("Search links open the marketplace. Apply or confirm year, engine size, mileage, location and radius on the marketplace itself: sites do not consistently accept every filter in their URLs.")
    s1, s2, s3 = st.columns(3)
    s1.link_button("Search eBay UK", ebay_url(filters), use_container_width=True)
    s2.link_button("Search Gumtree", gumtree_url(filters), use_container_width=True)
    s3.link_button("Search Facebook Marketplace", facebook_url(filters), use_container_width=True)
    st.markdown("#### Search another model quickly")
    quick = st.text_input("Temporary search phrase", placeholder="e.g. Honda Civic 1.8 petrol manual")
    if quick:
        qf = {**filters, "make": "", "model": quick, "keywords": "",}
        q1, q2, q3 = st.columns(3)
        q1.link_button("eBay", ebay_url(qf), use_container_width=True)
        q2.link_button("Gumtree", gumtree_url(qf), use_container_width=True)
        q3.link_button("Facebook", facebook_url(qf), use_container_width=True)
    st.caption("Saved filters are stored in saved_filters.json. On a hosted app, storage may reset when the app is redeployed; keep a backup of your filters.")

with tab_deal:
    st.subheader("Maximum offer and profit calculator")
    st.caption("Enter your own estimates. This is a planning calculator, not a valuation feed.")
    c1, c2 = st.columns(2)
    with c1:
        resale = st.number_input("Realistic resale price (£)", min_value=0, value=3000, step=100, key="resale")
        target_profit = st.number_input("Target profit (£)", min_value=0, value=1000, step=100, key="target")
        parts = st.number_input("Parts (£)", min_value=0, value=150, step=25, key="parts")
        labour = st.number_input("Labour / garage costs (£)", min_value=0, value=100, step=25, key="labour")
    with c2:
        prep = st.number_input("Cleaning, MOT, advertising and admin (£)", min_value=0, value=100, step=25, key="prep")
        warranty = st.number_input("Warranty / after-sales allowance (£)", min_value=0, value=150, step=25, key="warranty")
        contingency = st.number_input("Contingency (£)", min_value=0, value=200, step=25, key="contingency")
        other = st.number_input("Other costs / fees (£)", min_value=0, value=0, step=25, key="other")
    total_costs = parts + labour + prep + warranty + contingency + other
    max_offer = resale - target_profit - total_costs
    st.divider()
    k1, k2, k3 = st.columns(3)
    k1.metric("Maximum purchase offer", pounds(max(0, max_offer)))
    k2.metric("Total non-purchase costs", pounds(total_costs))
    k3.metric("Projected profit at £2,000 buy", pounds(resale - 2000 - total_costs))
    if max_offer <= 0:
        st.error("The deal does not meet your target profit at any positive purchase price using these estimates.")
    else:
        st.success(f"To target {pounds(target_profit)} profit, aim to pay no more than {pounds(max_offer)}.")
    st.caption("Include VAT/tax treatment, finance/insurance, transport, payment fees and any applicable business overheads in your own accounting.")

with tab_risk:
    st.subheader("Vehicle-specific risk worksheet")
    st.warning("This is a structured checklist, not an automatic mechanical diagnosis or a verified reliability database. Exact engine code, model year and service history matter.")
    r1, r2 = st.columns(2)
    with r1:
        vehicle = st.text_input("Vehicle / exact engine", placeholder="e.g. 2012 Honda Civic 1.8 i-VTEC")
        reg = st.text_input("Registration (optional)")
        mileage = st.number_input("Advertised mileage", min_value=0, max_value=500000, value=95000, step=1000)
        engine_code = st.text_input("Engine code (if known)")
        timing = st.selectbox("Timing system", ["Unknown", "Timing chain", "Dry timing belt", "Wet timing belt"])
        timing_evidence = st.selectbox("Timing maintenance evidence", ["Unknown / no evidence", "Invoices / verified history", "Not applicable / confirmed chain"])
    with r2:
        service = st.selectbox("Service history", ["Unknown / incomplete", "Partial", "Consistent invoices / stamps"])
        cold_start = st.selectbox("Cold start", ["Not checked", "Quiet / normal", "Rattle / knocking / tapping"])
        smoke = st.selectbox("Exhaust smoke", ["Not checked", "No unusual smoke", "Blue smoke", "White smoke when warm", "Black smoke"])
        oil = st.selectbox("Oil / coolant condition", ["Not checked", "Appears normal", "Low oil / sludge / contamination", "Oil in coolant / coolant in oil"])
        codes = st.selectbox("Diagnostic scan", ["Not done", "No relevant codes found", "Fault codes present / recently cleared"])
        mot = st.selectbox("MOT history", ["Not checked", "No concerning patterns", "Repeated advisories / failures", "Mileage or identity discrepancy"])
    extra_faults = st.text_area("Other known faults / seller statements", placeholder="Leaks, overheating, oil consumption, clutch slip, gearbox noise, warning lights...")
    inspection = st.selectbox("Independent inspection", ["Not arranged", "Booked", "Completed — no major concerns", "Completed — faults identified"])
    risk_points = 0
    risk_reasons = []
    if timing == "Unknown":
        risk_points += 1; risk_reasons.append("Timing system not verified.")
    if timing == "Dry timing belt" and timing_evidence == "Unknown / no evidence":
        risk_points += 2; risk_reasons.append("Cambelt history is unverified; confirm interval and price replacement.")
    if timing == "Wet timing belt":
        risk_points += 3; risk_reasons.append("Wet-belt system: verify exact engine, belt condition and replacement history; consider avoiding.")
    if timing == "Timing chain" and cold_start == "Rattle / knocking / tapping":
        risk_points += 3; risk_reasons.append("Cold-start rattle with chain engine needs diagnosis.")
    if service == "Unknown / incomplete":
        risk_points += 2; risk_reasons.append("Service history is incomplete or unknown.")
    if cold_start == "Not checked":
        risk_points += 1; risk_reasons.append("Cold start has not been observed.")
    elif cold_start == "Rattle / knocking / tapping":
        risk_points += 3; risk_reasons.append("Abnormal engine noise needs diagnosis.")
    if smoke in ["Blue smoke", "White smoke when warm", "Black smoke"]:
        risk_points += 3; risk_reasons.append("Unusual exhaust smoke needs diagnosis.")
    elif smoke == "Not checked":
        risk_points += 1; risk_reasons.append("Exhaust smoke has not been checked.")
    if oil in ["Low oil / sludge / contamination", "Oil in coolant / coolant in oil"]:
        risk_points += 4; risk_reasons.append("Potential lubrication or cooling-system concern.")
    elif oil == "Not checked":
        risk_points += 1; risk_reasons.append("Oil and coolant have not been checked.")
    if codes == "Fault codes present / recently cleared":
        risk_points += 2; risk_reasons.append("Fault codes or recent clearing require investigation.")
    elif codes == "Not done":
        risk_points += 1; risk_reasons.append("No diagnostic scan completed.")
    if mot in ["Repeated advisories / failures", "Mileage or identity discrepancy"]:
        risk_points += 2; risk_reasons.append("MOT pattern or mileage/identity concern.")
    elif mot == "Not checked":
        risk_points += 1; risk_reasons.append("MOT history not checked.")
    if inspection == "Completed — faults identified":
        risk_points += 2; risk_reasons.append("Independent inspection found faults; quantify before offer.")
    elif inspection in ["Not arranged", "Booked"]:
        risk_points += 1; risk_reasons.append("Independent inspection not yet completed.")
    st.divider()
    if st.button("Assess risk"):
        if risk_points <= 3:
            st.success(f"Preliminary screening: LOWER FLAGS ({risk_points} points). This does not mean the car is mechanically sound.")
        elif risk_points <= 7:
            st.warning(f"Preliminary screening: INVESTIGATE ({risk_points} points). Do not offer until key checks are completed.")
        else:
            st.error(f"Preliminary screening: HIGH RISK ({risk_points} points). Consider walking away unless fully diagnosed and priced.")
        for reason in risk_reasons:
            st.write("• " + reason)
        if extra_faults.strip():
            st.write("Additional notes: " + extra_faults)
    st.markdown("#### Copyable inspection / AI review brief")
    prompt = f"""Assess this potential UK used-car stock purchase. Be cautious and distinguish verified facts from assumptions.
Vehicle: {vehicle}
Registration: {reg}
Engine code: {engine_code}
Mileage: {mileage}
Timing system: {timing}; maintenance evidence: {timing_evidence}
Service history: {service}
Cold start: {cold_start}
Smoke: {smoke}
Oil/coolant: {oil}
Diagnostic scan: {codes}
MOT history: {mot}
Independent inspection: {inspection}
Other faults / seller statements: {extra_faults}
Please identify exact-engine-specific known risks, what evidence to request, tests to commission, likely repair-cost categories (not invented exact quotes), reasons to walk away, and what information is still missing. Do not claim a car is reliable based only on model reputation."""
    st.text_area("Copy this brief into ChatGPT with the advert, MOT history and photos", value=prompt, height=220)
    st.caption("A low score only means fewer warning flags were entered. It is not a roadworthiness certificate or a prediction of future failures.")

with tab_alerts:
    st.subheader("Marketplace alerts")
    st.markdown("""
**This app currently creates searches; it does not automatically monitor marketplace websites.** Use the sites' own saved-search alerts where available:

- **eBay:** open your search, sign in, save the search and enable notifications.
- **Facebook Marketplace:** save the search or enable listing notifications if the option appears for your account and region.
- **Gumtree:** sign in and look for saved-search or email-alert options.

Marketplace features and URL formats change. Avoid unofficial scraping or browser bots: they may breach platform terms or get accounts restricted.
""")
    st.subheader("Run on Android")
    st.markdown("""
**Simplest option: host it online and open it in Chrome on your phone.**

1. Create a free GitHub account at [github.com](https://github.com/).
2. Create a new repository, for example `car-finder-pro`.
3. Upload `app.py` and `requirements.txt` from this folder (optionally `README.md`).
4. Go to [Streamlit Community Cloud](https://share.streamlit.io/), sign in with GitHub and deploy the repository. Choose `app.py` as the app file.
5. Open the app's generated web address on your Android phone.
6. In Chrome, tap ⋮ → **Add to Home screen** (or **Install app**, if offered).

The dashboard then behaves much like an app shortcut. You need an internet connection. Treat the hosted app as private only if you configure access controls; don't enter sensitive personal information. Community Cloud is a hosting option with its own usage and availability limits.
""")
    st.info("If you prefer to run it entirely on your Android phone without hosting, it is possible using Termux, but it is more fiddly and the app only runs while the local server is running.")

st.divider()
st.caption("Car Finder Pro starter tool. Search links are best-effort and marketplace filters must be verified on the destination site. Always independently inspect vehicles and verify VIN, history, documents and exact engine specification.")

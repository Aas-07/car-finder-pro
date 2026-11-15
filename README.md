# Car Finder Pro

A flexible Streamlit app for searching UK used-car marketplaces and screening potential stock purchases.

## Features
- Editable make, model, keywords, year range, engine-size range, fuel, gearbox, condition, price, mileage, location and radius filters.
- Search links for eBay UK, Gumtree and Facebook Marketplace.
- Save/reset filters locally.
- Deal calculator: target profit, estimated resale, parts, labour, prep, warranty/after-sales allowance, contingency and other costs; calculates a maximum offer.
- Vehicle risk worksheet: timing system/history, service history, cold start, smoke, oil/coolant, diagnostic scan, MOT pattern and inspection status.
- Copyable brief to use with an AI assistant alongside a listing, MOT history and photographs.
- Android deployment instructions.

## Run on Windows, macOS or Linux
Install Python 3.10+ then in this folder run:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown in the terminal, usually http://localhost:8501.

## Run on Android (recommended: hosted web app)
1. Create a GitHub account and a new repository.
2. Upload `app.py` and `requirements.txt`.
3. Visit https://share.streamlit.io/ and sign in with GitHub.
4. Deploy the repository; set the main file to `app.py`.
5. Open the generated app URL on Android Chrome.
6. Chrome menu ⋮ → Add to Home screen / Install app.

The app runs on the hosted server, not locally on the phone. Internet access is required. Keep the repository private if you do not want the source code public, and review the hosting platform's current plan and privacy options.

## Marketplace and data limitations
This app opens search URLs; it does not scrape or automatically import listings. Marketplace sites can change their URL formats and may ignore some URL filters. Confirm year, engine, mileage, location and radius on the marketplace itself. Use each platform's native saved-search/alert feature for new listings. Do not use unofficial scraping or bots that may breach platform terms.

## Important
The risk worksheet is a checklist / triage aid, not a reliability database, mechanical diagnosis, valuation or guarantee. The max-offer calculation is only as accurate as your inputs. Independently verify engine code, timing system and maintenance schedule by VIN and manufacturer data.

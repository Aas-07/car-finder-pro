# Car Finder Pro

A Streamlit starter dashboard for UK used-car sourcing. It includes editable search filters, marketplace search links, a maximum-offer/profit calculator, and a vehicle-risk worksheet.

## Files

- `app.py` — the complete app
- `requirements.txt` — Python dependency
- `saved_filters.json` — starting filter values

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy/update on Streamlit Community Cloud

1. Download and extract this ZIP.
2. In your GitHub repository, open each existing file and replace its contents with the matching file from this updated folder. At minimum replace `app.py`; also replace `saved_filters.json` and `README.md` if present. Keep `requirements.txt`.
3. Commit the changes to the `main` branch.
4. Open your Streamlit Community Cloud app. It should redeploy automatically. If not, use the app menu to reboot/redeploy.
5. Refresh the app on your Android phone. The editable filters now appear directly under **Search cars**, not hidden in the sidebar.

## Search limitations

The app builds marketplace search words from Make, Model and optional extra keywords. The search phrase is blank when these are blank; it no longer inserts a default phrase. It passes the maximum price where supported by the marketplace URL. Marketplace websites do not consistently accept every filter (year, engine size, fuel, transmission, mileage, location and radius) in a search URL. Check and apply those filters on the destination marketplace after opening the link. This app does not scrape or automatically import listings.

## Notes

- The default maximum price is £2,000; change it in the visible search form.
- Location defaults to London and can be edited.
- A mileage value of `0` means no mileage limit.
- Engine min/max of `0` means no engine-size restriction.
- Saved settings on hosted free services may not persist through every redeploy or restart; keep your own copy of important settings.
- The risk worksheet is a checklist, not a mechanical diagnosis or verified engine-reliability database.

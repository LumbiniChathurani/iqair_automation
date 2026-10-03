import os
import requests

# --------------------------------------------------
# Configuration
# --------------------------------------------------

TOKEN = os.getenv("BROWSERLESS_TOKEN")

if not TOKEN:
    raise ValueError("BROWSERLESS_TOKEN is missing")

IQAIR_URL = (
    "https://www.iqair.com/air-quality/"
    "sri-lanka/central/akurana/fect-akurana-outdoor"
)

# Residential proxy + Stealth BrowserQL
ENDPOINT = (
    "https://production-sfo.browserless.io/stealth/bql"
    f"?token={TOKEN}"
    "&proxy=residential"
)


# --------------------------------------------------
# BrowserQL query
# --------------------------------------------------

query = """
mutation TestIQAir {
    goto(
        url: "https://www.iqair.com/air-quality/sri-lanka/central/akurana/fect-akurana-outdoor"
        waitUntil: networkIdle
    ) {
        status
    }

    solve(
        wait: true
    ) {
        found
        solved
        time
    }

    title {
        title
    }

    text {
        text
    }
}
"""


# --------------------------------------------------
# Send request to Browserless
# --------------------------------------------------

print("Starting BrowserQL test...")
print("Using residential proxy...")
print("Opening IQAir page...")

response = requests.post(
    ENDPOINT,
    headers={
        "Content-Type": "application/json"
    },
    json={
        "query": query,
        "operationName": "TestIQAir"
    },
    timeout=180
)

response.raise_for_status()

result = response.json()


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nBrowserQL response received.\n")

if "errors" in result:
    print("❌ BrowserQL returned errors:")
    print(result["errors"])
    raise SystemExit(1)

data = result.get("data", {})

goto_result = data.get("goto", {})
solve_result = data.get("solve", {})
title_result = data.get("title", {})
text_result = data.get("text", {})

status = goto_result.get("status")
title = title_result.get("title", "")
page_text = text_result.get("text", "")

print(f"BrowserQL goto status: {status}")
print(f"Page title: {title}")
print(
    f"CAPTCHA found: {solve_result.get('found')}"
)
print(
    f"CAPTCHA solved: {solve_result.get('solved')}"
)

print("\n" + "=" * 60)

# --------------------------------------------------
# Check whether IQAir was successfully loaded
# --------------------------------------------------

if "Vercel Security Checkpoint" in title:
    print("❌ IQAir security checkpoint detected.")

    print("\nFirst 1500 characters of page:")
    print(page_text[:1500])

elif "FECT-Akurana-outdoor" in page_text:
    print("✅ SUCCESS! IQAir page content was loaded.")

    print("\nFirst 3000 characters of page:")
    print(page_text[:3000])

else:
    print("⚠️ Page loaded, but expected IQAir content was not detected.")

    print("\nPage title:")
    print(title)

    print("\nFirst 1500 characters:")
    print(page_text[:1500])

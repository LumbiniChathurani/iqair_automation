import os
import requests

token = os.getenv("BROWSERLESS_TOKEN")

if not token:
    raise ValueError("BROWSERLESS_TOKEN is missing")

endpoint = "https://production-sfo.browserless.io/stealth/bql"

query = """
mutation TestIQAir {
    goto(
        url: "https://www.iqair.com/air-quality/sri-lanka/central/akurana/fect-akurana-outdoor"
        waitUntil: networkIdle
    ) {
        status
    }

    title {
        title
    }

    text {
        text
    }
}
"""

response = requests.post(
    endpoint,
    params={"token": token},
    json={
        "query": query,
        "operationName": "TestIQAir"
    },
    timeout=120
)

response.raise_for_status()

result = response.json()

page_title = result["data"]["title"]["title"]
page_text = result["data"]["text"]["text"]

print("BrowserQL goto status:", result["data"]["goto"]["status"])
print("Page title:", page_title)

if "Vercel Security Checkpoint" in page_title:
    print("❌ IQAir security checkpoint detected")
else:
    print("✅ Actual IQAir page loaded")

print("\nFirst 1000 characters of page:")
print(page_text[:1000])

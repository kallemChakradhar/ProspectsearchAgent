import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Mock signals if API not available
MOCK_SIGNALS = {
    "dataiq.com": {"hiring": True, "roles": ["Data Scientist", "ML Engineer"]},
    "fintechsolutions.com": {"hiring": False, "roles": []},
    "aianalytics.com": {"hiring": True, "roles": ["AI Engineer"]}
}

async def fetch_hiring_signals(domain: str):
    domain = domain.strip().lower() if domain else None
    if not domain:
        return {"hiring": False, "roles": []}

    if SERPAPI_KEY:
        try:
            url = "https://serpapi.com/search.json"
            params = {
                "engine": "google_jobs",
                "q": "hiring",
                "hl": "en",
                "location": "USA",
                "domain": domain,
                "api_key": SERPAPI_KEY
            }
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    if resp.status != 200:
                        raise Exception("API error")
                    data = await resp.json()
                    jobs = data.get("jobs_results", [])
                    return {"hiring": bool(jobs), "roles": [job.get("title") for job in jobs]}
        except:
            print(f"⚠️ Using mock hiring signals for {domain}")

    # fallback mock
    return MOCK_SIGNALS.get(domain, {"hiring": False, "roles": []})

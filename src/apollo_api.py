import os
import requests
from dotenv import load_dotenv
load_dotenv()

APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

def apollo_search_companies_and_contacts(icp):
    """Blocking version, wrapped in asyncio in main.py"""
    if APOLLO_API_KEY:
        print("🔍 Searching companies in Apollo (real API)...")
        headers = {"X-Api-Key": APOLLO_API_KEY}
        keywords = " ".join(icp.get("keywords", []))
        payload = {
            "q_keywords": keywords,
            "employee_count_min": icp.get("employee_count_min", 0),
            "revenue_min": icp.get("revenue_min", 0),
            "revenue_max": icp.get("revenue_max", 1_000_000_000),
            "geo": icp.get("geography", ["USA"])[0]
        }
        try:
            r = requests.post("https://api.apollo.io/v1/contacts/search", json=payload, headers=headers)
            if r.status_code != 200:
                raise Exception("Fallback to mock")
            data = r.json()
            companies = []
            for item in data.get("contacts", []):
                companies.append({
                    "company_name": item.get("company_name"),
                    "domain": item.get("company_domain"),
                    "contacts": [{
                        "name": f"{item.get('first_name', '')} {item.get('last_name', '')}",
                        "title": item.get("title"),
                        "email": item.get("email"),
                        "linkedin": item.get("linkedin_url")
                    }],
                    "industry": item.get("industry"),
                    "employee_count": item.get("employee_count"),
                    "revenue": item.get("revenue"),
                    "signals": {},
                    "source": ["Apollo"],
                    "confidence": 0.85
                })
            return companies
        except:
            print("⚠️ Using mock Apollo data due to API failure")

    # Mock data
    print("🔹 Returning mock Apollo data")
    return [
        {
            "company_name": "DataIQ Inc",
            "domain": "dataiq.com",
            "contacts": None,
            "industry": "B2B Software",
            "employee_count": 150,
            "revenue": 75000000,
            "signals": {"new_funding": True},
            "source": ["Apollo"],
            "confidence": 0.9
        }
    ]

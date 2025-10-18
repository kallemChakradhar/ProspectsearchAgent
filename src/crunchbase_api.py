import os
import requests
from dotenv import load_dotenv
load_dotenv()

CRUNCHBASE_API_KEY = os.getenv("CRUNCHBASE_API_KEY")

def fetch_companies_from_crunchbase(icp):
    """Blocking version, wrapped in asyncio in main.py"""
    if CRUNCHBASE_API_KEY:
        print("🔍 Fetching Crunchbase companies (real API)...")
        headers = {"X-Cb-User-Key": CRUNCHBASE_API_KEY}
        params = {
            "query": " ".join(icp.get("keywords", [])),
            "locations": icp.get("geography", ["USA"])[0],
            "employee_count_min": icp.get("employee_count_min", 0),
            "revenue_min": icp.get("revenue_min", 0)
        }
        try:
            r = requests.get("https://api.crunchbase.com/v4/data/organizations", headers=headers, params=params)
            if r.status_code != 200:
                raise Exception("Fallback to mock")
            data = r.json()
            companies = []
            for item in data.get("data", []):
                companies.append({
                    "company_name": item.get("properties", {}).get("name"),
                    "domain": item.get("properties", {}).get("website"),
                    "contacts": None,
                    "industry": item.get("properties", {}).get("category_list"),
                    "employee_count": item.get("properties", {}).get("num_employees_min"),
                    "revenue": item.get("properties", {}).get("annual_revenue"),
                    "signals": {"new_funding": bool(item.get("relationships", {}).get("funding_rounds"))},
                    "source": ["Crunchbase"],
                    "confidence": 0.85
                })
            return companies
        except:
            print("⚠️ Using mock Crunchbase data due to API failure")

    # Mock data
    print("🔹 Returning mock Crunchbase data")
    return [
        {
            "company_name": "FinTech Solutions",
            "domain": "fintechsolutions.com",
            "contacts": None,
            "industry": "FinTech",
            "employee_count": 300,
            "revenue": 120000000,
            "signals": {"new_funding": False},
            "source": ["Crunchbase"],
            "confidence": 0.85
        },
        {
            "company_name": "AI Analytics Co",
            "domain": "aianalytics.com",
            "contacts": None,
            "industry": "B2B Software",
            "employee_count": 100,
            "revenue": 50000000,
            "signals": {"new_funding": True},
            "source": ["Crunchbase"],
            "confidence": 0.88
        }
    ]

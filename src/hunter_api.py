import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

HUNTER_API_KEY = os.getenv("HUNTER_API_KEY")

# Mock fallback
MOCK_VERIFICATION = {
    "test@dataiq.com": True,
    "info@fintechsolutions.com": False,
    "contact@aianalytics.com": True
}

async def verify_email(email: str):
    email = email.strip().lower() if email else None
    if not email:
        return False

    if HUNTER_API_KEY:
        try:
            url = "https://api.hunter.io/v2/email-verifier"
            params = {"email": email, "api_key": HUNTER_API_KEY}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as resp:
                    if resp.status != 200:
                        raise Exception("API error")
                    data = await resp.json()
                    return data.get("data", {}).get("result") in ["deliverable", "risky"]
        except:
            print(f"⚠️ Using mock verification for {email}")

    # fallback mock
    return MOCK_VERIFICATION.get(email, True)

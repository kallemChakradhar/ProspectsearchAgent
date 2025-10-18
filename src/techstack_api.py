import os
import aiohttp
import asyncio
from dotenv import load_dotenv

load_dotenv()

BUILTWITH_API_KEY = os.getenv("BUILTWITH_API_KEY")
BASE_URL = "https://api.builtwith.com/v21/api.json"

TECH_STACK_MOCK = {
    "dataiq.com": ["AWS", "Snowflake", "Python", "React"],
    "fintechsolutions.com": ["Azure", "PostgreSQL", "Node.js", "Angular"],
    "aianalytics.com": ["GCP", "TensorFlow", "Python", "Vue.js"]
}

async def fetch_tech_stack(domain: str):
    if not domain:
        return []

    domain = domain.strip().lower()

    if BUILTWITH_API_KEY:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(BASE_URL, params={"KEY": BUILTWITH_API_KEY, "LOOKUP": domain}) as resp:
                    if resp.status != 200:
                        raise Exception("API error")
                    data = await resp.json()
                    techs = []
                    for cat in data.get("Results", {}).get("Paths", []):
                        for t in cat.get("Technologies", []):
                            techs.append(t.get("Name"))
                    return list(set(techs))
        except:
            print(f"⚠️ Using mock tech stack for {domain}")

    return TECH_STACK_MOCK.get(domain, ["AWS", "Python", "React"])  # fallback demo stack

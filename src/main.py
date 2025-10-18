import asyncio
from icp_parser import ICPParser
from apollo_api import apollo_search_companies_and_contacts
from crunchbase_api import fetch_companies_from_crunchbase
from merge_results import merge_and_deduplicate, save_to_json
from techstack_api import fetch_tech_stack
from serpapi_signals import fetch_hiring_signals
from hunter_api import verify_email

OUTPUT_FILE = "data/final_prospects.json"

async def enrich_company(company):
    domain = company.get("domain")

    # Tech stack + hiring signals
    tech_task = fetch_tech_stack(domain)
    hiring_task = fetch_hiring_signals(domain)

    # Email verification for all contacts
    contacts = company.get("contacts") or []
    email_tasks = [verify_email(c.get("email")) for c in contacts]

    tech_stack, hiring_signals, email_results = await asyncio.gather(
        tech_task, hiring_task, asyncio.gather(*email_tasks) if email_tasks else asyncio.gather()
    )

    # Update company
    company["tech_stack"] = tech_stack
    company["hiring_signals"] = hiring_signals
    for c, valid in zip(contacts, email_results or []):
        c["email_verified"] = valid

    return company

async def main():
    icp = ICPParser("config/icp_config.yaml").load_icp()

    # Fetch Apollo + Crunchbase concurrently
    apollo_task = asyncio.to_thread(apollo_search_companies_and_contacts, icp)
    crunchbase_task = asyncio.to_thread(fetch_companies_from_crunchbase, icp)
    apollo_data, crunchbase_data = await asyncio.gather(apollo_task, crunchbase_task)

    # Merge & deduplicate
    merged = merge_and_deduplicate(apollo_data, crunchbase_data)

    # Enrich all companies concurrently
    tasks = [enrich_company(c) for c in merged]
    final_results = await asyncio.gather(*tasks)

    # Save
    save_to_json(final_results, OUTPUT_FILE)
    print(final_results)

if __name__ == "__main__":
    asyncio.run(main())

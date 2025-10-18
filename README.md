ProspectSearchAgent
    ProspectSearchAgent is a Python tool that aggregates company and contact data from multiple sources, enriches it with tech stack and hiring signals, and outputs a clean, deduplicated list of prospects based on your Ideal Customer Profile (ICP).
    The tool works with real APIs if keys are provided, but can also use mock data for demo purposes.
Features
    Fetch companies and contacts from Apollo.io (or fallback mock data).


    Fetch funding & financial data from Crunchbase (or mock fallback).


    Detect technology stack using BuiltWith API.


    Fetch hiring/job signals using SerpAPI.


    Merge and deduplicate results from multiple sources.


    Configurable ICP in YAML/JSON.


    Outputs results in JSON format.


    Async-ready for faster API calls.


Project Structure
ProspectSearchAgent/
├── data/                     # Output JSON
├── config/                   # ICP configuration
│   └── icp_config.yaml
├── src/
│   ├── main.py                # Orchestrates async API calls & merges data
│   ├── apollo_api.py          # Apollo API / mock fallback
│   ├── crunchbase_api.py      # Crunchbase API / mock fallback
│   ├── techstack_api.py       # BuiltWith API / mock fallback
│   ├── serpapi_signals.py     # SerpAPI / hiring signals
│   ├── icp_parser.py          # Load ICP configuration
│   ├── merge_results.py       # Merge and deduplicate results
├── .env                       # API keys
├── requirements.txt           # Python dependencies
└── README.md                  # Project overview


How it Works

Workflow diagram:
      ┌─────────────┐
       │  ICP Config │
       └─────┬───────┘
             │
             ▼
 ┌────────────────────────┐
 │ Fetch company data     │
 │ - Apollo API           │
 │ - Crunchbase API       │
 └─────────┬──────────────┘
           │
           ▼
 ┌────────────────────────┐
 │ Enrich data            │
 │ - BuiltWith (Tech Stack) │
 │ - SerpAPI (Hiring)      │
 └─────────┬──────────────┘
           │
           ▼
 ┌────────────────────────┐
 │ Merge & deduplicate    │
 │ - Combine sources      │
 │ - Remove duplicates    │
 │ - Calculate confidence │
 └─────────┬──────────────┘
           │
           ▼
 ┌────────────────────────┐
 │ Save JSON output       │
 │ data/final_prospects.json │
 └────────────────────────┘




Step-by-step explanation:
    ICP Config – The user defines their Ideal Customer Profile in YAML/JSON format.


    Data Fetching – The system queries Apollo and Crunchbase APIs (or uses mock data if keys are missing).


    Data Enrichment – Each company is enriched with:


    Technology stack from BuiltWith API


    Hiring signals from SerpAPI


    Merge & Deduplicate – Data from multiple sources is combined, duplicates removed, confidence calculated.


    Output – Final cleaned data is saved in data/final_prospects.json.
    Setup
Clone the repository:

    git clone https://github.com/kallemChakradhar/ProspectsearchAgent.git
    cd ProspectSearchAgent

Create a virtual environment:
    python -m venv venv
    source venv/bin/activate      # Linux / macOS
    venv\Scripts\activate         # Windows

Install dependencies:
    pip install -r requirements.txt

Add your API keys to .env:
    APOLLO_API_KEY=your_apollo_key
    CRUNCHBASE_API_KEY=your_crunchbase_key
    BUILTWITH_API_KEY=your_builtwith_key
    SERPAPI_KEY=your_serpapi_key

Configure ICP in config/icp_config.yaml. Example:
    revenue_min: 20000000
    revenue_max: 200000000
    industry:
    - "B2B Software"
    - "FinTech"
    geography:
    - "USA"
    employee_count_min: 100
    keywords:
    - "AI"
    - "data analytics"
    - "automation"
    - "machine learning"
    signals:
    funding: true
    hiring_data_roles: true
    tech_stack:
        - "Snowflake"
        - "AWS"


Usage
Run the main script:
    python src/main.py

The final merged prospects will be saved in:
    data/final_prospects.json
Notes
    Works with mock data if APIs are not available.
    Supports async fetching for faster performance.


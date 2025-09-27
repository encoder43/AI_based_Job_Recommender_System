from apify_client import ApifyClient
import os 
from dotenv import load_dotenv

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def fetch_indeed_jobs(search_query: str, location: str = "in", rows: int = 20):
    """Fetches jobs from Indeed using a free Apify actor."""
    print(f"Fetching Indeed jobs for query: {search_query}")
    run_input = {
        "position": search_query,
        "country": location, # CORRECTED: Use country code 'in'
        "max_items": rows,
    }
    run = apify_client.actor("dtrungtin/indeed-scraper").call(run_input=run_input)
    return list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())

def fetch_google_jobs(search_query: str, location: str = "in", rows: int = 20):
    """Fetches jobs from Google Jobs using a free Apify actor."""
    print(f"Fetching Google jobs for query: {search_query}")
    run_input = {
        "queries": search_query,
        "countryCode": location, # CORRECTED: Use 'countryCode' parameter
        "maxPagesPerQuery": 1, # Limit to 1 page for speed
    }
    run = apify_client.actor("shtn/google-jobs-scraper").call(run_input=run_input)
    return list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())

def fetch_glassdoor_jobs(search_query: str, location: str = "India", rows: int = 20):
    """Fetches jobs from Glassdoor using a free Apify actor."""
    print(f"Fetching Glassdoor jobs for query: {search_query}")
    run_input = {
        "queries": search_query,
        "location": location, # CORRECTED: Use full country name as this actor expects it
        "maxItems": rows,
    }
    run = apify_client.actor("trudax/glassdoor-scraper").call(run_input=run_input)
    return list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())

def fetch_naukri_jobs(search_query: str, location: str = "india", rows: int = 60):
    """Fetches jobs from Naukri (your existing, working function)."""
    print(f"Fetching Naukri jobs for query: {search_query}")
    run_input = {
        "keyword": search_query,
        "maxJobs": rows,
    }
    run = apify_client.actor("alpcnRV9YI9lYVPWk").call(run_input=run_input)
    return list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
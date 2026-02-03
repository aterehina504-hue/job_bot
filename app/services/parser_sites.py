import requests
from bs4 import BeautifulSoup


INDEED_URLS = [
    "https://fr.indeed.com/jobs?q=&l=Cannes",
    "https://fr.indeed.com/jobs?q=&l=Nice",
]


def collect_site_jobs():
    jobs = []

    for url in INDEED_URLS:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for card in soup.select(".job_seen_beacon"):
            text = card.get_text(" ", strip=True)
            jobs.append({
                "source": "indeed",
                "text": text
            })

    return jobs

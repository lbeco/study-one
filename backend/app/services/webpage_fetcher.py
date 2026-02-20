import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional


class WebpageFetcher:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch(self, url: str) -> Dict:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return self.extract_content(response.text, url)
        except Exception as e:
            return {
                "url": url,
                "title": None,
                "description": None,
                "summary": None,
                "keywords": None,
                "error": str(e)
            }

    def extract_content(self, html: str, url: str) -> Dict:
        soup = BeautifulSoup(html, "html.parser")

        title = self._extract_title(soup)
        description = self._extract_meta(soup, "description")
        keywords = self._extract_meta(soup, "keywords")
        summary = self._extract_summary(soup)

        return {
            "url": url,
            "title": title,
            "description": description,
            "summary": summary,
            "keywords": keywords
        }

    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        if soup.title:
            return soup.title.string.strip()
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)
        return None

    def _extract_meta(self, soup: BeautifulSoup, name: str) -> Optional[str]:
        meta = soup.find("meta", attrs={"name": name})
        if meta and meta.get("content"):
            return meta["content"].strip()
        meta = soup.find("meta", attrs={"property": f"og:{name}"})
        if meta and meta.get("content"):
            return meta["content"].strip()
        return None

    def _extract_summary(self, soup: BeautifulSoup) -> Optional[str]:
        paragraphs = soup.find_all("p")
        if paragraphs:
            texts = [p.get_text(strip=True) for p in paragraphs[:3] if p.get_text(strip=True)]
            if texts:
                return " ".join(texts)[:500]
        return None


webpage_fetcher = WebpageFetcher()

"""
url_parser.py - Modular E-Commerce URL Extraction Layer
======================================================
Safely extracts product title, bullet claims, catalog images, and accessible
customer reviews from Amazon, Flipkart, or generic e-commerce product pages.
Follows ethical standards: no CAPTCHA bypassing or unauthorized auth bypass.
"""

import re
import urllib.parse
from typing import Optional, Dict, Any, List
import requests
from bs4 import BeautifulSoup
from .schema import UnifiedProductInput

SUPPORTED_DOMAINS = ["amazon.in", "amazon.com", "flipkart.com"]

class ProductURLExtractor:
    def __init__(self, timeout: int = 8):
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        }

    def validate_url(self, url: str) -> bool:
        """Checks if URL is well-formed and uses HTTP/HTTPS."""
        try:
            parsed = urllib.parse.urlparse(url.strip())
            return parsed.scheme in ["http", "https"] and bool(parsed.netloc)
        except Exception:
            return False

    def identify_domain(self, url: str) -> str:
        """Identifies domain or marks as generic."""
        netloc = urllib.parse.urlparse(url.strip()).netloc.lower()
        for domain in SUPPORTED_DOMAINS:
            if domain in netloc:
                return domain
        return "generic"

    def extract_from_url(self, url: str) -> UnifiedProductInput:
        """
        Retrieves accessible HTML and parses structured product representations.
        Returns UnifiedProductInput schema with source tracking.
        """
        if not self.validate_url(url):
            raise ValueError(f"Invalid product URL provided: '{url}'")

        domain = self.identify_domain(url)
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            html_content = response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Could not connect to URL ({e}). Site may require authentication or block scraping.")

        soup = BeautifulSoup(html_content, "html.parser")

        if "amazon" in domain:
            return self._parse_amazon(soup, url)
        elif "flipkart" in domain:
            return self._parse_flipkart(soup, url)
        else:
            return self._parse_generic(soup, url)

    def _parse_amazon(self, soup: BeautifulSoup, url: str) -> UnifiedProductInput:
        # Title
        title_tag = soup.find(id="productTitle") or soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Product"

        # Features / Bullet points
        features: List[str] = []
        feature_bullets = soup.find(id="feature-bullets")
        if feature_bullets:
            for li in feature_bullets.find_all("li"):
                text = li.get_text(strip=True)
                if text and len(text) > 10 and "make sure this fits" not in text.lower():
                    features.append(text)

        # Specifications
        specs: Dict[str, str] = {}
        tech_spec = soup.find(id="productDetails_techSpec_section_1")
        if tech_spec:
            for row in tech_spec.find_all("tr"):
                th = row.find("th")
                td = row.find("td")
                if th and td:
                    specs[th.get_text(strip=True)] = td.get_text(strip=True)

        # Images
        images: List[str] = []
        img_tag = soup.find(id="landingImage") or soup.find("img", {"class": "a-dynamic-image"})
        if img_tag and img_tag.get("src"):
            images.append(img_tag["src"])

        # Customer reviews (where visible in initial static HTML)
        reviews: List[Dict[str, Any]] = []
        review_elements = soup.find_all("div", {"data-hook": "review"})
        for rev in review_elements[:10]:
            body = rev.find("span", {"data-hook": "review-body"})
            if body:
                text = body.get_text(strip=True)
                if text:
                    reviews.append({"text": text, "source": "amazon_review"})

        # Product ID (ASIN if present in URL)
        asin_match = re.search(r"/(?:dp|gp/product)/([A-Z0-9]{10})", url)
        product_id = asin_match.group(1) if asin_match else "amazon_product"

        return UnifiedProductInput(
            product_id=product_id,
            title=title,
            features=features,
            specifications=specs,
            seller_images=images,
            customer_reviews=reviews,
            source_url=url,
            source_type="url"
        )

    def _parse_flipkart(self, soup: BeautifulSoup, url: str) -> UnifiedProductInput:
        title_tag = soup.find("span", {"class": "B_NuCI"}) or soup.find("h1")
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Product"

        features = [li.get_text(strip=True) for li in soup.find_all("li", {"class": "_21A_Va"}) if li.get_text(strip=True)]
        
        images = []
        img_tag = soup.find("img", {"class": "_396cs4"})
        if img_tag and img_tag.get("src"):
            images.append(img_tag["src"])

        return UnifiedProductInput(
            product_id="flipkart_product",
            title=title,
            features=features,
            seller_images=images,
            source_url=url,
            source_type="url"
        )

    def _parse_generic(self, soup: BeautifulSoup, url: str) -> UnifiedProductInput:
        title = soup.title.string.strip() if soup.title else "Generic E-Commerce Product"
        features = [p.get_text(strip=True) for p in soup.find_all(["p", "li"]) if 20 < len(p.get_text(strip=True)) < 250][:8]
        return UnifiedProductInput(
            product_id="generic_product",
            title=title,
            features=features,
            source_url=url,
            source_type="url"
        )

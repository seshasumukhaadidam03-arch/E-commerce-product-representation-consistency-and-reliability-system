import re
import socket
import ssl
import urllib.parse
from datetime import datetime
import bs4
import requests
import tldextract
import whois

class PhishingFeatureExtractor:
    """
    Extracts lexical, network, and content features from a given URL for phishing detection.
    """
    
    # Common URL shorteners
    SHORTENERS = {
        'bit.ly', 'goo.gl', 'shorte.st', 'go2l.ink', 'x.co', 'ow.ly', 't.co', 'tinyurl.com',
        'tr.im', 'is.gd', 'cli.gs', 'yfrog.com', 'migre.me', 'ff.im', 'tiny.cc', 'url4.eu',
        'twit.ac', 'su.pr', 'twurl.nl', 'snipurl.com', 'short.to', 'BudURL.com', 'ping.fm',
        'post.ly', 'Just.as', 'bkite.com', 'snipr.com', 'fic.kr', 'loopt.us', 'doiop.com',
        'short.ie', 'kl.am', 'wp.me', 'rubyurl.com', 'om.ly', 'to.ly', 'bit.do', 'lnkd.in',
        'db.tt', 'qr.ae', 'adf.ly', 'goo.io', 'link.zip', 'tiny.one'
    }

    def __init__(self, timeout=5.0):
        self.timeout = timeout

    def extract_all(self, url: str) -> dict:
        """
        Extracts lexical, network, and DOM features from a URL.
        Handles errors gracefully by returning fallback default values.
        """
        # Ensure URL has a scheme
        if not re.match(r'^https?://', url, re.IGNORECASE):
            url = 'http://' + url

        features = {}
        
        # 1. Lexical Features
        lexical = self.extract_lexical_features(url)
        features.update(lexical)
        
        # 2. Network/Security Features
        network = self.extract_network_features(url)
        features.update(network)
        
        # 3. DOM/Content Features (requires fetching page)
        dom = self.extract_dom_features(url)
        features.update(dom)
        
        return features

    def extract_lexical_features(self, url: str) -> dict:
        """
        Extracts structural and lexical features from the URL string.
        """
        parsed = urllib.parse.urlparse(url)
        netloc = parsed.netloc
        path = parsed.path
        
        # Extract subdomain, domain, and suffix
        extracted = tldextract.extract(url)
        domain = f"{extracted.domain}.{extracted.suffix}"
        subdomain = extracted.subdomain
        
        # Check for IP address in domain
        is_ip = 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', netloc) else 0
        
        # Check for URL shorteners
        is_shortened = 1 if netloc.lower() in self.SHORTENERS or domain.lower() in self.SHORTENERS else 0
        
        # Count subdomains
        qty_subdomains = len(subdomain.split('.')) if subdomain else 0
        
        # Suspicious keywords in domain
        suspicious_keywords = ['login', 'signin', 'verify', 'update', 'secure', 'account', 'banking', 'support', 'free']
        has_suspicious_keyword = 1 if any(kw in netloc.lower() for kw in suspicious_keywords) else 0

        # Feature mapping (matched to common public model features)
        return {
            'url_length': len(url),
            'domain_length': len(domain),
            'qty_dot_url': url.count('.'),
            'qty_hyphen_url': url.count('-'),
            'qty_slash_url': url.count('/'),
            'qty_questionmark_url': url.count('?'),
            'qty_equal_url': url.count('='),
            'qty_at_url': url.count('@'),
            'qty_and_url': url.count('&'),
            'qty_exclamation_url': url.count('!'),
            'qty_tilde_url': url.count('~'),
            'qty_comma_url': url.count(','),
            'qty_plus_url': url.count('+'),
            'qty_asterisk_url': url.count('*'),
            'qty_hashtag_url': url.count('#'),
            'qty_dollar_url': url.count('$'),
            'qty_percent_url': url.count('%'),
            'is_ip': is_ip,
            'is_shortened': is_shortened,
            'qty_subdomains': qty_subdomains,
            'has_suspicious_keyword': has_suspicious_keyword
        }

    def extract_network_features(self, url: str) -> dict:
        """
        Extracts network, SSL, and WHOIS features.
        """
        parsed = urllib.parse.urlparse(url)
        domain_name = tldextract.extract(url).registered_domain
        
        is_ssl = 1 if parsed.scheme.lower() == 'https' else 0
        
        # Default fallback values
        domain_age_days = -1
        domain_expiry_days = -1
        
        # Fetch WHOIS info
        try:
            w = whois.whois(domain_name)
            creation_date = w.creation_date
            expiration_date = w.expiration_date
            
            # Extract date if it's a list (some domains return multiple dates)
            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]
                
            now = datetime.now()
            
            if creation_date and isinstance(creation_date, datetime):
                domain_age_days = (now - creation_date).days
            if expiration_date and isinstance(expiration_date, datetime):
                domain_expiry_days = (expiration_date - now).days
        except Exception:
            # WHOIS fails often for dynamic, transient, or custom top-level domains
            pass
            
        return {
            'is_ssl': is_ssl,
            'domain_age_days': domain_age_days,
            'domain_expiry_days': domain_expiry_days
        }

    def extract_dom_features(self, url: str) -> dict:
        """
        Fetches the web page content and extracts DOM-based security metrics.
        """
        # Default fallbacks if domain is offline or blocked
        features = {
            'qty_iframes': 0,
            'qty_forms': 0,
            'qty_external_links': 0,
            'form_action_external': 0,
            'qty_hidden_elements': 0
        }
        
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/120.0.0.0 Safari/537.36'
            )
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=self.timeout, allow_redirects=True)
            if response.status_code != 200:
                return features
                
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            
            # Count iframes
            features['qty_iframes'] = len(soup.find_all('iframe'))
            
            # Count forms
            forms = soup.find_all('form')
            features['qty_forms'] = len(forms)
            
            # Analyze links
            links = soup.find_all('a', href=True)
            total_links = len(links)
            external_links = 0
            
            parsed_url = urllib.parse.urlparse(url)
            base_domain = tldextract.extract(url).registered_domain
            
            for link in links:
                href = link['href']
                link_parsed = urllib.parse.urlparse(href)
                # If absolute URL and domain differs
                if link_parsed.netloc:
                    link_domain = tldextract.extract(href).registered_domain
                    if link_domain != base_domain:
                        external_links += 1
                        
            features['qty_external_links'] = external_links / total_links if total_links > 0 else 0
            
            # Check form action points to external/suspicious domain
            form_action_external = 0
            for form in forms:
                action = form.get('action', '')
                if action:
                    action_parsed = urllib.parse.urlparse(action)
                    if action_parsed.netloc:
                        action_domain = tldextract.extract(action).registered_domain
                        if action_domain != base_domain:
                            form_action_external = 1
                            break
            features['form_action_external'] = form_action_external
            
            # Count hidden elements (basic checker)
            hidden_tags = len(soup.find_all(attrs={"type": "hidden"}))
            hidden_styles = len(soup.find_all(style=re.compile(r'display:\s*none|visibility:\s*hidden', re.IGNORECASE)))
            features['qty_hidden_elements'] = hidden_tags + hidden_styles
            
        except Exception:
            # Silence exceptions, return defaults for offline domains
            pass
            
        return features

if __name__ == '__main__':
    # Simple self-test
    extractor = PhishingFeatureExtractor()
    test_url = "https://www.google.com"
    print(f"Extracting features for {test_url}...")
    feats = extractor.extract_all(test_url)
    for k, v in feats.items():
        print(f"  {k}: {v}")

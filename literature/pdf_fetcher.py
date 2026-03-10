"""
PDF fetcher module with Unpaywall API and fallback retrieval.
Modeled on clawd-is-lit repository workflow.
"""

import os
import requests
import time
import re
from typing import Optional, Dict, Tuple
from urllib.parse import quote
import yaml
from playwright.async_api import async_playwright
import asyncio


class PDFFetcher:
    """Fetch PDFs using Unpaywall API first, then fallback methods."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.unpaywall_config = self.config.get("unpaywall", {})
        self.mirrors = self.config.get("mirrors", [])
        self.retrieval_config = self.config.get("retrieval", {})
        self.pdf_dir = self.config.get("pdf_directory", "pdfs")

        # Ensure PDF directory exists
        os.makedirs(self.pdf_dir, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}
        )

    def fetch_pdf(self, paper: Dict) -> Tuple[bool, Optional[str], str]:
        """
        Attempt to fetch PDF for a paper using multiple methods.

        Args:
            paper: Paper metadata dict with 'doi', 'title', 'url' keys

        Returns:
            Tuple of (success, filepath, access_route)
            - success: True if PDF was downloaded
            - filepath: Path to downloaded PDF (or None)
            - access_route: Description of how PDF was accessed
        """
        title = paper.get("title", "unknown")
        doi = paper.get("doi")
        url = paper.get("url")

        # Create safe filename
        filename = self._sanitize_filename(title) + ".pdf"
        filepath = os.path.join(self.pdf_dir, filename)

        # Skip if already downloaded
        if os.path.exists(filepath):
            return True, filepath, "already_downloaded"

        # Try methods in order of preference
        methods = [
            ("unpaywall", lambda: self._try_unpaywall(doi, filepath)),
            ("direct_url", lambda: self._try_direct_download(url, filepath)),
            # Note: mirror fallback requires async, skip for now in sync context
            # ('mirrors', lambda: asyncio.run(self._try_mirrors(doi, title, filepath)))
        ]

        for method_name, method_func in methods:
            if method_name == "unpaywall" and not doi:
                continue
            if method_name == "direct_url" and not url:
                continue

            try:
                success = method_func()
                if success:
                    return True, filepath, method_name
            except Exception as e:
                print(f"  {method_name} failed: {e}")
                continue

            # Delay between attempts
            time.sleep(self.retrieval_config.get("delay_between_requests", 2))

        return False, None, "all_methods_failed"

    def _try_unpaywall(self, doi: str, filepath: str) -> bool:
        """Try to download PDF via Unpaywall API."""
        if not doi:
            return False

        email = self.unpaywall_config.get("email")
        api_url = self.unpaywall_config.get("api_url", "https://api.unpaywall.org/v2")

        if not email or email == "your.email@example.com":
            print("  Warning: Unpaywall email not configured in config.yaml")
            return False

        url = f"{api_url}/{doi}?email={email}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Try to find best open access location
            best_oa = data.get("best_oa_location")
            if best_oa and best_oa.get("url_for_pdf"):
                pdf_url = best_oa["url_for_pdf"]
                return self._download_pdf(pdf_url, filepath)

            # Try oa_locations
            oa_locations = data.get("oa_locations", [])
            for location in oa_locations:
                pdf_url = location.get("url_for_pdf")
                if pdf_url:
                    if self._download_pdf(pdf_url, filepath):
                        return True

        except Exception as e:
            print(f"  Unpaywall error: {e}")

        return False

    def _try_direct_download(self, url: str, filepath: str) -> bool:
        """Try to download PDF directly from the paper URL."""
        if not url:
            return False

        # Check if URL already points to a PDF
        if url.lower().endswith(".pdf"):
            return self._download_pdf(url, filepath)

        # Try to find PDF link on the page
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # Look for PDF links in the HTML
            pdf_patterns = [
                r'href="([^"]+\.pdf)"',
                r'href="([^"]+/pdf/[^"]+)"',
                r'<meta name="citation_pdf_url" content="([^"]+)"',
            ]

            for pattern in pdf_patterns:
                matches = re.findall(pattern, response.text, re.IGNORECASE)
                for pdf_url in matches:
                    # Make absolute URL if relative
                    if not pdf_url.startswith("http"):
                        from urllib.parse import urljoin

                        pdf_url = urljoin(url, pdf_url)

                    if self._download_pdf(pdf_url, filepath):
                        return True

        except Exception as e:
            print(f"  Direct download error: {e}")

        return False

    async def _try_mirrors(self, doi: str, title: str, filepath: str) -> bool:
        """Try to download from mirror sites using browser automation."""
        if not self.mirrors:
            return False

        # Prefer DOI search if available
        search_term = doi if doi else title

        for mirror in self.mirrors:
            try:
                print(f"  Trying mirror: {mirror}")
                success = await self._fetch_from_mirror(mirror, search_term, filepath)
                if success:
                    return True
            except Exception as e:
                print(f"  Mirror {mirror} failed: {e}")
                continue

        return False

    async def _fetch_from_mirror(
        self, mirror_url: str, search_term: str, filepath: str
    ) -> bool:
        """Fetch PDF from a specific mirror site using Playwright."""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                # Navigate to mirror
                await page.goto(
                    mirror_url, wait_until="domcontentloaded", timeout=30000
                )

                # Find search input and submit
                await page.fill(
                    'input[type="text"], input[name="q"], input#search', search_term
                )
                await page.press(
                    'input[type="text"], input[name="q"], input#search', "Enter"
                )

                # Wait for results or PDF
                await page.wait_for_load_state("networkidle", timeout=30000)

                # Look for download button or direct PDF link
                download_selectors = [
                    'button:has-text("download")',
                    'a:has-text("download")',
                    'a[href$=".pdf"]',
                    "#download",
                ]

                for selector in download_selectors:
                    try:
                        element = await page.query_selector(selector)
                        if element:
                            # Start download
                            async with page.expect_download() as download_info:
                                await element.click()
                            download = await download_info.value
                            await download.save_as(filepath)
                            await browser.close()
                            return True
                    except:
                        continue

            except Exception as e:
                print(f"  Mirror fetch error: {e}")
            finally:
                await browser.close()

        return False

    def _download_pdf(self, url: str, filepath: str) -> bool:
        """Download PDF from URL to filepath."""
        try:
            response = self.session.get(
                url,
                timeout=self.retrieval_config.get("timeout_seconds", 30),
                stream=True,
            )
            response.raise_for_status()

            # Check if response is actually a PDF
            content_type = response.headers.get("Content-Type", "")
            if "pdf" not in content_type.lower():
                # Try anyway - some servers don't set correct content type
                pass

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Verify the file is a valid PDF
            if os.path.exists(filepath):
                with open(filepath, "rb") as f:
                    header = f.read(4)
                    if header == b"%PDF":
                        return True
                    else:
                        os.remove(filepath)
                        return False

        except Exception as e:
            print(f"  Download error: {e}")
            if os.path.exists(filepath):
                os.remove(filepath)

        return False

    def _sanitize_filename(self, title: str, max_length: int = 200) -> str:
        """Create safe filename from paper title."""
        # Remove/replace unsafe characters
        safe = re.sub(r'[<>:"/\\|?*]', "", title)
        safe = re.sub(r"\s+", "_", safe)
        safe = safe[:max_length]
        return safe


def main():
    """Example usage."""
    fetcher = PDFFetcher()

    # Example paper
    paper = {
        "title": "Designing Social Inquiry",
        "doi": "10.2307/j.ctt7sfzx",
        "url": "https://scholar.google.com/scholar?q=designing+social+inquiry",
    }

    print(f"Attempting to fetch: {paper['title']}")
    success, filepath, method = fetcher.fetch_pdf(paper)

    if success:
        print(f"Success! Downloaded via {method}")
        print(f"Saved to: {filepath}")
    else:
        print(f"Failed to download (attempted: {method})")


if __name__ == "__main__":
    main()

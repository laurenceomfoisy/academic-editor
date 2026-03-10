"""
Google Scholar search module using Playwright for browser automation.
Modeled on clawd-is-lit repository workflow.
"""

import asyncio
import re
from typing import List, Dict, Optional
from playwright.async_api import async_playwright, Page, Browser
import yaml
import os


class ScholarSearcher:
    """Search Google Scholar and extract paper metadata."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.scholar_config = self.config.get("scholar", {})
        self.browser_config = self.config.get("browser", {})
        self.retrieval_config = self.config.get("retrieval", {})

    async def search(self, query: str, max_results: int = None) -> List[Dict]:
        """
        Search Google Scholar for papers matching the query.

        Args:
            query: Search query string
            max_results: Maximum number of results (defaults to config)

        Returns:
            List of paper metadata dictionaries with keys:
            - title: Paper title
            - authors: List of author names
            - year: Publication year
            - venue: Journal/conference name
            - url: Direct link to paper (if available)
            - doi: DOI (if available)
            - citations: Citation count
            - abstract: Paper abstract (if available)
        """
        if max_results is None:
            max_results = self.scholar_config.get("max_results", 20)

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=self.browser_config.get("headless", True),
                slow_mo=self.browser_config.get("slow_mo", 100),
            )

            page = await browser.new_page()
            papers = []

            try:
                # Build search URL with optional year filters
                search_url = self._build_search_url(query)

                await page.goto(search_url, wait_until="networkidle", timeout=30000)

                # Wait for results to load
                await page.wait_for_selector(".gs_r.gs_or.gs_scl", timeout=10000)

                # Extract paper metadata from search results
                papers = await self._extract_papers(page, max_results)

            except Exception as e:
                print(f"Error during Scholar search: {e}")
            finally:
                await browser.close()

            return papers

    def _build_search_url(self, query: str) -> str:
        """Build Google Scholar search URL with optional filters."""
        base_url = "https://scholar.google.com/scholar"
        params = f"?q={query.replace(' ', '+')}"

        year_start = self.scholar_config.get("year_start")
        year_end = self.scholar_config.get("year_end")

        if year_start:
            params += f"&as_ylo={year_start}"
        if year_end:
            params += f"&as_yhi={year_end}"

        return base_url + params

    async def _extract_papers(self, page: Page, max_results: int) -> List[Dict]:
        """Extract paper metadata from Scholar results page."""
        papers = []

        # Get all paper result elements
        results = await page.query_selector_all(".gs_r.gs_or.gs_scl")

        for i, result in enumerate(results[:max_results]):
            try:
                paper = await self._extract_paper_metadata(result)
                if paper:
                    papers.append(paper)

                # Delay between extractions to avoid rate limiting
                delay = self.retrieval_config.get("delay_between_requests", 2)
                await asyncio.sleep(delay)

            except Exception as e:
                print(f"Error extracting paper {i + 1}: {e}")
                continue

        return papers

    async def _extract_paper_metadata(self, result_element) -> Optional[Dict]:
        """Extract metadata from a single Scholar result element."""
        try:
            # Title and main link
            title_elem = await result_element.query_selector(".gs_rt a")
            title = await title_elem.inner_text() if title_elem else None
            url = await title_elem.get_attribute("href") if title_elem else None

            # Remove [HTML], [PDF] tags from title
            if title:
                title = re.sub(r"\[(HTML|PDF)\]\s*", "", title)

            # Authors, year, venue (in gs_a element)
            gs_a = await result_element.query_selector(".gs_a")
            gs_a_text = await gs_a.inner_text() if gs_a else ""

            authors, year, venue = self._parse_gs_a(gs_a_text)

            # Abstract snippet
            abstract_elem = await result_element.query_selector(".gs_rs")
            abstract = await abstract_elem.inner_text() if abstract_elem else None

            # Citation count
            citations = 0
            cite_elem = await result_element.query_selector(".gs_fl a")
            if cite_elem:
                cite_text = await cite_elem.inner_text()
                match = re.search(r"Cited by (\d+)", cite_text)
                if match:
                    citations = int(match.group(1))

            # Try to extract DOI from URL or page
            doi = self._extract_doi(url) if url else None

            return {
                "title": title,
                "authors": authors,
                "year": year,
                "venue": venue,
                "url": url,
                "doi": doi,
                "citations": citations,
                "abstract": abstract,
            }

        except Exception as e:
            print(f"Error parsing result element: {e}")
            return None

    def _parse_gs_a(self, gs_a_text: str) -> tuple:
        """Parse the gs_a element containing authors, year, venue."""
        # Format: "Author1, Author2 - Venue, Year - Publisher"
        authors = []
        year = None
        venue = None

        if not gs_a_text:
            return authors, year, venue

        parts = gs_a_text.split(" - ")

        if len(parts) > 0:
            # First part contains authors
            author_text = parts[0].strip()
            authors = [a.strip() for a in author_text.split(",")]

        if len(parts) > 1:
            # Second part contains venue and year
            venue_year = parts[1].strip()
            # Extract year (4 digits)
            year_match = re.search(r"\b(19|20)\d{2}\b", venue_year)
            if year_match:
                year = int(year_match.group(0))
                venue = venue_year.replace(year_match.group(0), "").strip(" ,")
            else:
                venue = venue_year

        return authors, year, venue

    def _extract_doi(self, url: str) -> Optional[str]:
        """Extract DOI from URL if present."""
        if not url:
            return None

        # Common DOI patterns
        doi_match = re.search(r"10\.\d{4,}/[^\s]+", url)
        if doi_match:
            return doi_match.group(0)

        return None


async def main():
    """Example usage."""
    searcher = ScholarSearcher()

    query = "causal inference political science"
    print(f"Searching Google Scholar for: {query}")

    papers = await searcher.search(query, max_results=5)

    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper['title']}")
        print(
            f"   Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}"
        )
        print(f"   Year: {paper['year']}")
        print(f"   Venue: {paper['venue']}")
        print(f"   Citations: {paper['citations']}")
        print(f"   DOI: {paper['doi']}")
        print(f"   URL: {paper['url']}")


if __name__ == "__main__":
    asyncio.run(main())

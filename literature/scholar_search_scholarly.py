"""
Google Scholar search module using scholarly library with built-in anti-blocking.
This is more reliable than direct Playwright scraping for production use.
"""

import time
from typing import List, Dict, Optional
import yaml
import os
from scholarly import scholarly, ProxyGenerator


class ScholarSearcher:
    """Search Google Scholar and extract paper metadata using scholarly library."""

    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "config.yaml")

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.scholar_config = self.config.get("scholar", {})
        self.retrieval_config = self.config.get("retrieval", {})

        # Setup proxy if needed (helps avoid blocking)
        try:
            pg = ProxyGenerator()
            # Use free proxies (scholarly has built-in free proxy support)
            # scholarly.use_proxy(pg)
            pass  # Comment out proxy for now - may not be needed
        except:
            pass

    def search(self, query: str, max_results: int = None) -> List[Dict]:
        """
        Search Google Scholar for papers matching the query.

        Args:
            query: Search query string
            max_results: Maximum number of results (defaults to config)

        Returns:
            List of paper metadata dictionaries
        """
        if max_results is None:
            max_results = self.scholar_config.get("max_results", 20)

        papers = []

        try:
            # Search using scholarly library
            search_query = scholarly.search_pubs(query)

            for i in range(max_results):
                try:
                    result = next(search_query)
                    paper = self._extract_paper_metadata(result)
                    if paper:
                        papers.append(paper)
                        print(f"  [{i + 1}] {paper['title'][:60]}...")

                    # Delay between requests to avoid rate limiting
                    delay = self.retrieval_config.get("delay_between_requests", 2)
                    time.sleep(delay)

                except StopIteration:
                    break
                except Exception as e:
                    print(f"  Error extracting paper {i + 1}: {e}")
                    continue

        except Exception as e:
            print(f"Error during Scholar search: {e}")

        return papers

    def _extract_paper_metadata(self, result) -> Optional[Dict]:
        """Extract metadata from a scholarly result object."""
        try:
            # Get basic info
            bib = result.get("bib", {})

            title = bib.get("title", "Unknown")
            authors = bib.get("author", [])
            if isinstance(authors, str):
                authors = [authors]

            year = bib.get("pub_year")
            if year:
                try:
                    year = int(year)
                except:
                    year = None

            venue = bib.get("venue", bib.get("journal", ""))
            abstract = bib.get("abstract", "")

            # Get URL
            url = result.get("pub_url") or result.get("eprint_url")

            # Get citation count
            citations = result.get("num_citations", 0)

            # Try to extract DOI
            doi = None
            if "pub_url" in result:
                import re

                doi_match = re.search(r"10\.\d{4,}/[^\s]+", result["pub_url"])
                if doi_match:
                    doi = doi_match.group(0)

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
            print(f"Error parsing result: {e}")
            return None


def main():
    """Example usage."""
    searcher = ScholarSearcher()

    query = "causal inference political science"
    print(f"Searching Google Scholar for: {query}")

    papers = searcher.search(query, max_results=5)

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
    main()

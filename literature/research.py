"""
Main research pipeline orchestrator.
Coordinates Google Scholar search, PDF retrieval, and reading.
Modeled on clawd-is-lit repository workflow.
"""

import asyncio
import json
import os
from typing import List, Dict
from datetime import datetime
from pathlib import Path

# Try to import the scholarly-based searcher first (more reliable)
# Fall back to Playwright-based searcher if needed
try:
    from scholar_search_scholarly import ScholarSearcher

    USING_SCHOLARLY = True
except ImportError:
    from scholar_search import ScholarSearcher

    USING_SCHOLARLY = False

from pdf_fetcher import PDFFetcher


class ResearchPipeline:
    """Orchestrate literature search, retrieval, and reading."""

    def __init__(self, config_path: str = None):
        self.searcher = ScholarSearcher(config_path)
        self.fetcher = PDFFetcher(config_path)
        self.output_dir = Path(self.fetcher.pdf_dir).resolve()
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {
            "query": None,
            "timestamp": None,
            "papers_found": 0,
            "pdfs_downloaded": 0,
            "pdfs_failed": 0,
            "papers": [],
            "output_directory": str(self.output_dir),
        }

    async def run(
        self, query: str, max_results: int = None, read_pdfs: bool = False
    ) -> Dict:
        """
        Run complete literature retrieval pipeline.

        Args:
            query: Search query for Google Scholar
            max_results: Maximum papers to retrieve (defaults to config)
            read_pdfs: If True, read and extract text from downloaded PDFs

        Returns:
            Dictionary with pipeline results including:
            - query: Original search query
            - timestamp: When search was run
            - papers_found: Number of papers found
            - pdfs_downloaded: Number of PDFs successfully downloaded
            - pdfs_failed: Number of download failures
            - papers: List of paper metadata with download status
        """
        print(f"\n{'=' * 70}")
        print(f"LITERATURE RETRIEVAL PIPELINE")
        print(f"{'=' * 70}")
        print(f"Query: {query}")
        print(f"Max results: {max_results or 'default'}")
        print(
            f"Search method: {'scholarly library' if USING_SCHOLARLY else 'Playwright'}"
        )
        print(f"{'=' * 70}\n")

        # Initialize results
        self.results["query"] = query
        self.results["timestamp"] = datetime.now().isoformat()

        # Step 1: Search Google Scholar
        print("STEP 1: Searching Google Scholar...")
        if USING_SCHOLARLY:
            papers = self.searcher.search(query, max_results)
        else:
            papers = await self.searcher.search(query, max_results)
        self.results["papers_found"] = len(papers)

        print(f"Found {len(papers)} papers\n")

        if not papers:
            print("No papers found. Exiting.")
            return self.results

        # Step 2: Fetch PDFs
        print("STEP 2: Fetching PDFs...")
        for i, paper in enumerate(papers, 1):
            print(f"\n[{i}/{len(papers)}] {paper['title'][:60]}...")

            success, filepath, access_route = self.fetcher.fetch_pdf(paper)

            paper["pdf_downloaded"] = success
            paper["pdf_path"] = filepath
            paper["access_route"] = access_route

            if success:
                self.results["pdfs_downloaded"] += 1
                print(f"  ✓ Downloaded via {access_route}")
            else:
                self.results["pdfs_failed"] += 1
                print(f"  ✗ Failed ({access_route})")

            self.results["papers"].append(paper)

        # Step 3: Read PDFs (optional)
        if read_pdfs:
            print("\nSTEP 3: Reading PDFs...")
            for paper in self.results["papers"]:
                if paper["pdf_downloaded"] and paper["pdf_path"]:
                    print(f"Reading: {paper['title'][:60]}...")
                    # TODO: Implement PDF text extraction
                    # This would use PyPDF2 or pdfplumber to extract text
                    pass

        # Print summary
        self._print_summary()

        return self.results

    def _print_summary(self):
        """Print pipeline execution summary."""
        print(f"\n{'=' * 70}")
        print("PIPELINE SUMMARY")
        print(f"{'=' * 70}")
        print(f"Query: {self.results['query']}")
        print(f"Papers found: {self.results['papers_found']}")
        print(f"PDFs downloaded: {self.results['pdfs_downloaded']}")
        print(f"PDFs failed: {self.results['pdfs_failed']}")
        print(f"Output directory: {self.results['output_directory']}")

        if self.results["papers_found"] > 0:
            success_rate = (
                self.results["pdfs_downloaded"] / self.results["papers_found"]
            ) * 100
            print(f"Success rate: {success_rate:.1f}%")

        print(f"\nDownload methods used:")
        methods = {}
        for paper in self.results["papers"]:
            if paper["pdf_downloaded"]:
                route = paper["access_route"]
                methods[route] = methods.get(route, 0) + 1

        for method, count in sorted(methods.items(), key=lambda x: x[1], reverse=True):
            print(f"  {method}: {count}")

        print(f"{'=' * 70}\n")

    def save_results(self, filepath: str = None):
        """Save pipeline results to JSON file."""
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = str(self.output_dir / f"research_results_{timestamp}.json")

        with open(filepath, "w") as f:
            json.dump(self.results, f, indent=2)

        print(f"Results saved to: {filepath}")

    def get_downloaded_papers(self) -> List[Dict]:
        """Return list of successfully downloaded papers."""
        return [p for p in self.results["papers"] if p["pdf_downloaded"]]

    def get_failed_papers(self) -> List[Dict]:
        """Return list of papers that failed to download."""
        return [p for p in self.results["papers"] if not p["pdf_downloaded"]]


async def main():
    """Example usage."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python /path/to/research.py '<search query>' [max_results]")
        print("\nExample:")
        print(
            "  ~/.config/opencode/literature/venv/bin/python ~/.config/opencode/literature/research.py 'causal inference political science' 10"
        )
        sys.exit(1)

    query = sys.argv[1]
    max_results = int(sys.argv[2]) if len(sys.argv) > 2 else None

    pipeline = ResearchPipeline()
    results = await pipeline.run(query, max_results=max_results)

    # Save results
    pipeline.save_results()

    # Show downloaded papers
    downloaded = pipeline.get_downloaded_papers()
    if downloaded:
        print("\nSuccessfully downloaded papers:")
        for paper in downloaded:
            print(f"  - {paper['title']}")
            print(f"    File: {paper['pdf_path']}")

    # Show failed papers
    failed = pipeline.get_failed_papers()
    if failed:
        print("\nFailed to download:")
        for paper in failed:
            print(f"  - {paper['title']}")


if __name__ == "__main__":
    asyncio.run(main())

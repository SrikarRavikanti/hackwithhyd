"""
Connector Adapter Base Class
Simulates external integration sources (Support, Reviews, Surveys, Sales Calls, Interviews).
Each connector implements: fetch(), normalize(), ingest().
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseConnector(ABC):
    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    def fetch(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch raw feedback from external source."""
        pass

    @abstractmethod
    def normalize(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Normalize raw external payload into standard Feedback Memory schema."""
        pass

    def ingest(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Fetch and normalize records ready for Hindsight retention."""
        raw = self.fetch(limit)
        return self.normalize(raw)

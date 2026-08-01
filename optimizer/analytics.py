"""OPTIMIZER Agent — Performance tracking with Gemini API."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional
from collections import defaultdict

import gemini_client


class PerformanceTracker:
    """Track Etsy performance with Gemini-powered optimization recommendations."""

    def __init__(self, data_dir: str = "data/analytics"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.data_dir / "performance_history.jsonl"

    def log_listing(self, listing_id: str, metrics: dict):
        """Log daily metrics for a listing."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "listing_id": listing_id,
            **metrics
        }
        with open(self.history_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def get_listing_trend(self, listing_id: str, days: int = 7) -> dict:
        """Get performance trend for a listing."""
        metrics = defaultdict(list)

        with open(self.history_file) as f:
            for line in f:
                entry = json.loads(line.strip())
                if entry["listing_id"] == listing_id:
                    for key, value in entry.items():
                        if key not in ["timestamp", "listing_id"]:
                            metrics[key].append(value)

        trends = {}
        for key, values in metrics.items():
            if len(values) >= 2:
                recent = values[-days:]
                older = values[:-days] if len(values) > days else values[:len(values)//2]
                avg_recent = sum(recent) / len(recent)
                avg_older = sum(older) / len(older) if older else 0
                trends[key] = ((avg_recent - avg_older) / avg_older * 100) if avg_older > 0 else (100 if avg_recent > 0 else 0)
        return trends

    def run_council_optimization(self, listings_data: list[dict]) -> list[dict]:
        """Run Gemini-powered optimization recommendations."""
        prompt = f"""Analyze these Etsy listing performances and recommend optimizations:

{json.dumps(listings_data, indent=2)}

For each listing with declining metrics, provide:
1. Diagnosis (what's wrong)
2. Specific action (title change, new tags, price adjustment, new images)
3. Priority (high/medium/low)
4. Expected impact

Return as JSON array with: listing_id, diagnosis, action, priority, expected_impact"""

        result = gemini_client.generate_json(prompt)
        if isinstance(result, list):
            return result
        if isinstance(result, dict) and "error" not in result:
            return [result]
        return [{"error": "Failed to parse optimization output", "raw": str(result)}]

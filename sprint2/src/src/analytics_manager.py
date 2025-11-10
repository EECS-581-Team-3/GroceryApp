from datetime import datetime
from statistics import mean

class AnalyticsManager:
    def __init__(self):
        self.usage_history = {}

    def record_change(self, item_name: str, new_qty: int):
        """Record each time an item's quantity changes."""
        key = item_name.strip().lower()
        self.usage_history.setdefault(key, []).append((datetime.now(), new_qty))

    def most_used_items(self):
        """
        Returns items that go out of stock most frequently.
        """
        usage_counts = {
            name: sum(1 for _, q in history if q == 0)
            for name, history in self.usage_history.items()
        }
        if not usage_counts:
            return []
        max_outs = max(usage_counts.values())
        return [n for n, c in usage_counts.items() if c == max_outs]

    def average_stock_level(self, inventory):
        """Compute average quantity per item."""
        if not inventory.items:
            return 0
        return mean(item.quantity for item in inventory.items.values())

    def restock_recommendations(self, inventory):
        """
        Suggests items likely needing restock soon.
        Logic: Items trending toward zero or repeatedly out of stock.
        """
        recommendations = []
        for name, history in self.usage_history.items():
            if len(history) >= 2:
                # Compare last two records
                prev_qty = history[-2][1]
                curr_qty = history[-1][1]
                if curr_qty < prev_qty and curr_qty <= 2:
                    recommendations.append(name)
        # Add any currently out-of-stock items
        recommendations += [item.name for item in inventory.list_out_of_stock()]
        return sorted(set(recommendations))

    def summary_report(self, inventory):
        """Return analytics summary as dict."""
        return {
            "total_items": len(inventory.items),
            "avg_stock": round(self.average_stock_level(inventory), 2),
            "most_used": self.most_used_items(inventory),
            "recommendations": self.restock_recommendations(inventory),
        }

    def __repr__(self):
        return f"AnalyticsManager({len(self.usage_history)} tracked items)"
from dataclasses import dataclass, field
from typing import Any
import re

from src.businesspilot.schemas import BusinessRequest


@dataclass
class BusinessState:
    request: BusinessRequest
    research_data: dict[str, Any] = field(default_factory=dict)
    strategy_data: dict[str, Any] = field(default_factory=dict)
    finance_data: dict[str, Any] = field(default_factory=dict)
    execution_data: dict[str, Any] = field(default_factory=dict)
    messages: list[dict[str, Any]] = field(default_factory=list)
    evaluation_feedback: list[str] = field(default_factory=list)
    evaluation_data: dict[str, Any] = field(default_factory=dict)
    current_stage: str = "initialized"
    revision_count: int = 0

    def add_message(self, sender: str, receiver: str, content: dict):
        self.messages.append({
            "sender": sender,
            "receiver": receiver,
            "content": content,
            "status": "completed",
        })

    def update_stage(self, stage: str):
        self.current_stage = stage

    def add_feedback(self, feedback: str):
        self.evaluation_feedback.append(feedback)

    def add_strategy(self, strategy: str, action: str, priority: str = "Medium",
                     source_agent: str = "Strategy Agent"):
        """Add a strategy once; return its stable task ID."""
        normalized = re.sub(r"\s+", " ", strategy.strip().lower())
        strategies = self.strategy_data.setdefault("strategies", [])
        for item in strategies:
            existing = re.sub(r"\s+", " ", item["strategy"].strip().lower())
            if existing == normalized:
                return item["task_id"]

        task_id = f"T{len(strategies) + 1:03d}"
        strategies.append({
            "task_id": task_id,
            "strategy": strategy.strip(),
            "action": action,
            "priority": priority,
            "source_agent": source_agent,
        })
        return task_id

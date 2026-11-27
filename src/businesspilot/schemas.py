from dataclasses import dataclass
from enum import Enum


class BusinessType(str, Enum):
    RETAIL = "retail"
    RESTAURANT = "restaurant"
    STARTUP = "startup"
    FREELANCER = "freelancer"
    ECOMMERCE = "ecommerce"
    OTHER = "other"


@dataclass
class BusinessProfile:
    name: str
    business_type: BusinessType
    description: str
    location: str = "Not provided"


@dataclass
class BusinessRequest:
    profile: BusinessProfile
    problem: str
    budget: float
    goal: str
    duration_days: int = 30

    def __post_init__(self):
        if not self.profile.name.strip():
            raise ValueError("Business name is required.")
        if not self.problem.strip():
            raise ValueError("Business problem is required.")
        if not self.goal.strip():
            raise ValueError("Business goal is required.")
        if self.budget < 0:
            raise ValueError("Budget cannot be negative.")
        if self.duration_days <= 0:
            raise ValueError("Duration must be greater than zero.")

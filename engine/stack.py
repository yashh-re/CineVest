def stack_summary(budget: int, sources: dict[str, int]) -> dict:
    """Compare funding sources against the budget. All amounts in cents."""
    if budget <= 0:
        raise ValueError("Budget must be more than zero")
    funded = sum(sources.values())
    return {
        "funded": funded,
        "still_needed": max(budget - funded, 0),
        "over_funded": max(funded - budget, 0),
        "percent_funded": funded / budget,
    }
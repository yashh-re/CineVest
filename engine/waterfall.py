def pay_tier(cash: int, owed: int) -> tuple[int, int]:
    """Pay off as of 'owed' as 'cash' allows. Returns (paid, cash_left)."""
    paid = min(cash, owed)
    return paid, cash - paid

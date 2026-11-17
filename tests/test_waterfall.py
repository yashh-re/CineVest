from engine.waterfall import pay_tier


def test_pays_in_full_when_cash_is_enough():
    assert pay_tier(cash=100, owed=60) == (60, 40)


def test_pays_what_it_can_when_cash_is_short():
    assert pay_tier(cash=50, owed=60) == (50, 0)
    
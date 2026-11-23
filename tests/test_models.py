import pytest

from engine.models import Tier


def test_typo_in_field_name_is_caught():
    with pytest.raises(ValueError, match="principle"):
        Tier.from_dict({"name": "Gap loan", "kind": "recoup",
                        "principle": 100, "multiple": 1.1})


def test_missing_field_is_caught():
    with pytest.raises(ValueError, match="missing 'multiple'"):
        Tier.from_dict({"name": "Gap loan", "kind": "recoup", "principal": 100})


def test_parties_become_party_objects():
    tier = Tier.from_dict({
        "name": "Equity", "kind": "pari_passu",
        "parties": [{"name": "Investor A", "principal": 100, "multiple": 1.2}],
    })
    assert tier.parties[0].name == "Investor A"
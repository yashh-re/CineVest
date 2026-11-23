from dataclasses import dataclass

# Which fields each kind of tier must have.
REQUIRED_FIELDS = {
    "percent_of_gross": ["value"],
    "fixed": ["value"],
    "share_of_remaining": ["value"],
    "recoup": ["principal", "multiple"],
    "pari_passu": ["parties"],
}


@dataclass
class Party:
    """One investor or lender inside a pari passu tier."""
    name: str
    principal: int
    multiple: float


@dataclass
class Tier:
    """One step in the waterfall."""
    name: str
    kind: str
    value: float | None = None
    principal: int | None = None
    multiple: float | None = None
    parties: list[Party] | None = None

    def __post_init__(self):
        """Runs automatically after a Tier is created: checks it makes sense."""
        if self.kind not in REQUIRED_FIELDS:
            raise ValueError(f"Tier '{self.name}': unknown kind '{self.kind}'")
        for field_name in REQUIRED_FIELDS[self.kind]:
            if getattr(self, field_name) is None:
                raise ValueError(
                    f"Tier '{self.name}' ({self.kind}) is missing '{field_name}'"
                )

    @classmethod
    def from_dict(cls, data: dict) -> "Tier":
        """Build a Tier from a dictionary, such as one loaded from JSON."""
        data = dict(data)  # copy, so we don't change the caller's dictionary
        try:
            if data.get("parties") is not None:
                data["parties"] = [Party(**p) for p in data["parties"]]
            return cls(**data)
        except TypeError as error:
            raise ValueError(f"Tier '{data.get('name', '?')}': {error}") from None
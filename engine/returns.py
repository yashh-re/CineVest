def moic(received: int, invested: int) -> float:
    """Multiple on invested capital: total received divided by total invested.

    1.0 means the investor got exactly their money back; 2.0 means double.
    """
    if invested <= 0:
        raise ValueError("Invested amount must be more than zero")
    return received / invested

def price_str_repr(price: float) -> str:
    """Convert float odds to their string representation.

    Args:
        odds: Price in floating representation.

    Returns:
        String representation of the odds.

    Examples:

        >>> price_str_repr(1.2)
        '1.20'
        >>> price_str_repr(4.0)
        '4.0'
        >>> price_str_repr(7.0)
        '7.0'
        >>> price_str_repr(200.0)
        '200'
    """
    if price == 0.0:
        return '0.0'  # Price 0.0 is a special price transmitted by Betfair
    if price < 1.01:
        raise ValueError(f"Price: {price}. Prices cannot be lower than 1.01.")
    elif 1.01 <= price < 4.0:
        return "{:.2f}".format(price)
    elif 4.0 <= price < 20.:
        return "{:.1f}".format(price)
    elif 20. <= price <= 1000.:
        return "{:.0f}".format(price)
    else:
        raise ValueError(f"Price: {price}. Prices cannot be higher than 1000.")

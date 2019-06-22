def odds_str_repr(odds: float) -> str:
    """Convert float odds to their string representation.

    Args:
        odds: Odds in floating representation.

    Returns:
        String representation of the odds.

    Examples:

        >>> odds_str_repr(1.2)
        '1.20'
        >>> odds_str_repr(4.0)
        '4.0'
        >>> odds_str_repr(7.0)
        '7.0'
        >>> odds_str_repr(200.0)
        '200'
    """
    if odds < 1.01:
        raise ValueError("Prices cannot be lower than 1.01.")
    elif 1.01 <= odds < 4.0:
        return "{:.2f}".format(odds)
    elif 4.0 <= odds < 20.:
        return "{:.1f}".format(odds)
    elif 20. <= odds <= 1000.:
        return "{:.0f}".format(odds)
    else:
        raise ValueError("Prices cannot be higher than 1000.")

def convert_units(value: float, from_unit: str, to_unit: str) -> str:
    units = {
        "mm": ("length", 0.001),
        "cm": ("length", 0.01),
        "m": ("length", 1.0),
        "km": ("length", 1000.0),
        "in": ("length", 0.0254),
        "ft": ("length", 0.3048),
        "yd": ("length", 0.9144),
        "mi": ("length", 1609.344),
        "mg": ("mass", 0.000001),
        "g": ("mass", 0.001),
        "kg": ("mass", 1.0),
        "oz": ("mass", 0.028349523125),
        "lb": ("mass", 0.45359237),
    }

    source = from_unit.lower()
    target = to_unit.lower()

    if source not in units:
        raise ValueError(f"Unsupported from_unit: {from_unit}")
    if target not in units:
        raise ValueError(f"Unsupported to_unit: {to_unit}")

    source_type, source_multiplier = units[source]
    target_type, target_multiplier = units[target]

    if source_type != target_type:
        raise ValueError(f"Cannot convert {source_type} to {target_type}")

    result = value * source_multiplier / target_multiplier
    return str(result)

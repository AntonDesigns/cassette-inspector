# Mapper module — NEO raw value translation only.
# Translates NEO 2000 series raw integers (0-9) to SlotOccupationState (0-6).
# NEO UV series already outputs SlotOccupationState directly, no translation needed.

NEO_2000_MAP = {
    0: 1,  # not exist  -> Empty
    1: 3,  # exists     -> CorrectlyOccupied
    2: 2,  # thick      -> NotEmpty
    3: 5,  # cross      -> CrossSlotted
    4: 5,  # bow/lift   -> CrossSlotted
    7: 4,  # multiple   -> DoubleSlotted
    8: 2,  # thin       -> NotEmpty
    9: 0,  # failure    -> Undefined
}

def translate_neo_2000(raw_values: list) -> list:
    return [NEO_2000_MAP.get(v, 0) for v in raw_values]

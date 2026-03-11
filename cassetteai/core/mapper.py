# I handle NEO 2000 raw value translation here and nothing else.
# This is pure data transformation. No I/O, no imports, no side effects.
#
# The NEO 2000 series outputs raw integers 0-9 which mean something
# different from the SlotOccupationState standard Trymax uses everywhere else.
# I translate them here before anything gets written to inspections.csv.
#
# The NEO UV series already outputs SlotOccupationState 0-6 directly
# so it never needs to come through here.
#
# Translation table from the handoff document:
#   0 (not exist)  -> 1  (Empty)
#   1 (exists)     -> 3  (CorrectlyOccupied)
#   2 (thick)      -> 2  (Indeterminate)
#   3 (cross)      -> 5  (CrossSlotted)
#   4 (bow/lift)   -> 5  (CrossSlotted)
#   7 (multiple)   -> 4  (MissingWafer)
#   8 (thin)       -> 2  (Indeterminate)
#   9 (failure)    -> 0  (NoWafer)
#   anything else  -> 0  (NoWafer) as a safe fallback
#
# SlotOccupationState reference:
#   0 = NoWafer
#   1 = Empty
#   2 = Indeterminate
#   3 = CorrectlyOccupied
#   4 = MissingWafer
#   5 = CrossSlotted
#   6 = DoubleSlotted

NEO_2000_MAP = {
    0: 1,
    1: 3,
    2: 2,
    3: 5,
    4: 5,
    7: 4,
    8: 2,
    9: 0,
}


def translate_neo_2000(raw_values: list) -> list:
    # Take a list of raw NEO 2000 integers and return a list of
    # SlotOccupationState integers. I map unknown values to 0 (NoWafer)
    # so the app never crashes on unexpected mapper output.
    return [NEO_2000_MAP.get(v, 0) for v in raw_values]

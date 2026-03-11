// Constants only.
var SLOT_STATES = {
    0: { name: "NoWafer",            color: "#444444" },
    1: { name: "Empty",              color: "#222222" },
    2: { name: "Indeterminate",      color: "#f59e0b" },
    3: { name: "CorrectlyOccupied",  color: "#14b8a6" },
    4: { name: "MissingWafer",       color: "#ef4444" },
    5: { name: "CrossSlotted",       color: "#f97316" },
    6: { name: "DoubleSlotted",      color: "#8b5cf6" },
};

var CONFIDENCE = {
    HIGH: 0.90,
    LOW:  0.70,
    COLOR_HIGH:   "#22c55e",
    COLOR_MEDIUM: "#f59e0b",
    COLOR_LOW:    "#ef4444",
};

var APP_CONFIG = {
    SLOT_COUNT:     25,
    TOAST_DURATION: 1600,
    LABELER_URL:    "http://localhost:5050",
};

// Single source of truth for slot states and app constants.
// Same pattern as the slot labeler config.js.

var SLOT_STATES = {
  0: { name: "Undefined",         cls: "s-undef",    icon: "?" },
  1: { name: "Empty",             cls: "s-empty",    icon: "○" },
  2: { name: "NotEmpty",          cls: "s-notempty", icon: "◐" },
  3: { name: "CorrectlyOccupied", cls: "s-occupied", icon: "●" },
  4: { name: "DoubleSlotted",     cls: "s-double",   icon: "◉" },
  5: { name: "CrossSlotted",      cls: "s-cross",    icon: "✕" },
  6: { name: "Reserved",          cls: "s-reserved", icon: "-" },
};

var APP_CONFIG = {
  SLOT_COUNT:     25,
  TOAST_DURATION: 1600,
  LABELER_URL:    "http://localhost:5050",
};

// Single shared State object. Every module reads from here.
// No module creates its own copy of any of these values.
// If I need to add a new piece of shared state, I add it here.

var State = {
    engineer:      null,   // Resolved engineer name from Windows username or dropdown
    cameraActive:  false,  // True when the webcam feed is running
    lastResult:    null,   // Last prediction result from /api/snapshot or /api/predict
    history:       [],     // Array of recent inspections for the history panel
    gradcamActive: false,  // True when the Grad-CAM overlay is toggled on
    mapperSlots:   null,   // Last mapper slot values for the comparison panel
};

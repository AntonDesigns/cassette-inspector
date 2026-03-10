// Single shared State object for all runtime data.
// Every module reads from here. Nobody creates their own copy.

var State = {
  engineer:     null,
  cameraActive: false,
  lastResult:   null,
  history:      [],
};

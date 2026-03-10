// Inspect-level actions: trigger snapshot, accept result, flag for review.
// Calls API and updates State. No DOM manipulation here.
var InspectActions = {
  snapshot:     async function() {},
  flagForReview: function(cropPath) {
    // Opens the slot labeler deep link with the flagged crop and engineer name.
    var params = "crop=" + encodeURIComponent(cropPath) + "&engineer=" + encodeURIComponent(State.engineer || "");
    window.open(APP_CONFIG.LABELER_URL + "?" + params);
  },
};

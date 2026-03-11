// Inspection-level actions: snapshot, accept result, flag for review.

var InspectActions = {
    snapshot: function() {
        Toast.show("Capturing...", "info");
        API.snapshot()
            .then(function(data) {
                State.lastResult = data;
                State.history.unshift({
                    timestamp_utc: new Date().toISOString(),
                    final_status:  "pending",
                    ai_slots:      data.slots,
                });

                Overlay.render(data.slots, data.confidence);
                Comparison.render(data.slots, State.mapperSlots);
                History.render();

                var ms = data.inference_ms || 0;
                document.getElementById("inference-time").textContent = "Last: " + ms + "ms";
                Toast.show("Snapshot complete", "success");
            })
            .catch(function() {
                Toast.show("Snapshot failed", "error");
            });
    },

    flagForReview: function() {
        if (!State.lastResult) {
            Toast.show("No result to flag", "error");
            return;
        }
        var cropPath = State.lastResult.crop_image_path || "";
        var params = "crop=" + encodeURIComponent(cropPath)
                   + "&engineer=" + encodeURIComponent(State.engineer || "");
        window.open(APP_CONFIG.LABELER_URL + "?" + params);
        Toast.show("Opening slot labeler...", "info");
    },

};

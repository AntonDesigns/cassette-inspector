// Review-level actions: confirm AI predictions, correct slots, submit ground truth.
var ReviewActions = {
    confirm: function() {
        if (!State.lastResult) {
            Toast.show("Nothing to confirm", "error");
            return;
        }

        var inspectionId = State.lastResult.inspection_id;
        var slots = State.lastResult.slots;

        API.confirm(inspectionId, slots, State.engineer)
            .then(function() {
                Toast.show("Confirmed", "success");
                if (State.history.length > 0) {
                    State.history[0].final_status = "reviewed";
                    History.render();
                }
            })
            .catch(function() {
                Toast.show("Confirm failed", "error");
            });
    },

    correctSlot: function(slotIndex, newState) {
        if (!State.lastResult || !State.lastResult.slots) return;
        State.lastResult.slots[slotIndex] = newState;
        Overlay.render(State.lastResult.slots, State.lastResult.confidence);
        Comparison.render(State.lastResult.slots, State.mapperSlots);
    },

};

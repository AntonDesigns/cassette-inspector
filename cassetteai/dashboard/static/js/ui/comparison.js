// AI vs Mapper side-by-side comparison panel.
var Comparison = {
    render: function(aiSlots, mapperSlots) {
        Comparison._renderGrid("ai-grid", aiSlots);
        Comparison._renderGrid("mapper-grid", mapperSlots);
    },

    clear: function() {
        Comparison._renderGrid("ai-grid", null);
        Comparison._renderGrid("mapper-grid", null);
    },

    _renderGrid: function(elementId, slots) {
        var el = document.getElementById(elementId);
        if (!el) return;
        el.innerHTML = "";

        for (var i = 0; i < APP_CONFIG.SLOT_COUNT; i++) {
            var state = slots ? (slots[i] || 0) : 0;
            var stateInfo = SLOT_STATES[state] || SLOT_STATES[0];

            var cell = document.createElement("div");
            cell.className = "comparison-slot";
            cell.style.backgroundColor = stateInfo.color;
            cell.title = "Slot " + (i + 1) + ": " + stateInfo.name;
            cell.textContent = i + 1;

            el.appendChild(cell);
        }
    },
};

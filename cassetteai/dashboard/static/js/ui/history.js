// Session history list.
var History = {
    render: function() {
        var list = document.getElementById("history-list");
        if (!list) return;
        list.innerHTML = "";

        if (!State.history || State.history.length === 0) {
            var empty = document.createElement("li");
            empty.className = "history-empty";
            empty.textContent = "No inspections yet this session.";
            list.appendChild(empty);
            return;
        }

        State.history.forEach(function(entry) {
            var li = document.createElement("li");
            li.className = "history-item";

            var time = document.createElement("span");
            time.className = "history-time";
            time.textContent = entry.timestamp_utc
                ? entry.timestamp_utc.replace("T", " ").substring(0, 19)
                : "";

            var status = document.createElement("span");
            status.className = "history-status history-status-" + (entry.final_status || "pending");
            status.textContent = entry.final_status || "pending";

            var slots = document.createElement("span");
            slots.className = "history-slots";
            if (entry.ai_slots && entry.ai_slots.length) {
                var occupied = entry.ai_slots.filter(function(s) { return s === 3; }).length;
                slots.textContent = occupied + "/25 occupied";
            }
            li.appendChild(time);
            li.appendChild(status);
            li.appendChild(slots);
            list.appendChild(li);
        });
    },
};

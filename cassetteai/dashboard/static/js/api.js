var API = {

    snapshot: function() {
        return fetch("/api/snapshot", { method: "POST" })
            .then(function(r) { return r.json(); });
    },

    predict: function(imageB64, machineType) {
        return fetch("/api/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_b64: imageB64, machine_type: machineType }),
        }).then(function(r) { return r.json(); });
    },

    explain: function(imageB64) {
        return fetch("/api/explain", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image_b64: imageB64 }),
        }).then(function(r) { return r.json(); });
    },

    confirm: function(inspectionId, slots, engineer) {
        return fetch("/api/confirm", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                inspection_id: inspectionId,
                slots: slots,
                engineer: engineer,
            }),
        }).then(function(r) { return r.json(); });
    },

    status: function() {
        return fetch("/api/status")
            .then(function(r) { return r.json(); });
    },
};

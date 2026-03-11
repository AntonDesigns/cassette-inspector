// 25-slot prediction overlay drawn on the canvas above the camera feed.

var Overlay = {
    render: function(slots, confidence) {
        var canvas = document.getElementById("overlay-canvas");
        if (!canvas) return;
        var video = document.getElementById("camera-feed");
        canvas.width = video.videoWidth || canvas.offsetWidth;
        canvas.height = video.videoHeight || canvas.offsetHeight;

        var ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        var cols = 5;
        var rows = 5;
        var slotW = canvas.width / (cols + 1);
        var slotH = canvas.height / (rows + 1);
        var radius = Math.min(slotW, slotH) * 0.35;

        for (var i = 0; i < APP_CONFIG.SLOT_COUNT; i++) {
            var col = i % cols;
            var row = Math.floor(i / cols);
            var x = slotW * (col + 1);
            var y = slotH * (row + 1);

            var conf = confidence ? confidence[i] : 1;
            var state = slots ? slots[i] : 0;
            var stateColor = (SLOT_STATES[state] || SLOT_STATES[0]).color;
            var borderColor = Overlay._confidenceColor(conf);
            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fillStyle = stateColor;
            ctx.fill();
            ctx.strokeStyle = borderColor;
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.fillStyle = "#ffffff";
            ctx.font = "bold " + Math.round(radius * 0.7) + "px sans-serif";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(i + 1, x, y);
        }
    },

    clear: function() {
        var canvas = document.getElementById("overlay-canvas");
        if (!canvas) return;
        canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
    },

    _confidenceColor: function(conf) {
        if (conf >= CONFIDENCE.HIGH) return CONFIDENCE.COLOR_HIGH;
        if (conf >= CONFIDENCE.LOW)  return CONFIDENCE.COLOR_MEDIUM;
        return CONFIDENCE.COLOR_LOW;
    },
};

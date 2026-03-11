// Grad-CAM heatmap overlay toggle.
var GradCAMUI = {
    show: function(heatmapB64) {
        var img = document.getElementById("gradcam-overlay");
        if (!img) return;
        img.src = "data:image/jpeg;base64," + heatmapB64;
        img.style.display = "block";
        State.gradcamActive = true;
    },

    hide: function() {
        var img = document.getElementById("gradcam-overlay");
        if (!img) return;
        img.style.display = "none";
        img.src = "";
        State.gradcamActive = false;
    },

    toggle: function() {
        if (State.gradcamActive) {
            GradCAMUI.hide();
            return;
        }

        var imageB64 = CameraUI.captureFrame();
        if (!imageB64) {
            Toast.show("No camera frame available", "error");
            return;
        }

        API.explain(imageB64)
            .then(function(data) {
                if (data.heatmap_b64) {
                    GradCAMUI.show(data.heatmap_b64);
                    Toast.show("Grad-CAM active", "info");
                }
            })
            .catch(function() {
                Toast.show("Grad-CAM failed", "error");
            });
    },
};

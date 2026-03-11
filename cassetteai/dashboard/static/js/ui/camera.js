// Live webcam feed using getUserMedia.
var CameraUI = {
    start: function() {
        var video = document.getElementById("camera-feed");
        if (!video) return;

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
                State.cameraActive = true;
                Toast.show("Camera started", "success");
            })
            .catch(function(err) {
                State.cameraActive = false;
                Toast.show("Camera not available: " + err.message, "error");
            });
    },

    stop: function() {
        var video = document.getElementById("camera-feed");
        if (!video || !video.srcObject) return;
        video.srcObject.getTracks().forEach(function(t) { t.stop(); });
        video.srcObject = null;
        State.cameraActive = false;
    },

    captureFrame: function() {
        var video = document.getElementById("camera-feed");
        if (!video) return null;
        var canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext("2d").drawImage(video, 0, 0);
        return canvas.toDataURL("image/jpeg").split(",")[1];
    },
};

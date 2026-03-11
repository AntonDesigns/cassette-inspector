// Boot only. 
(function() {

    function init() {
        Theme.init();
        resolveEngineer();
        CameraUI.start();
        checkStatus();
        wireEvents();
    }

    function resolveEngineer() {
        // Try to read the engineer name from the URL parameter first.
        var params = new URLSearchParams(window.location.search);
        var nameFromUrl = params.get("engineer");

        if (nameFromUrl) {
            State.engineer = nameFromUrl;
            setEngineerDisplay(nameFromUrl);
            return;
        }
        fetch("/api/status")
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (data.engineer) {
                    State.engineer = data.engineer;
                    setEngineerDisplay(data.engineer);
                } else {
                    showEngineerDropdown();
                }
            })
            .catch(function() {
                showEngineerDropdown();
            });
    }

    function setEngineerDisplay(name) {
        var badge = document.getElementById("engineer-name");
        if (badge) badge.textContent = name;
        var screen = document.getElementById("engineer-select-screen");
        if (screen) screen.style.display = "none";
    }

    function showEngineerDropdown() {
        var screen = document.getElementById("engineer-select-screen");
        if (screen) screen.style.display = "flex";
    }

    function checkStatus() {
        API.status()
            .then(function(data) {
                var modelEl = document.getElementById("model-status");
                var cameraEl = document.getElementById("camera-status");
                if (modelEl) modelEl.textContent = "Model: " + (data.model_loaded ? "ready" : "not loaded");
                if (cameraEl) cameraEl.textContent = "Camera: " + (data.camera_connected ? "connected" : "not found");
            })
            .catch(function() {
                Toast.show("Could not reach backend", "error");
            });
    }

    function wireEvents() {
        document.addEventListener("click", function(e) {
            var action = e.target.getAttribute("data-action");
            if (!action) return;

            switch (action) {
                case "snapshot":        InspectActions.snapshot();     break;
                case "toggle-gradcam":  GradCAMUI.toggle();            break;
                case "flag-review":     InspectActions.flagForReview(); break;
                case "confirm":         ReviewActions.confirm();        break;
                case "toggle-theme":    Theme.toggle();                break;
                case "confirm-engineer":
                    var dropdown = document.getElementById("engineer-dropdown");
                    if (dropdown && dropdown.value) {
                        State.engineer = dropdown.value;
                        setEngineerDisplay(dropdown.value);
                    }
                    break;
            }
        });
    }
    document.addEventListener("DOMContentLoaded", init);
})();

// Timed toast notifications. 
var Toast = {
    show: function(message, type) {
        var el = document.getElementById("toast");
        if (!el) return;
        el.textContent = message;
        el.className = "toast toast-" + (type || "info") + " toast-visible";
        clearTimeout(Toast._timer);
        Toast._timer = setTimeout(function() {
            el.className = "toast";
        }, APP_CONFIG.TOAST_DURATION);
    },
    _timer: null,
};

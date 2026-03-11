// Dark and light theme toggle.

var Theme = {
    toggle: function() {
        var html = document.documentElement;
        var current = html.getAttribute("data-theme");
        var next = current === "dark" ? "light" : "dark";
        html.setAttribute("data-theme", next);
        Theme._updateLogo(next);
    },

    _updateLogo: function(theme) {
        var body = document.body;
        var logo = document.querySelector(".logo");
        if (!logo) return;
        var src = theme === "dark"
            ? body.getAttribute("data-logo-dark")
            : body.getAttribute("data-logo-light");
        if (src) logo.src = src;
    },

    init: function() {
        var current = document.documentElement.getAttribute("data-theme") || "dark";
        Theme._updateLogo(current);
    },
};

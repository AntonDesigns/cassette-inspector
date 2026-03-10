// Every fetch() call lives here and nowhere else.
// When a route changes in main.py, this is the only JS file that needs updating.

var API = {

  predict: async function (imageB64) {
    var res = await fetch("/api/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ image_b64: imageB64 }),
    });
    return res.json();
  },

  explain: async function (imageB64) {
    var res = await fetch("/api/explain", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ image_b64: imageB64 }),
    });
    return res.json();
  },

  snapshot: async function () {
    var res = await fetch("/api/snapshot", { method: "POST" });
    return res.json();
  },

  confirm: async function (data) {
    var res = await fetch("/api/confirm", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(data),
    });
    return res.json();
  },

  status: async function () {
    var res = await fetch("/api/status");
    return res.json();
  },

};

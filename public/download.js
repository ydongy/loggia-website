// Reads the same update feed as the app and fills in the download button.
// The wording comes from data attributes on #download, so every language page shares this file.
(function () {
  var section = document.getElementById("download");
  if (!section) return;
  var d = section.dataset;
  function fill(s, v, os) { return s.replace("{v}", v).replace("{os}", os || ""); }
  var status = document.getElementById("status");
  fetch("https://dl.useloggia.com/latest.json", { cache: "no-store" })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (f) {
      if (!/^https:\/\//.test(f.url)) throw new Error("bad url");
      status.textContent = fill(f.minimumOS ? d.version : d.versionNoOs, f.version, f.minimumOS);
      var a = document.getElementById("download-button");
      a.href = f.url; a.textContent = fill(d.button, f.version); a.hidden = false;
      if (f.sha256) {
        document.getElementById("sha").textContent = "SHA-256: " + f.sha256;
        document.getElementById("checksum").hidden = false;
      }
    })
    .catch(function () { status.textContent = d.error; });
})();

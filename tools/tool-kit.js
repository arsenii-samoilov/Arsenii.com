/* tool-kit.js - shared helpers for the arsenii.com program management tools.
   ES5-safe vanilla JS, no dependencies. Exposes a single global: window.TK.
   Provides shareable links (URL hash), embed codes, and Excel / Word export,
   plus the buttons that wire them up, so every tool stays DRY. */
(function () {
  "use strict";

  function b64encode(str) { return btoa(unescape(encodeURIComponent(str))); }
  function b64decode(str) { return decodeURIComponent(escape(atob(str))); }

  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;")
      .replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function thisFile() {
    var path = location.pathname || "";
    var i = path.lastIndexOf("/");
    var f = i >= 0 ? path.substring(i + 1) : path;
    return f || "index.html";
  }

  function encodeState(obj) {
    try {
      location.hash = "#d=" + encodeURIComponent(b64encode(JSON.stringify(obj)));
      return true;
    } catch (e) { return false; }
  }

  function decodeState() {
    try {
      var h = location.hash || "";
      if (h.charAt(0) === "#") h = h.substring(1);
      if (h.indexOf("d=") !== 0) return null;
      var data = h.substring(2);
      if (!data) return null;
      return JSON.parse(b64decode(decodeURIComponent(data)));
    } catch (e) { return null; }
  }

  function isEmbed() {
    return /[?&]embed=1(?:&|$)/.test(location.search);
  }

  function flash(btn, msg) {
    if (!btn) return;
    if (!btn.getAttribute("data-tk-label")) {
      btn.setAttribute("data-tk-label", btn.textContent);
    }
    btn.textContent = msg;
    setTimeout(function () {
      btn.textContent = btn.getAttribute("data-tk-label");
    }, 1500);
  }

  function copyText(text, btn, msg) {
    function done() { flash(btn, msg || "Copied"); }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); done(); } catch (e) {}
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(done, fallback);
    } else { fallback(); }
  }

  function download(filename, content, mime) {
    var blob = new Blob([content], { type: mime });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  function exportExcel(filename, header, rows) {
    var html = '<html xmlns:o="urn:schemas-microsoft-com:office:office" ' +
      'xmlns:x="urn:schemas-microsoft-com:office:excel" ' +
      'xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="utf-8">' +
      '<!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet>' +
      '<x:Name>Sheet1</x:Name><x:WorksheetOptions><x:DisplayGridlines/>' +
      '</x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook>' +
      '</xml><![endif]--></head><body><table border="1">';
    var i, j;
    if (header && header.length) {
      html += "<tr>";
      for (i = 0; i < header.length; i++) html += "<th>" + esc(header[i]) + "</th>";
      html += "</tr>";
    }
    rows = rows || [];
    for (i = 0; i < rows.length; i++) {
      html += "<tr>";
      for (j = 0; j < rows[i].length; j++) html += "<td>" + esc(rows[i][j]) + "</td>";
      html += "</tr>";
    }
    html += "</table></body></html>";
    if (!/\.xls$/i.test(filename)) filename += ".xls";
    download(filename, html, "application/vnd.ms-excel");
  }

  function exportWord(filename, htmlString) {
    var doc = '<html xmlns:o="urn:schemas-microsoft-com:office:office" ' +
      'xmlns:w="urn:schemas-microsoft-com:office:word" ' +
      'xmlns="http://www.w3.org/TR/REC-html40"><head><meta charset="utf-8">' +
      '<title>Document</title><style>body{font-family:Calibri,Arial,sans-serif;' +
      'font-size:11pt;color:#1a1a1a;}h1,h2,h3{font-family:Georgia,serif;}' +
      'table{border-collapse:collapse;}td,th{border:1px solid #999;padding:6px;}' +
      '</style></head><body>' + htmlString + '</body></html>';
    if (!/\.doc$/i.test(filename)) filename += ".doc";
    download(filename, doc, "application/msword");
  }

  var CSS = [
    "body.tk-embed .site-header,",
    "body.tk-embed .tool-explainer,",
    "body.tk-embed .tool-cta,",
    "body.tk-embed .site-footer,",
    "body.tk-embed .tk-share,",
    "body.tk-embed .tk-embed-btn,",
    "body.tk-embed .tk-embed-panel { display: none !important; }",
    "body.tk-embed .tool-wrap { padding-top: 1.25rem; padding-bottom: 1.25rem; }",
    "body.tk-embed .tool-hero { margin-bottom: 1.5rem; }",
    ".tk-attribution { text-align: center; font-family: var(--font-sans); font-size: 0.78rem; margin: 1.75rem 0 0; color: #94a3b8; }",
    ".tk-attribution a { color: var(--accent); text-decoration: none; }",
    "body:not(.tk-embed) .tk-attribution { display: none; }",
    ".tk-embed-panel { max-width: 760px; margin: -0.5rem auto 1.5rem; border: 1px solid var(--accent-light); border-radius: 8px; padding: 1rem; background: var(--bg-warm); }",
    ".tk-embed-panel textarea { width: 100%; box-sizing: border-box; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.78rem; line-height: 1.5; border: 1px solid var(--accent-light); border-radius: 6px; padding: 0.6rem; min-height: 5.5rem; resize: vertical; color: var(--text); background: #fff; }",
    ".tk-embed-actions { margin-top: 0.6rem; display: flex; justify-content: flex-end; }",
    "@media print { .tk-share, .tk-embed-btn, .tk-embed-panel, .tk-attribution { display: none !important; } }"
  ].join("\n");

  function injectCss() {
    var s = document.createElement("style");
    s.type = "text/css";
    s.appendChild(document.createTextNode(CSS));
    document.head.appendChild(s);
  }

  function mkBtn(label, cls) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "tool-btn" + (cls ? " " + cls : "");
    b.textContent = label;
    return b;
  }

  function setup(config) {
    config = config || {};
    var controls = document.querySelector(config.controlsSelector || ".tool-controls");
    var file = config.file || thisFile();
    var toolName = config.toolName || (document.title || "").split("|")[0]
      .replace(/^\s+|\s+$/g, "") || "tool";

    var wrap = document.querySelector(".tool-wrap");
    if (wrap && !document.querySelector(".tk-attribution")) {
      var attr = document.createElement("p");
      attr.className = "tk-attribution";
      attr.innerHTML = 'Made by <a href="https://arsenii.com/tools/" target="_blank" rel="noopener">arsenii.com</a>';
      wrap.appendChild(attr);
    }

    if (!controls) return;

    if (config.excel) {
      var xbtn = mkBtn("Export Excel");
      xbtn.addEventListener("click", function () {
        var d = config.excel.build() || {};
        exportExcel(config.excel.filename || "export", d.header, d.rows);
      });
      controls.appendChild(xbtn);
    }

    if (config.word) {
      var wbtn = mkBtn("Export Word");
      wbtn.addEventListener("click", function () {
        exportWord(config.word.filename || "document", config.word.build() || "");
      });
      controls.appendChild(wbtn);
    }

    var sbtn = mkBtn("Copy Share Link", "tk-share");
    sbtn.addEventListener("click", function () {
      if (config.getState) encodeState(config.getState());
      copyText(location.href, sbtn, "Link copied");
    });
    controls.appendChild(sbtn);

    var ebtn = mkBtn("Get Embed Code", "tk-embed-btn");
    controls.appendChild(ebtn);

    var snippet =
      '<iframe src="https://arsenii.com/tools/' + file + '?embed=1" width="100%" height="600" style="border:1px solid #e2e8f0;border-radius:8px;"></iframe>\n' +
      '<p>Free ' + toolName + ' by <a href="https://arsenii.com/tools/">Arsenii Samoilov</a></p>';

    var panel = document.createElement("div");
    panel.className = "tk-embed-panel";
    panel.style.display = "none";
    var ta = document.createElement("textarea");
    ta.readOnly = true;
    ta.value = snippet;
    ta.setAttribute("aria-label", "Embed code");
    panel.appendChild(ta);
    var actions = document.createElement("div");
    actions.className = "tk-embed-actions";
    var cbtn = mkBtn("Copy");
    cbtn.addEventListener("click", function () { ta.select(); copyText(snippet, cbtn, "Copied"); });
    actions.appendChild(cbtn);
    panel.appendChild(actions);
    controls.parentNode.insertBefore(panel, controls.nextSibling);

    ebtn.addEventListener("click", function () {
      var showing = panel.style.display !== "none";
      panel.style.display = showing ? "none" : "block";
      if (!showing) { ta.focus(); ta.select(); }
    });
  }

  injectCss();
  if (isEmbed() && document.body) {
    document.body.className += (document.body.className ? " " : "") + "tk-embed";
  }

  window.TK = {
    encodeState: encodeState,
    decodeState: decodeState,
    isEmbed: isEmbed,
    copyText: copyText,
    download: download,
    exportExcel: exportExcel,
    exportWord: exportWord,
    flash: flash,
    esc: esc,
    setup: setup
  };
})();

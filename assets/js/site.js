// Theme: system preference by default, manual toggle wins and is remembered.
(function () {
  var saved = localStorage.getItem("liftsmart-theme");
  if (saved === "light" || saved === "dark") document.documentElement.setAttribute("data-theme", saved);
  window.toggleTheme = function () {
    var root = document.documentElement, cur = root.getAttribute("data-theme");
    if (!cur) cur = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    var next = cur === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next); localStorage.setItem("liftsmart-theme", next);
  };
  // Language: remember the visitor's pick; close the menu on outside click.
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".lang-menu a");
    if (a) localStorage.setItem("liftsmart-lang", a.getAttribute("data-lang"));
    document.querySelectorAll("details.lang[open]").forEach(function (d) { if (!d.contains(e.target)) d.removeAttribute("open"); });
  });
})();

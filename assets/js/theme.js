// Manual light/dark toggle; system preference is the default until the
// visitor picks one.
(function () {
  var saved = localStorage.getItem("liftsmart-theme");
  if (saved === "light" || saved === "dark") {
    document.documentElement.setAttribute("data-theme", saved);
  }

  window.toggleTheme = function () {
    var root = document.documentElement;
    var current = root.getAttribute("data-theme");
    if (!current) {
      current = window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }
    var next = current === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem("liftsmart-theme", next);
  };
})();

// Screenshot carousel on the home page. Without JavaScript the slides are a scroll-snap row and the
// dots are links. This script stacks the slides and cross-fades between them instead (the class
// "fade"), so the screenshots' shadows never slide past the edges mid-transition. It adds the
// previous / next buttons, arrow keys and horizontal swipes. No autoplay.
(function () {
  var root = document.querySelector(".carousel");
  if (!root) return;
  var track = root.querySelector(".slides");
  var slides = root.querySelectorAll(".slide");
  var dots = root.querySelectorAll(".dots a");
  var prev = root.querySelector(".prev");
  var next = root.querySelector(".next");
  var current = 0;

  function show(i) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    current = i;
    for (var s = 0; s < slides.length; s++) {
      slides[s].classList.toggle("current", s === i);
      slides[s].setAttribute("aria-hidden", s === i ? "false" : "true");
    }
    for (var d = 0; d < dots.length; d++) {
      if (d === i) dots[d].setAttribute("aria-current", "true"); else dots[d].removeAttribute("aria-current");
    }
    prev.disabled = i === 0;
    next.disabled = i === slides.length - 1;
  }

  root.classList.add("fade");
  prev.hidden = false;
  next.hidden = false;
  prev.addEventListener("click", function () { show(current - 1); });
  next.addEventListener("click", function () { show(current + 1); });
  for (var d = 0; d < dots.length; d++) {
    dots[d].addEventListener("click", (function (i) {
      return function (e) { e.preventDefault(); show(i); };
    })(d));
  }
  track.addEventListener("keydown", function (e) {
    if (e.key === "ArrowLeft") { e.preventDefault(); show(current - 1); }
    if (e.key === "ArrowRight") { e.preventDefault(); show(current + 1); }
  });
  // A mostly horizontal swipe of 40px or more moves one slide; vertical drags still scroll the page.
  var startX = null, startY = 0;
  track.addEventListener("pointerdown", function (e) {
    if (e.pointerType === "mouse") return;
    startX = e.clientX; startY = e.clientY;
  });
  track.addEventListener("pointerup", function (e) {
    if (startX === null) return;
    var dx = e.clientX - startX, dy = e.clientY - startY;
    startX = null;
    if (Math.abs(dx) >= 40 && Math.abs(dx) > Math.abs(dy)) show(current + (dx < 0 ? 1 : -1));
  });
  track.addEventListener("pointercancel", function () { startX = null; });
  // A link to one of the slides (#shot-link and so on) opens on that slide.
  var hash = window.location.hash.slice(1);
  var start = 0;
  for (var s = 0; s < slides.length; s++) if (slides[s].id === hash) start = s;
  show(start);
  window.requestAnimationFrame(function () {
    window.requestAnimationFrame(function () { root.classList.add("ready"); });
  });
})();

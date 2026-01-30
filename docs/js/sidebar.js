// Toggle open/close when clicking section labels
document.querySelectorAll(".sidebar li > span").forEach((span) => {
  span.addEventListener("click", () => {
    span.parentElement.classList.toggle("open");
  });
});

// Auto-open current page path (doc-style)
const currentPath = window.location.pathname;

document.querySelectorAll(".sidebar a").forEach((link) => {
  if (currentPath.startsWith(new URL(link.href).pathname)) {
    let li = link.parentElement;
    while (li) {
      if (li.tagName === "LI") {
        li.classList.add("open");
      }
      li = li.parentElement;
    }
  }
});

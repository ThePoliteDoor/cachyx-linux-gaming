const currentPath = window.location.pathname.replace(/\/+$/, "");

// 1️⃣ Open ALL sidebar sections by default
document.querySelectorAll(".sidebar li").forEach((li) => {
  if (li.querySelector("ul")) {
    li.classList.add("open");
  }
});

// 2️⃣ Keep active page logic (auto-open correct path)
document.querySelectorAll(".sidebar a").forEach((link) => {
  const linkPath = new URL(link.href).pathname.replace(/\/+$/, "");

  if (currentPath === linkPath || currentPath.startsWith(linkPath + "/")) {
    let el = link.parentElement;

    while (el && !el.classList.contains("sidebar")) {
      if (el.tagName === "LI") {
        el.classList.add("open");
      }
      el = el.parentElement;
    }
  }
});

// 3️⃣ Allow user to manually close/open sections
document.querySelectorAll(".sidebar li > span").forEach((span) => {
  span.addEventListener("click", () => {
    span.parentElement.classList.toggle("open");
  });
});

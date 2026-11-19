const tabs = document.querySelectorAll("nav button");
for (const button of tabs) {
  button.addEventListener("click", () => {
    for (const tab of tabs) {
      const active = tab === button;
      tab.setAttribute("aria-current", String(active));
      document.getElementById(tab.getAttribute("aria-controls")).hidden = !active;
    }
  });
}
const segment = document.getElementById("segmento");
segment.addEventListener("change", () => {
  document.querySelectorAll("[data-segment]").forEach((panel, i) => {
    panel.hidden = segment.selectedIndex > 0 && segment.selectedIndex !== i + 1;
  });
});

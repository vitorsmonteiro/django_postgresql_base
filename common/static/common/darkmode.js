// Dark Mode Toggle Script
const darkModeSwitch = document.getElementById("darkModeSwitch");
const htmlElement = document.documentElement;

// Check for saved theme preference or system preference
const savedTheme = localStorage.getItem("theme");
const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)");

// Set initial theme
if (savedTheme) {
  htmlElement.setAttribute("data-bs-theme", savedTheme);
  darkModeSwitch.checked = savedTheme === "dark";
} else if (systemPrefersDark.matches) {
  htmlElement.setAttribute("data-bs-theme", "dark");
  darkModeSwitch.checked = true;
}

// Toggle theme on switch change
darkModeSwitch.addEventListener("change", () => {
  const newTheme = darkModeSwitch.checked ? "dark" : "light";
  htmlElement.setAttribute("data-bs-theme", newTheme);
  localStorage.setItem("theme", newTheme);
});

// Handle system theme changes
systemPrefersDark.addListener((e) => {
  if (!localStorage.getItem("theme")) {
    htmlElement.setAttribute("data-bs-theme", e.matches ? "dark" : "light");
    darkModeSwitch.checked = e.matches;
  }
});

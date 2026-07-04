document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll("[data-endpoint]");
  const statusEl = document.getElementById("status");
  const contentTypeEl = document.getElementById("contentType");
  const charsetEl = document.getElementById("charset");
  const locationEl = document.getElementById("location");
  const bodyEl = document.getElementById("body");

  buttons.forEach(button => {
    button.addEventListener("click", async () => {
      const endpoint = button.getAttribute("data-endpoint");
      const response = await fetch(endpoint, { redirect: "manual" });
      const text = await response.text();
      const contentType = response.headers.get("Content-Type") || "-";
      const location = response.headers.get("Location") || "-";
      const charset = contentType.includes("charset=") ? contentType.split("charset=")[1] : "-";

      statusEl.textContent = `${response.status} ${response.statusText}`;
      contentTypeEl.textContent = contentType;
      charsetEl.textContent = charset;
      locationEl.textContent = location;
      bodyEl.textContent = text.trim() ? text : "<empty response>";
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const buttons = document.querySelectorAll("button[data-endpoint]");
  const statusEl = document.getElementById("status");
  const locationEl = document.getElementById("location");
  const redirectEl = document.getElementById("redirect");
  const resultEl = document.getElementById("result");
  const bodyEl = document.getElementById("body");

  buttons.forEach(button => {
    button.addEventListener("click", async () => {
      const endpoint = button.getAttribute("data-endpoint");
      const method = button.getAttribute("data-method") || "GET";
      const options = { method, redirect: "manual" };

      if (method === "POST") {
        options.headers = { "Content-Type": "application/json" };
        options.body = JSON.stringify({ username: "student" });
      }

      const response = await fetch(endpoint, options);
      const text = await response.text();
      const location = response.headers.get("Location") || "-";
      const status = `${response.status} ${response.statusText}`;
      const result = evaluateResult(endpoint, response.status, location);

      statusEl.textContent = status;
      locationEl.textContent = location;
      redirectEl.textContent = location !== "-" ? location : "-";
      resultEl.textContent = result;
      bodyEl.textContent = text.trim() ? text : "<empty response>";
    });
  });

  function evaluateResult(endpoint, status, location) {
    const isApi = endpoint.startsWith("/api/");
    const isBrowser = endpoint === "/page" || endpoint === "/login";

    if (isBrowser) {
      return location.startsWith("https://") ? "PASS" : "FAIL";
    }
    if (isApi) {
      return status === 403 && location === "-" ? "PASS" : "FAIL";
    }
    return "UNKNOWN";
  }
});

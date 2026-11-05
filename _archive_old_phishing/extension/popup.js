const API_URL = "http://127.0.0.1:8000/api/v1/check";

document.addEventListener("DOMContentLoaded", async () => {
  const urlDisplay = document.getElementById("current-url");
  const statusDisplay = document.getElementById("status-display");
  const scanBtn = document.getElementById("btn-scan");

  // Get current active tab URL
  const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tabs.length === 0) return;

  const currentTab = tabs[0];
  const url = currentTab.url;

  // Render URL in popup
  urlDisplay.textContent = url;

  // Skip scan if it's an internal chrome page
  if (url.startsWith("chrome-extension://") || url.startsWith("chrome://") || url.startsWith("about:")) {
    statusDisplay.textContent = "Protected Browser Page";
    statusDisplay.className = "status-text status-safe";
    scanBtn.disabled = true;
    return;
  }

  scanBtn.addEventListener("click", async () => {
    statusDisplay.textContent = "Scanning page...";
    statusDisplay.className = "status-text";

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
      });

      if (!response.ok) {
        throw new Error("API server offline");
      }

      const result = await response.json();
      const confidencePercent = (result.confidence * 100).toFixed(1);

      if (result.is_phishing) {
        statusDisplay.innerHTML = `⚠️ Suspicious (${confidencePercent}%)`;
        statusDisplay.className = "status-text status-warning";
      } else {
        statusDisplay.innerHTML = `🛡️ Legitimate (${confidencePercent}%)`;
        statusDisplay.className = "status-text status-safe";
      }
    } catch (error) {
      console.error(error);
      statusDisplay.textContent = "API server offline";
      statusDisplay.className = "status-text status-warning";
    }
  });
});

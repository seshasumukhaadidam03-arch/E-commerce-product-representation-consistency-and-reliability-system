const API_URL = "http://127.0.0.1:8000/api/v1/check";

// Local cache for URL scan results
const scanCache = new Map();
// Temporary set of user-bypassed domains
const bypassedDomains = new Set();

// Simple static whitelist of major domains to optimize latency
const WHITELIST = new Set([
  "google.com",
  "github.com",
  "gmail.com",
  "microsoft.com",
  "facebook.com",
  "youtube.com",
  "wikipedia.org",
  "linkedin.com",
  "twitter.com",
  "amazon.com",
  "netflix.com",
  "stackoverflow.com",
  "localhost",
  "127.0.0.1"
]);

// Helper to extract hostname from URL
function getHostname(urlStr) {
  try {
    const url = new URL(urlStr);
    return url.hostname.replace(/^www\./, "");
  } catch (e) {
    return null;
  }
}

// Listen for tab navigation events before the page is rendered
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  // Only intercept main frame requests (ignore sub-frames like iframes)
  if (details.frameId !== 0) return;

  const url = details.url;
  
  // Skip extension pages, browser settings pages, etc.
  if (url.startsWith("chrome-extension://") || url.startsWith("chrome://") || url.startsWith("about:")) {
    return;
  }

  const hostname = getHostname(url);
  if (!hostname) return;

  // 1. Whitelist check
  if (WHITELIST.has(hostname)) {
    console.log(`[Shield] URL is in whitelist: ${hostname}`);
    return;
  }

  // 2. User bypass check
  if (bypassedDomains.has(hostname)) {
    console.log(`[Shield] Domain was bypassed by user: ${hostname}`);
    return;
  }

  // 3. Cache check
  if (scanCache.has(url)) {
    const cachedResult = scanCache.get(url);
    if (cachedResult.is_phishing) {
      console.log(`[Shield] Cache HIT: Blocking ${url}`);
      redirectToBlockPage(details.tabId, url, cachedResult.confidence);
    }
    return;
  }

  console.log(`[Shield] Scanning URL: ${url}`);
  
  // Asynchronously contact our API backend
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url: url })
    });

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const result = await response.json();
    console.log(`[Shield] Result:`, result);

    // Save result to cache
    scanCache.set(url, {
      is_phishing: result.is_phishing,
      confidence: result.confidence
    });

    // If phishing, redirect the tab immediately
    if (result.is_phishing) {
      redirectToBlockPage(details.tabId, url, result.confidence);
    }
  } catch (error) {
    console.error("[Shield] Error querying API backend:", error);
    // Silent fail-open if the backend is down (to not break user's internet)
  }
});

function redirectToBlockPage(tabId, originalUrl, confidence) {
  const blockPageUrl = chrome.runtime.getURL(
    `blocked.html?url=${encodeURIComponent(originalUrl)}&confidence=${encodeURIComponent((confidence * 100).toFixed(1))}`
  );
  chrome.tabs.update(tabId, { url: blockPageUrl });
}

// Message receiver to handle bypass action from the warning page
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "bypass") {
    const hostname = getHostname(request.url);
    if (hostname) {
      bypassedDomains.add(hostname);
      console.log(`[Shield] Added to bypass list: ${hostname}`);
      // Redirect user back to the original URL
      chrome.tabs.update(sender.tab.id, { url: request.url });
    }
  }
});

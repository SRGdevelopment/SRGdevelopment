const apiBaseUrlInput = document.getElementById("api-base-url");
const refreshButton = document.getElementById("refresh-button");
const healthOutput = document.getElementById("health-output");
const marketsOutput = document.getElementById("markets-output");
const recommendationsOutput = document.getElementById("recommendations-output");
const docsLink = document.getElementById("docs-link");
const openapiLink = document.getElementById("openapi-link");

function normalizeBaseUrl(value) {
  return value.replace(/\/+$/, "");
}

function getSafeBaseUrl(value) {
  try {
    const url = new URL(normalizeBaseUrl(value || "http://localhost:8000"));
    if (url.protocol !== "http:" && url.protocol !== "https:") {
      throw new Error("Unsupported protocol");
    }
    return url.origin;
  } catch {
    return "http://localhost:8000";
  }
}

function renderList(container, items, formatter) {
  container.replaceChildren();
  for (const item of items) {
    const entry = document.createElement("li");
    entry.textContent = formatter(item);
    container.appendChild(entry);
  }
}

function renderStatus(container, message) {
  const entry = document.createElement("li");
  entry.textContent = message;
  container.replaceChildren(entry);
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function refreshPreview() {
  const baseUrl = getSafeBaseUrl(apiBaseUrlInput.value);
  apiBaseUrlInput.value = baseUrl;
  docsLink.href = `${baseUrl}/docs`;
  openapiLink.href = `${baseUrl}/openapi.json`;

  healthOutput.textContent = "Loading…";
  renderStatus(marketsOutput, "Loading…");
  renderStatus(recommendationsOutput, "Loading…");

  try {
    const [health, markets, recommendations] = await Promise.all([
      fetchJson(`${baseUrl}/health`),
      fetchJson(`${baseUrl}/markets/live`),
      fetchJson(`${baseUrl}/recommendations/top`),
    ]);

    healthOutput.textContent = JSON.stringify(health, null, 2);
    renderList(
      marketsOutput,
      markets,
      (market) => `${market.event} — ${market.side_a_price_cents}/${market.side_b_price_cents}¢`,
    );
    renderList(
      recommendationsOutput,
      recommendations.recommendations,
      (recommendation) =>
        `${recommendation.market_id} ${recommendation.side} — edge ${recommendation.edge.toFixed(2)}`,
    );
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    healthOutput.textContent = `Unable to load preview data: ${message}`;
    renderStatus(marketsOutput, "Unavailable");
    renderStatus(recommendationsOutput, "Unavailable");
  }
}

refreshButton.addEventListener("click", refreshPreview);
refreshPreview();

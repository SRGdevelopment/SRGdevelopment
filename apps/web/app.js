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

function renderList(container, items, formatter) {
  container.innerHTML = "";
  for (const item of items) {
    const entry = document.createElement("li");
    entry.textContent = formatter(item);
    container.appendChild(entry);
  }
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json();
}

async function refreshPreview() {
  const baseUrl = normalizeBaseUrl(apiBaseUrlInput.value || "http://localhost:8000");
  docsLink.href = `${baseUrl}/docs`;
  openapiLink.href = `${baseUrl}/openapi.json`;

  healthOutput.textContent = "Loading…";
  marketsOutput.innerHTML = "<li>Loading…</li>";
  recommendationsOutput.innerHTML = "<li>Loading…</li>";

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
    marketsOutput.innerHTML = "<li>Unavailable</li>";
    recommendationsOutput.innerHTML = "<li>Unavailable</li>";
  }
}

refreshButton.addEventListener("click", refreshPreview);
refreshPreview();

# Blue Coat Traffic Logging — User Agent Analysis

**Purpose**  
This dashboard helps security and network teams understand *what* is talking to the internet through Blue Coat / Symantec Proxy (ProxySG/ASG) and *how* it behaves, with emphasis on user-agent intelligence, destinations, categories, allow/deny posture, and latency. It’s meant to surface risky or unexpected user agents, identify noisy/business-critical destinations, and spot performance outliers.

---

## What’s Included (Panels)

- **Top Destinations**  
  Ranks busiest external hosts (`cs_host`) to reveal high-volume SaaS, update services, and CDNs.

- **Traffic by Filter Category**  
  Summarizes proxy classifications (`filter_category`) to validate acceptable-use posture and catch odd categories gaining volume.

- **Observed vs Blocked Traffic**  
  Breaks down `sc_filter_result` (e.g., allowed/blocked) to confirm policy effectiveness and detect drift.

- **Time Taken Distribution (by Host)**  
  Per-destination latency percentiles (`min/q1/median/q3/max` from `time_taken`) to flag slow upstreams or degraded paths.

- **Chrome Versions**  
  Extracts `Chrome/<version>` from `cs_user_agent` to highlight outdated browsers or uneven patching.

- **New Non-Browser User Agents (24h vs prior day)**  
  Finds *non-Mozilla* user agents that are new or up-trending using `compare with timeshift 1d`—useful for detecting new tooling or suspicious beacons.

- **New Browser User Agents (24h vs prior day)**  
  Same concept as above, scoped to browser-like agents (strings containing “Mozilla”) to catch atypical or legacy UA strings.

---

## Data Requirements

- **Log Source:** Blue Coat / Symantec Proxy logs forwarded to Sumo Logic.
- **Source Category:** Queries assume `_sourceCategory = "syslog/bluecoat"`. Change to match your environment.
- **Parsed Fields:**  Use the FER in the regex folder beforehand
  `s_action`, `sc_status`, `cs_method`, `time_taken`, `sc_bytes`, `cs_bytes`,  
  `cs_uri_scheme`, `cs_host`, `cs_uri_path`, `cs_uri_query`, `cs_uri_extension`,  
  `cs_auth_group`, `rs(Content-Type)`, `cs(User-Agent)`, `cs(Referer)`,  
  `sc-filter-result` → `sc_filter_result`, `filter_category`, `cs_uri`.

> **Note:** The regex extracts pipe-delimited key/values. If your format is customized, adjust the regex patterns accordingly.

---

## Time Range & Refresh

- **Default Range:** Last 24 hours  
- **Refresh:** Manual by default (configure auto-refresh in the UI if desired)

---

## How It Works (At a Glance)

- **Parsing:** `parse regex` extracts Blue Coat fields from pipe-delimited messages.  
- **Aggregation:** `count by` for leaders/categories; `pct()` over `time_taken` for latency percentiles.  
- **User-Agent Intelligence:** Regex captures browser versions; “new UA” tables use `compare with timeshift 1d` to surface day-over-day changes.

---

## Typical Investigations

- **Policy drift:** Unexpected rise in *allowed* traffic for categories that should be restricted.  
- **Emerging tools/agents:** New, non-browser UAs appearing across endpoints.  
- **Patch hygiene:** Outdated Chrome versions lingering in parts of the org.  
- **Performance hotspots:** Elevated median/max `time_taken_ms` for specific SaaS/CDN hosts.

---

## Setup

1. **Import** the dashboard JSON in Sumo Logic (Dashboards → **Import**).  
2. **Update filters:** Replace `_sourceCategory="syslog/bluecoat"` with your value(s).  
3. **(Optional)** Add a dashboard-level variable for source category if you ingest from multiple Blue Coat feeders.  
4. **Save** and set your preferred default time range / auto-refresh.

---

## Privacy & Security

- **No screenshots** are included to avoid exposing customer-specific domains or user-agents.  
- Before sharing externally, scrub any example outputs or replace with mock data.

---

## Limitations / Notes

- Customized log formats may require tweaking the regex.  
- UA versioning currently focuses on Chrome; extend patterns for Edge/Firefox/Safari as needed.  
- Timeshift comparisons require at least 48 hours of data for meaningful deltas.


# NetPulse: Large-Scale Internet Outage Detection, Propagation Analysis & Early Warning System

[![Python 3.13](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1-black.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-20%20Passed-brightgreen.svg)]()
[![Design](https://img.shields.io/badge/UI-Futuristic%20SaaS%20Dark-indigo.svg)]()

> A Big Data network intelligence platform designed to ingest high-volume network telemetry, detect active outages, analyze spatial-temporal propagation patterns across Indian metropolitan regions, predict outage risk in real-time, and benchmark ISP recovery dynamics.

---

## 1. Problem Statement

Modern internet reliability is critical for digital economies. However, telecom operators and digital platforms frequently struggle with:
1. **Delayed Outage Identification**: Reactive alerting based on end-user complaints rather than proactive degradation signals.
2. **Invisible Cascading Propagation**: Outages in major upstream transit hubs (e.g., Chennai or Mumbai) silently propagate to secondary and tertiary cities before operators notice the correlation.
3. **Lack of Early Warning**: Missing leading indicators (rate-of-change in latency, subtle packet loss spikes, DNS resolution latency) that precede catastrophic blackouts.
4. **Opaque Recovery Trajectories**: No standardized metric to compare Mean Time to Recover (MTTR) across national ISPs and regional access rings.

**NetPulse** solves this by unifying Big Data batch processing (HDFS, Pig, Hive) with Machine Learning (Isolation Forest, Rate-of-Change Risk Scoring) and an interactive, real-time command dashboard.

---

## 2. Architecture Overview

```
[ Synthetic Telemetry Engine (100k+ records) ]
                  │
                  ▼
         [ Big Data Pipeline ]
         ├── HDFS Storage (/netpulse/raw, /processed, /analytics, /outages, /regions, /isps)
         ├── Apache Pig ETL (Validation, Cleaning, Outage & Propagation Prep)
         └── Apache Hive Analytics (netpulse DB, Aggregations, Reliability & Recovery Views)
                  │
                  ▼
    [ Python ML & Analytics Engine ]
    ├── Isolation Forest Anomaly Detection
    ├── Network Health Score Engine (0-100)
    ├── Outage Detection & Severity Engine (0-100)
    ├── Spatial-Temporal Propagation Engine (Haversine velocity tracking)
    ├── Early Warning Risk Predictor (0-100)
    ├── Historical Outage Signature Matcher
    └── Recovery Time Analyzer
                  │
                  ▼
         [ Database Layer ]
         ├── MongoDB / Fallback Embedded Document Store
         └── Collections: network_status, outage_events, alerts, predictions,
                          propagation_events, recovery_events, outage_signatures
                  │
                  ▼
       [ Flask REST & Socket.IO APIs ]
       ├── REST Endpoints: /api/network/*, /api/outages/*, /api/regions,
       │                   /api/isps, /api/propagation, /api/predictions,
       │                   /api/recovery, /api/alerts, /api/analysis/run
       └── WebSocket: /network-live (SIMULATED LIVE TELEMETRY)
                  │
                  ▼
   [ Futuristic SaaS Dark Navy Dashboard ]
   ├── HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, Bootstrap Icons, Chart.js, Leaflet.js, Jinja2
   └── Dynamic India Map, KPI Cards, Forensic Time Series, Propagation Path Visualizer
```

---

## 3. Core Features

1. **Network Health Score (0-100)**: Project-defined linear penalty score combining latency, packet loss, download degradation, upload degradation, DNS failures, and connection status.
2. **Outage Detection Engine**: Rule-based detection using critical packet loss (&ge; 25%), latency (&ge; 280 ms), and connection drops.
3. **ML Anomaly Detection**: Unsupervised `IsolationForest` detecting multi-dimensional feature deviations.
4. **Outage Severity Index (0-100)**: Multi-factor scoring accounting for user scale, duration, geographic breadth, and throughput collapse.
5. **Outage Propagation Analysis**: Tracks cascading failures (e.g. *Chennai &rarr; Coimbatore &rarr; Madurai &rarr; Salem*), computing propagation velocity (km/h) and stage timelines. Labeled as *detected propagation patterns*.
6. **Root-Cause Pattern Analysis**: Classifies ISP instability, regional congestion, DNS reachability, and connectivity drops.
7. **Early Warning Risk Engine**: 0-100 risk score with leading signal derivatives and a 2-hour forecast horizon.
8. **Recurring Outage Signatures**: Matches incidents against archetypal fingerprints (diurnal peak, midnight maintenance, monsoon fiber attenuation).
9. **Recovery Intelligence & MTTR**: Analyzes recovery times, throughput restoration slopes (Mbps/min), and fast/slow recovery percentages.
10. **Dynamic India Map**: Leaflet.js map tracking 10 Indian cities (Chennai, Coimbatore, Bengaluru, Hyderabad, Mumbai, Delhi, Pune, Kochi, Madurai, Salem) with glowing status markers.
11. **Live Network Telemetry**: WebSocket-based telemetry stream labeled `SIMULATED LIVE TELEMETRY`.
12. **Operational Alert Center**: Triage and acknowledge alerts across 6 core categories.

---

## 4. Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, Bootstrap Icons, Chart.js 4, Leaflet.js 1.9, Jinja2.
- **Backend**: Python 3.13, Flask 3.1, Flask-SocketIO 5.6, simple-websocket.
- **Database**: MongoDB 7.0 / Transparent Embedded JSON Collection Store.
- **Big Data Pipeline**: Apache Hadoop 3.2 (HDFS), Apache Pig 0.17, Apache Hive 2.3.
- **Analytics & ML**: Scikit-learn (Isolation Forest), Pandas, NumPy.
- **Testing**: pytest 9.1.

---

## 5. Quick Start (Demo Mode)

NetPulse runs immediately out-of-the-box in **Demo Mode** without requiring external Hadoop or MongoDB installations.

```bash
# 1. Clone or navigate to the directory
cd NetPulse

# 2. Install dependencies
pip install -r requirements.txt

# 3. Generate 100,000 synthetic telemetry records
python data/generator.py --records 100000 --seed 42

# 4. Run automated tests
pytest -v tests/

# 5. Launch NetPulse web server
python app.py
```

Access the dashboard at: **`http://localhost:5000`**

---

## 6. Big Data Mode & Production Deployment

To run with full Hadoop HDFS, Hive, and MongoDB:

```bash
# Start cluster services via Docker Compose
docker-compose up -d

# Initialize HDFS directories
bash hdfs/create_dirs.sh

# Upload raw telemetry to HDFS
bash hdfs/upload_data.sh data/raw/network_telemetry.csv

# Execute Pig ETL transformations
pig -x mapreduce pig/clean_validate.pig
pig -x mapreduce pig/transform_metrics.pig
pig -x mapreduce pig/outage_prep.pig

# Execute Hive Data Warehouse creation
hive -f hive/01_create_database.hql
hive -f hive/02_create_tables.hql
hive -f hive/03_analytical_queries.hql

# Launch application in Big Data Mode
python app.py
```

---

## 7. REST & WebSocket API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/api/network/summary` | `GET` | Core KPI cards, health index, active outage counts |
| `/api/network/status` | `GET` | Geographic node status for Leaflet map & 24h trends |
| `/api/outages` | `GET` | List outages (filter by `city`, `isp`, `active_only`) |
| `/api/outages/<incident_id>` | `GET` | Detailed incident forensics (before/during/after) |
| `/api/regions` | `GET` | Regional network health and impact breakdown |
| `/api/isps` | `GET` | ISP performance, latency, and reliability benchmarks |
| `/api/propagation` | `GET` | Detected propagation chains, velocity, and stages |
| `/api/predictions` | `GET` | Early warning outage risk scores and leading signals |
| `/api/recovery` | `GET` | MTTR metrics, recovery velocity, and slopes |
| `/api/alerts` | `GET` | Operational notifications log |
| `/api/alerts/<id>/ack` | `POST` | Acknowledge an alert |
| `/api/analysis/run` | `POST` | Trigger full analytics & ML batch processing |
| `/network-live` | `WS` | WebSocket streaming simulated live telemetry |

---

## 8. Test Suite Summary

Run all 20 unit and integration tests:
```bash
pytest -v tests/
```

- `test_generator.py`: Verifies 100k data schema, range bounds, and seed consistency.
- `test_health_score.py`: Verifies linear penalties, weights, and vectorized computations.
- `test_outage_detector.py`: Tests outage thresholds and incident clustering.
- `test_severity.py`: Tests multi-factor 0-100 severity bounds.
- `test_propagation.py`: Tests Haversine distance and cascading chain detection.
- `test_recovery.py`: Tests MTTR and recovery velocity classification.
- `test_early_warning.py`: Tests pre-outage rate of change derivatives.
- `test_database.py`: Tests CRUD operations across MongoDB and fallback store.
- `test_api.py`: Tests all 8 core REST API endpoints.

---

## 9. Limitations & Future Work

- **Limitations**:
  - In Demo Mode, calculations are executed using optimized in-memory Pandas routines rather than distributed MapReduce tasks.
  - Telemetry is generated based on realistic statistical models rather than live ISP SNMP feeds.
- **Future Improvements**:
  - Integration with live RIPE Atlas or ThousandEyes probe feeds.
  - Graph Neural Network (GNN) modeling for physical optical fiber topology propagation.
  - Automated BGP route leak verification integration via RouteViews.

import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    # Set 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color Palette (Dark Navy & Futuristic SaaS Accents)
    COLOR_BG = RGBColor(10, 13, 24)        # #0a0d18 deep navy
    COLOR_CARD = RGBColor(18, 25, 46)      # #12192e glass navy
    COLOR_TEXT_MAIN = RGBColor(241, 245, 249) # #f1f5f9
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184) # #94a3b8
    COLOR_CYAN = RGBColor(6, 182, 212)     # #06b6d4
    COLOR_PURPLE = RGBColor(168, 85, 247)  # #a855f7
    COLOR_INDIGO = RGBColor(99, 102, 241)  # #6366f1
    COLOR_EMERALD = RGBColor(16, 185, 129) # #10b981
    COLOR_ROSE = RGBColor(244, 63, 94)     # #f43f5e
    COLOR_AMBER = RGBColor(245, 158, 11)   # #f59e0b

    slides_data = [
        # Slide 1: Title
        {
            "title": "NetPulse",
            "subtitle": "Large-Scale Internet Outage Detection, Propagation Analysis & Early Warning System",
            "tag": "BIG DATA NETWORK INTELLIGENCE PLATFORM",
            "bullets": [
                "A Big Data & Machine Learning Framework for Critical Telecommunication Infrastructure",
                "Scalable Telemetry Ingestion (100k+ Records across Indian Metropolitan Transit Rings)",
                "Spatial-Temporal Cascading Outage Detection & Pre-Failure Early Warning Risk Modeling"
            ],
            "notes": "Good morning everyone. Today I am presenting NetPulse, an end-to-end Big Data network intelligence system designed to tackle one of the most critical vulnerabilities in telecommunications: detecting internet disruptions, tracking how outages cascade across geographic regions, and warning operators before blackouts occur."
        },
        # Slide 2: Problem Statement
        {
            "title": "Problem Statement: The Fragility of Modern Internet",
            "subtitle": "Why Traditional Network Monitoring Tools Fail at Scale",
            "tag": "CHALLENGES IN CURRENT INFRASTRUCTURE",
            "bullets": [
                "Reactive Instead of Proactive: Operators alert only after full link collapse or citizen complaints.",
                "Invisible Cascading Propagation: Transit gateway failures silently ripple across secondary cities.",
                "Telemetry Volume Overload: Millions of probes create data streams that crash conventional relational SQL databases.",
                "Opaque Recovery Dynamics: Telecom regulators lack standardized Mean Time to Recover (MTTR) benchmarks."
            ],
            "notes": "Let us examine why modern networks fail. Internet outages are rarely isolated, instantaneous events. In reality, they begin with subtle metric degradation at core peering transit gateways like Chennai or Mumbai, which then propagate along regional fiber routes. Traditional tools are reactive and siloed, unable to digest the sheer volume of continuous high-frequency telemetry."
        },
        # Slide 3: Proposed Solution
        {
            "title": "Proposed Solution: The NetPulse Architecture",
            "subtitle": "Unified Big Data Batch Processing + Sub-Millisecond Operational Intelligence",
            "tag": "A MULTI-TIER DATA PARADIGM",
            "bullets": [
                "Automated Network Health Index: Standardized 0-100 linear penalty score across 6 key metrics.",
                "Spatial-Temporal Propagation Engine: Haversine-based velocity tracking of cascading disruption vectors.",
                "Unsupervised Machine Learning: Isolation Forest for non-linear multi-dimensional anomaly detection.",
                "Early Warning Predictive Risk: 2-hour forecast horizon derived from degradation rates-of-change."
            ],
            "notes": "NetPulse bridges this gap with a multi-tier data architecture. It ingests massive probe telemetry into Hadoop HDFS, cleans and transforms it using Apache Pig, runs large-scale OLAP analytics in Apache Hive, applies Isolation Forest ML in Python, and serves real-time curated intelligence through MongoDB to a futuristic SaaS command dashboard."
        },
        # Slide 4: End-to-End System Architecture
        {
            "title": "End-to-End Pipeline: From Raw Probes to Dashboard",
            "subtitle": "Decoupled Ingestion, Processing, Analytics, and Real-Time Serving",
            "tag": "DATA FLOW & PIPELINE LIFECYCLE",
            "bullets": [
                "Raw Telemetry (100k+ records) -> Hadoop HDFS Storage (/netpulse/raw)",
                "Apache Pig ETL -> Multi-step cleaning, coordinate boundary checks, and threshold clamping",
                "Apache Hive Warehouse -> Schema-on-read ORC & Parquet tables for analytical OLAP aggregations",
                "Machine Learning Core -> Isolation Forest anomaly scores & Outage Severity indices (0-100)",
                "MongoDB Serving Layer -> Sub-5ms queries feeding Flask REST endpoints & Socket.IO live stream"
            ],
            "notes": "Here is the architectural lifecycle. Notice the decoupling: raw high-volume data stays in the distributed HDFS layer and is cleaned via Pig. Hive structures analytical aggregations, while Python executes ML models. Finally, only curated, actionable insights are loaded into MongoDB for sub-5-millisecond retrieval by our Flask web application."
        },
        # Slide 5: The Big Data Core
        {
            "title": "The Big Data Core: HDFS, Pig & Hive",
            "subtitle": "Why Using All Three Technologies is Essential",
            "tag": "DISTRIBUTED DATA ENGINE",
            "bullets": [
                "Hadoop HDFS: Cost-effective, distributed, fault-tolerant raw storage for billions of telemetry pings.",
                "Apache Pig (Procedural ETL): High-throughput sanitation, clamping packet loss [0-100]%, and discarding nulls.",
                "Apache Hive (Declarative OLAP): SQL-on-Hadoop enabling historical provider reliability and MTTR queries.",
                "Columnar Optimization: Storing warehouse tables in ORC and Parquet formats reduces disk I/O by up to 80%."
            ],
            "notes": "A common evaluation question is: why do we need HDFS, Pig, and Hive together? HDFS is our write-heavy raw repository. Pig gives us procedural cleaning power to filter out negative latencies and invalid coordinates before warehousing. Hive then provides declarative SQL so network engineers can run analytical aggregations across months of historical data without writing low-level code."
        },
        # Slide 6: Operational Serving & Database Strategy
        {
            "title": "Operational Serving: Why MongoDB & Dual-Mode Design?",
            "subtitle": "Bridging Batch Analytics with Low-Latency Web Delivery",
            "tag": "HIGH-CONCURRENCY SERVING LAYER",
            "bullets": [
                "The Hive Query Latency Problem: Hive takes 15-60s to compile distributed jobs - unacceptable for web UI.",
                "MongoDB Sub-5ms Lookups: Stores curated incident models, city health, alerts, and early warnings.",
                "No Raw Data in MongoDB: Raw bulk telemetry remains in HDFS/Hive to prevent database bloat.",
                "Zero-Dependency Demo Mode: Embedded in-memory/JSON store activates automatically when cluster is offline."
            ],
            "notes": "While Hive is brilliant for batch aggregations, it is too slow for web users who expect instant page loads. MongoDB acts as our high-speed operational cache, serving pre-computed health indices and alerts in under 5 milliseconds. Moreover, NetPulse features an automatic fallback to an embedded local document store if MongoDB is offline, guaranteeing 100% operational availability."
        },
        # Slide 7: Core Algorithm 1 - Health & Outages
        {
            "title": "Core Algorithm: Health Score & Outage Detection",
            "subtitle": "Objective Metric Formulations & Multi-Factor Severity Scoring",
            "tag": "MATHEMATICAL FORMULATIONS",
            "bullets": [
                "Network Health Score (0-100) = 100 - [0.25*Lat_Pen + 0.30*Loss_Pen + 0.15*Down + 0.10*Up + 0.10*DNS + 0.10*Conn]",
                "Contiguous Incident Clustering: Groups sequential threshold violations (gap < 20m) into persistent incidents.",
                "Outage Severity Index (0-100): Combines throughput drop (25%), packet loss (25%), log-scaled users (20%), duration (15%), and geographic spread (10%).",
                "Root-Cause Pattern Classifier: Identifies ISP instability, regional congestion, and DNS reachability failures."
            ],
            "notes": "Here is our core mathematical logic. Instead of subjective statuses, NetPulse computes a normalized 0 to 100 Health Score using a weighted linear penalty model. If an outage occurs, our severity algorithm evaluates throughput collapse, packet loss, and human impact via a logarithmic scale so that massive 100,000-user outages are appropriately escalated."
        },
        # Slide 8: Core Algorithm 2 - Machine Learning
        {
            "title": "Core Algorithm: ML Anomaly Detection",
            "subtitle": "Unsupervised Multi-Dimensional Isolation Forest Modeling",
            "tag": "SCIKIT-LEARN MACHINE LEARNING",
            "bullets": [
                "Unsupervised Isolation Forest: Trained on 6-dimensional telemetry tensors without requiring human labels.",
                "Mathematical Premise: Anomalous points are few and distinct, requiring significantly fewer tree splits to isolate.",
                "Anomaly Score Formulation: s(x, n) = 2^(-E(h(x)) / c(n)), mapped to a 0-100 anomaly intensity index.",
                "Complementary Architecture: Catches subtle multi-variable drifts that rigid threshold rules overlook."
            ],
            "notes": "Rule-based thresholds are great for obvious blackouts, but what about subtle infrastructure degradation? We utilize Scikit-learn's Isolation Forest. Because anomalous telemetry points reside in low-density feature space, recursive random tree partitioning isolates them in far fewer splits than normal clusters, allowing us to detect emerging failures in an unsupervised manner."
        },
        # Slide 9: Core Algorithm 3 - Propagation Engine
        {
            "title": "Core Algorithm: Spatial-Temporal Outage Propagation",
            "subtitle": "Tracking Cascading Failures Across Transit Rings",
            "tag": "CORRELATION & VELOCITY ENGINE",
            "bullets": [
                "Cascading Vector Tracking: Detects sequential failure onset: Chennai -> Coimbatore -> Madurai -> Salem.",
                "Haversine Surface Distance: Computes true great-circle kilometers between metropolitan coordinates.",
                "Propagation Velocity (km/h): Total geographical distance divided by elapsed onset time.",
                "Strict Disclaimer: Output designated as 'detected propagation patterns' (statistical correlation), not confirmed physical root causes."
            ],
            "notes": "This slide showcases one of NetPulse's most novel contributions: Outage Propagation Analysis. When an incident occurs in Chennai at T=0, followed by Coimbatore 35 minutes later, Madurai 40 minutes after, and Salem 45 minutes later, NetPulse clusters them into a single propagation chain, calculates its velocity in km/h, and plots the vector path on our interactive map."
        },
        # Slide 10: Core Algorithm 4 - Early Warning System
        {
            "title": "Core Algorithm: Early Warning & Risk Forecast",
            "subtitle": "Predictive First-Order Derivative Analytics (2-Hour Horizon)",
            "tag": "PRE-OUTAGE PREDICTIVE ENGINE",
            "bullets": [
                "Rate-of-Change Derivatives: Measures Delta Latency, Delta Packet Loss, and Throughput Decay.",
                "Outage Risk Score (0-100) = 0.30*Lat_Risk + 0.30*Loss_Risk + 0.25*Speed_Risk + 0.15*DNS_Risk.",
                "Categorical Risk Tiers: Low (<35), Moderate (35-59), Elevated (60-79), and Critical (>=80).",
                "Historical Signature Matching: Vector similarity identifies recurring diurnal evening congestion archetypes."
            ],
            "notes": "How do we prevent blackouts? By measuring rates-of-change rather than absolute levels. If a city's latency derivative jumps by 140% and DNS resolution timeouts begin to rise, our Early Warning Engine calculates an Outage Risk Score and issues alerts up to 2 hours before complete catastrophic network collapse."
        },
        # Slide 11: Recovery & Verification
        {
            "title": "Recovery Intelligence & Empirical Verification",
            "subtitle": "Standardized MTTR Analytics & Automated Test Suite Results",
            "tag": "BENCHMARKING & VALIDATION",
            "bullets": [
                "Mean Time to Recover (MTTR): Quantifies restoration duration and bandwidth restoration slopes (Mbps/min).",
                "Recovery Classifications: Fast (<30m - auto failover), Moderate (30-90m), and Slow (>90m - physical repair).",
                "Automated Testing (pytest): 20/20 Test Suites Passed with 100% success rate across all algorithms and APIs.",
                "Live API Verification: 20/20 REST endpoints and WebSocket channels verified operational at http://localhost:5000."
            ],
            "notes": "Finally, NetPulse measures post-outage resilience. We calculate the Mean Time to Recover across ISPs and determine the throughput restoration slope. Furthermore, our entire platform is backed by rigorous engineering: 20 out of 20 unit and integration tests pass cleanly in pytest, and all 20 web and API endpoints are verified live."
        },
        # Slide 12: Conclusion & Q&A
        {
            "title": "Conclusion & Future Horizons",
            "subtitle": "Transforming Reactive Telecommunications into Predictive Intelligence",
            "tag": "SUMMARY & FUTURE ENHANCEMENTS",
            "bullets": [
                "Proven Viability: Scalable Big Data pipeline handling 100k+ records with sub-second dashboard updates.",
                "Key Innovations: Unified Health Score, cascading propagation detection, and 2-hour early warning models.",
                "Future Enhancements: Integration with real-world RIPE Atlas and BGP route leak feeds via RouteViews.",
                "Open for Questions: Thank you for your time!"
            ],
            "notes": "In conclusion, NetPulse proves that combining Big Data technologies with modern machine learning can transform telecommunications from a reactive firefighting posture into proactive, predictive network intelligence. Thank you, and I now welcome any questions from the panel."
        }
    ]

    blank_slide_layout = prs.slide_layouts[6]

    for idx, data in enumerate(slides_data):
        slide = prs.slides.add_slide(blank_slide_layout)

        # 1. Background Rectangle
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = COLOR_BG
        bg_shape.line.fill.background()

        # 2. Top Banner Pill / Category Tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.4))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = f"{data['tag']}  |  SLIDE {idx + 1} OF 12"
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_CYAN

        # 3. Slide Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = data["title"]
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_MAIN

        # 4. Slide Subtitle
        sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(0.4))
        tf_sub = sub_box.text_frame
        tf_sub.word_wrap = True
        p_sub = tf_sub.paragraphs[0]
        p_sub.text = data["subtitle"]
        p_sub.font.size = Pt(14)
        p_sub.font.color.rgb = COLOR_PURPLE

        # 5. Main Content Card
        card_shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.15), Inches(11.733), Inches(4.75)
        )
        card_shape.fill.solid()
        card_shape.fill.fore_color.rgb = COLOR_CARD
        card_shape.line.color.rgb = COLOR_INDIGO
        card_shape.line.width = Pt(1.5)

        # 6. Bullets inside Main Card
        content_box = slide.shapes.add_textbox(Inches(1.1), Inches(2.35), Inches(11.133), Inches(4.3))
        tf_content = content_box.text_frame
        tf_content.word_wrap = True

        for b_idx, bullet in enumerate(data["bullets"]):
            p = tf_content.add_paragraph() if b_idx > 0 else tf_content.paragraphs[0]
            p.text = f"•  {bullet}"
            p.font.size = Pt(16)
            p.font.color.rgb = COLOR_TEXT_MAIN
            p.space_after = Pt(18)
            p.space_before = Pt(4)

        # 7. Add Speaker Notes to Slide
        notes_slide = slide.notes_slide
        tf_notes = notes_slide.notes_text_frame
        tf_notes.text = f"SPEAKER TALKING POINTS:\n{data['notes']}"

    output_path = "NetPulse_Seminar_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation successfully generated at: {output_path}")

if __name__ == '__main__':
    create_presentation()

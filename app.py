import os
import sys
import logging
from pathlib import Path
from flask import Flask, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS

from config import Config
from database.db import db
from routes.api_routes import api_bp
from routes.view_routes import view_bp
from routes.socket_events import register_socket_events
from services.alert_service import AlertService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger('NetPulse')

def create_app():
    """Application factory for NetPulse."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register Blueprints
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)

    # Global 404 handler
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({'status': 'error', 'message': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

    return app

def initialize_database_data():
    """Seeds initial dataset and runs first-pass analytics if database is empty."""
    status_col = db.get_collection('network_status')
    if status_col.count_documents({}) == 0:
        logger.info("Initializing NetPulse database with baseline network telemetry...")
        from data.generator import generate_telemetry
        from analytics.outage_detector import OutageDetector
        from analytics.health_score import HealthScoreEngine
        from analytics.severity_calculator import SeverityCalculator
        from analytics.propagation_engine import PropagationEngine
        from analytics.early_warning import EarlyWarningEngine
        from analytics.recovery_analyzer import RecoveryAnalyzer
        import pandas as pd

        csv_path = Config.RAW_DATA_DIR / 'network_telemetry.csv'
        if not csv_path.exists():
            logger.info("Generating initial telemetry dataset (100,000 records)...")
            df = generate_telemetry(num_records=100000)
        else:
            df = pd.read_csv(csv_path)

        # Detect incidents
        incidents = OutageDetector.detect_incidents_from_df(df)
        outage_col = db.get_collection('outage_events')
        for inc in incidents:
            dur = inc['metrics_during']
            sev = SeverityCalculator.calculate(
                avg_download_mbps=dur['download_mbps'],
                avg_packet_loss_pct=dur['packet_loss_pct'],
                affected_users=inc['affected_users'],
                duration_mins=inc['duration_mins']
            )
            inc['severity_score'] = sev
            outage_col.insert_one(inc)

        # Populate current network status for 10 cities * 6 ISPs
        latest_slice = df.tail(len(Config.TARGET_CITIES) * len(Config.TARGET_ISPS))
        for _, row in latest_slice.iterrows():
            h_score = HealthScoreEngine.calculate_score(
                latency_ms=row['latency_ms'],
                packet_loss_pct=row['packet_loss_percent'],
                download_mbps=row['download_mbps'],
                upload_mbps=row['upload_mbps'],
                dns_failure=row['dns_failure'],
                connection_status=row['connection_status']
            )
            status_col.insert_one({
                'city': row['city'],
                'region': row['region'],
                'isp': row['isp'],
                'network_type': row['network_type'],
                'latitude': float(row['latitude']),
                'longitude': float(row['longitude']),
                'latency_ms': float(row['latency_ms']),
                'download_mbps': float(row['download_mbps']),
                'upload_mbps': float(row['upload_mbps']),
                'packet_loss_percent': float(row['packet_loss_percent']),
                'dns_failure': int(row['dns_failure']),
                'connection_status': row['connection_status'],
                'active_users': int(row['active_users']),
                'health_score': h_score,
                'status_label': HealthScoreEngine.get_status_label(h_score)
            })

        # Propagation
        prop_patterns = PropagationEngine.detect_patterns(incidents)
        prop_col = db.get_collection('propagation_events')
        for p in prop_patterns:
            prop_col.insert_one(p)

        # Predictions
        preds = EarlyWarningEngine.generate_city_predictions(df)
        pred_col = db.get_collection('predictions')
        for pr in preds:
            pred_col.insert_one(pr)

        # Recovery
        rec_data = RecoveryAnalyzer.analyze_recoveries(incidents)
        rec_col = db.get_collection('recovery_events')
        for ev in rec_data['events']:
            rec_col.insert_one(ev)

        # Alerts
        AlertService.seed_initial_alerts()
        logger.info(f"Database initialization complete! Loaded {len(incidents)} incidents, {len(prop_patterns)} propagation patterns.")

app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")
register_socket_events(socketio)

if __name__ == '__main__':
    initialize_database_data()
    env_info = Config.check_system_environment()
    print("=" * 60)
    print("NETPULSE - Internet Outage & Early Warning Platform")
    print(f"Mode: {env_info['pipeline_mode']}")
    print(f"Server running at: http://{Config.HOST}:{Config.PORT}")
    print("=" * 60)
    socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, allow_unsafe_werkzeug=True)

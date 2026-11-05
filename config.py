import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
ENV_PATH = BASE_DIR / '.env'
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)
else:
    load_dotenv(BASE_DIR / '.env.example')

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'netpulse-super-secret-key-2026')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() in ('true', '1', 't')
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

    # Storage Paths
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    EMBEDDED_DB_DIR = BASE_DIR / 'database' / 'storage'

    # MongoDB Settings
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
    MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'netpulse')
    FORCE_DEMO_MODE = os.getenv('FORCE_DEMO_MODE', 'False').lower() in ('true', '1', 't')

    # Big Data Tool Paths
    HADOOP_HOME = os.getenv('HADOOP_HOME', 'C:\\hadoop')
    HDFS_NAMENODE = os.getenv('HDFS_NAMENODE', 'hdfs://localhost:9000')

    # Indian Metropolitan Monitored Nodes
    TARGET_CITIES = {
        'Chennai': {'lat': 13.0827, 'lng': 80.2707, 'region': 'South'},
        'Coimbatore': {'lat': 11.0168, 'lng': 76.9558, 'region': 'South'},
        'Bengaluru': {'lat': 12.9716, 'lng': 77.5946, 'region': 'South'},
        'Hyderabad': {'lat': 17.3850, 'lng': 78.4867, 'region': 'South'},
        'Mumbai': {'lat': 19.0760, 'lng': 72.8777, 'region': 'West'},
        'Delhi': {'lat': 28.6139, 'lng': 77.2090, 'region': 'North'},
        'Pune': {'lat': 18.5204, 'lng': 73.8567, 'region': 'West'},
        'Kochi': {'lat': 9.9312, 'lng': 76.2673, 'region': 'South'},
        'Madurai': {'lat': 9.9252, 'lng': 78.1198, 'region': 'South'},
        'Salem': {'lat': 11.6643, 'lng': 78.1460, 'region': 'South'}
    }

    TARGET_ISPS = ['Jio', 'Airtel', 'Vodafone Idea (Vi)', 'BSNL', 'ACT Fibernet', 'Tata Communications']
    NETWORK_TYPES = ['5G', '4G LTE', 'Fiber Broadband', 'Enterprise Leased Line']

    # Health Score Weights
    WEIGHTS = {
        'latency': 0.25,
        'packet_loss': 0.30,
        'download_degradation': 0.15,
        'upload_degradation': 0.10,
        'dns_failure': 0.10,
        'connection_status': 0.10
    }

    # Outage Thresholds
    OUTAGE_THRESHOLDS = {
        'packet_loss_critical': 25.0,     # >25% packet loss
        'latency_critical_ms': 280.0,     # >280ms latency
        'download_drop_percent': 70.0,    # >70% drop from baseline
        'dns_failure_rate': 0.35,         # >35% DNS failure rate
    }

    @classmethod
    def check_system_environment(cls):
        """Audits host machine for Big Data tools and determines operational mode."""
        env_status = {
            'python': True,
            'java': shutil.which('java') is not None,
            'hadoop': shutil.which('hadoop') is not None or os.path.exists(os.path.join(cls.HADOOP_HOME, 'bin', 'hadoop.cmd')),
            'hdfs': shutil.which('hdfs') is not None or os.path.exists(os.path.join(cls.HADOOP_HOME, 'bin', 'hdfs.cmd')),
            'pig': shutil.which('pig') is not None,
            'hive': shutil.which('hive') is not None,
            'mongodb': False,
            'wsl': shutil.which('wsl') is not None
        }

        # Check MongoDB connection
        try:
            from pymongo import MongoClient
            client = MongoClient(cls.MONGO_URI, serverSelectionTimeoutMS=800)
            client.admin.command('ping')
            env_status['mongodb'] = True
            client.close()
        except Exception:
            env_status['mongodb'] = False

        # Real Big Data is only ACTIVE if Hadoop, Pig, Hive and MongoDB are all truly functioning
        has_full_big_data = (
            env_status['hadoop'] and 
            env_status['pig'] and 
            env_status['hive'] and 
            env_status['mongodb'] and 
            not cls.FORCE_DEMO_MODE
        )

        return {
            'environment': env_status,
            'pipeline_mode': 'BIG DATA PIPELINE ACTIVE' if has_full_big_data else 'DEMO MODE',
            'is_demo_mode': not has_full_big_data
        }

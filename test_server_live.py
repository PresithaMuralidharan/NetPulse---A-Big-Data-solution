import urllib.request
import json

endpoints = [
    '/',
    '/live',
    '/outages',
    '/regions',
    '/isps',
    '/propagation',
    '/early-warning',
    '/recovery',
    '/historical',
    '/alerts',
    '/settings',
    '/api/network/summary',
    '/api/network/status',
    '/api/outages',
    '/api/regions',
    '/api/isps',
    '/api/propagation',
    '/api/predictions',
    '/api/recovery',
    '/api/alerts'
]

print("=== VERIFYING NETPULSE LIVE SERVER (http://127.0.0.1:5000) ===")
success_count = 0
for ep in endpoints:
    url = f"http://127.0.0.1:5000{ep}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NetPulse-Verifier'})
        with urllib.request.urlopen(req, timeout=4) as res:
            status = res.status
            content_type = res.headers.get('Content-Type', '')
            print(f"[OK] {status} {ep} ({content_type.split(';')[0]})")
            success_count += 1
    except Exception as e:
        print(f"[FAIL] {ep}: {e}")

print(f"\nVerification Results: {success_count}/{len(endpoints)} endpoints fully functional!")

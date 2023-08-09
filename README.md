# DHuS-LatencyMonitoring

Monitoring probes to watch ESA DataHub System redistribution latencies.

### Installation

```
apt install -y python3-virtualenv
virtualenv .
pip install -r requirements.txt
```

### Configuration

Fill `config.json` properly. Get yourself inspired by `config.json.template`.

### Usage

```
source bin/activate
python ./check_products.py
```

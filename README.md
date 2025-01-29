# `test-kde`

Test the duration of computing 1000 kernel density estimation of a data series
that has 40 points. This is typical of a moderate to high perf.compare
workload.

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
python ./test.py
```

# License

MIT

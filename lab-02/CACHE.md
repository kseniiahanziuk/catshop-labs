# Cache

Cache: pip downloads (`~/.cache/pip`), key `pip-Linux-py3.12-<hash of requirements.txt and requirements-dev.txt>`.

Cold run output: 
```bash
Cache saved with key: pip-Linux-py3.12-4bf497b2de56fe878be15bbb330d1759074719f0d99051fb8ed8d54755e0c408
```

Warm run output:
```bash
Cache hit occurred on the primary key pip-Linux-py3.12-4bf497b2de56fe878be15bbb330d1759074719f0d99051fb8ed8d54755e0c408, not saving cache.
```

| Run | `pip install` step | `test` job |
|---|---|---|
| cold (cache miss) | 6s | 20s |
| warm (cache hit) | 8s | 28s |
| warm (#2) | 3s | 11s |

For some reason, the "warm" run was the slower one. This might be caused by the fact that in our case there's not a lot of time to save: pip runs fast enough. Fetching the dependency files for the package from cache might be harder than using the optimized way from Github's runners.

To check it out, I re-run it for the third time. Third time is the charm, it was 2 times faster than both of the first 2 runs. Even though, this behaviour might not be stable. The increased speed may be caused by the fact that different virtual machines are involved in running different runs: a difference within a few seconds is normal in such environment. If our pipelines were taking more time to run and the processes underneath were harder, the diff will be visible, since the pipeline and the processes itself would take minutes, not seconds.
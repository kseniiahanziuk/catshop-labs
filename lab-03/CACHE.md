# Lab 3 - caches and the minutes

Workflow: `pipeline-lab-03` (caller) -> `_build-and-test` (reusable).

| | run | total duration |
|---|---|---|
| cold | https://github.com/kseniiahanziuk/catshop-labs/actions/runs/45894983127 | 1m 10s |
| warm | https://github.com/kseniiahanziuk/catshop-labs/actions/runs/45897264898 | 47s |
| saving | | 23s (≈33%) |

| cache | where | key | cold | warm |
|---|---|---|---|---|
| dependency | `actions/cache` in job `test` | `pip-Linux-py3.12-<hashFiles(lab-03/requirements*.txt)>`, fallback prefix `pip-Linux-py3.12-` | `python-env` step 7s (cache restore: miss) | `python-env` step 7s |
| layer | `cache-from` / `cache-to` `type=gha,mode=max` in job `build` | buildx manages it, scope `lab-03` | build step 22s; `pip install` layer 2.6s, nothing `CACHED`, cache export 14.7s | build step 10s; every layer `CACHED`, cache export 0.5s |

The layer cache did the work: the build step went from 22s to 10s. In the warm run every
Dockerfile step came back `CACHED`, and exporting the cache took 0.5s instead of 14.7s because
there were no new layers to write. The dependency cache made no difference you can see at step
level: `python-env` took 7s both times. The packages are small, and most of that step is
`setup-python` and upgrading pip, which the pip cache does not cover.

## Not cached

pip's own cache inside the image build (`pip install --no-cache-dir`). When `requirements.txt`
is unchanged, the whole install layer comes from the layer cache, so a pip cache inside the image
adds nothing. When it has changed, the layer has to be rebuilt anyway, and reusing pip's downloads
would need a `RUN --mount=type=cache`, which lives on the builder and is gone with the runner.
Keeping it out also keeps the image smaller.

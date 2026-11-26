# Lab 3 - caches and the minutes

Workflow: `pipeline-lab-03` (caller) -> `_build-and-test` (reusable).

| | run | total duration |
|---|---|---|
| cold | https://github.com/kseniiahanziuk/catshop-labs/actions/runs/45894983127 | 1m 10s |
| warm | TODO | TODO |
| saving | | TODO |

| cache | where | key | cold | warm |
|---|---|---|---|---|
| dependency | `actions/cache` in job `test` | `pip-Linux-py3.12-<hashFiles(lab-03/requirements*.txt)>`, fallback prefix `pip-Linux-py3.12-` | `python-env` step 7s (cache restore: miss) | TODO |
| layer | `cache-from` / `cache-to` `type=gha,mode=max` in job `build` | buildx manages it, scope `lab-03` | build step 22s; inside it `pip install` layer 2.6s, nothing `CACHED` | TODO |

## Not cached

pip's own cache inside the image build (`pip install --no-cache-dir`). When `requirements.txt`
is unchanged, the whole install layer comes from the layer cache, so a pip cache inside the image
adds nothing. When it has changed, the layer has to be rebuilt anyway, and reusing pip's downloads
would need a `RUN --mount=type=cache`, which lives on the builder and is gone with the runner.
Keeping it out also keeps the image smaller.

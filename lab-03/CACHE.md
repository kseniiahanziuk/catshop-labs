# Lab 3 - caches and the minutes

Workflow: `pipeline-lab-03` (caller) -> `_build-and-test` (reusable).

| | total duration |
|---|---|
| cold | TODO |
| warm | TODO |
| saving | TODO |

| cache | where | key | cold | warm |
|---|---|---|---|---|
| dependency | `actions/cache` in job `test` | `pip-Linux-py3.12-<hashFiles(lab-03/requirements*.txt)>`, fallback prefix `pip-Linux-py3.12-` | TODO: install step time | TODO |
| layer | `cache-from` / `cache-to` `type=gha,mode=max` in job `build` | buildx manages it, scope `lab-03` | TODO: build step time | TODO |

## Not cached

pip's own cache inside the image build (`pip install --no-cache-dir`). When `requirements.txt`
is unchanged, the whole install layer comes from the layer cache, so a pip cache inside the image
adds nothing. When it has changed, the layer has to be rebuilt anyway, and reusing pip's downloads
would need a `RUN --mount=type=cache`, which lives on the builder and is gone with the runner.
Keeping it out also keeps the image smaller.

import json


def results_to_json(results):
    return json.dumps(
        results,
        indent=4,
        ensure_ascii=False
    )
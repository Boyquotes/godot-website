import csv
from fuzzywuzzy import fuzz
from operator import itemgetter

match_threshold = 70
metadata = {
    "name": "GODOT (Graph of Dated Objects and Texts) Reconciliation Service - Roman Consulates",
    "defaultTypes": [{"id": "/people/person", "name": "Person"}],
    "view": {"url": "https://godot.date/id/{{id}}"},
    "preview": {"url": "https://godot.date/reconcile/preview={{id}}"}
    }

reader = csv.DictReader(open('app/Consulate_URIs.tsv', 'rt'), delimiter='\t')
records = [r for r in reader]


def search(query):
    matches = []
    for r in records:
        score = fuzz.partial_ratio(query, r['consul_names'])
        if score > match_threshold:
            if int(r['not_before']) < 0:
                not_before = str(int(r['not_before']) * - 1) + " BC"
            else:
                not_before = r['not_before'] + " AD"
            if int(r['not_after']) < 0:
                not_after = str(int(r['not_after']) * - 1) + " BC"
            else:
                not_after = r['not_after'] + " AD"
            matches.append({
                "id": r['godot_uri'],
                "name": r['consul_names'] + " (" + not_before + " - " + not_after  + ")",
                "score": score,
                "match": query == r['consul_names'],
                "type": [{"id": "/people/person", "name": "Person"}]
            })
    ordered_matches = sorted(matches, key=itemgetter('score'), reverse=True)
    return ordered_matches


def get_openrefine_metadata():
    return metadata

import csv
#import sys
#import simplejson as json
from fuzzywuzzy import fuzz
#from flask import Flask, request, jsonify
from collections import OrderedDict
from operator import itemgetter


# Matching threshold.
match_threshold = 70

# Basic service metadata. There are a number of other documented options
# but this is all we need for a simple service.
metadata = {
    "name": "GODOT (Graph of Dated Objects and Texts) Reconciliation Service - Roman Consulates",
    "defaultTypes": [{"id": "/people/person", "name": "Person"}],
    "view": {"url": "https://godot.date/id/{{id}}"},
    "preview": {"url": "https://godot.date/reconcile/preview={{id}}"}
    }

# Read in person records from csv file.
reader = csv.DictReader(open('app/Consulate_URIs.tsv', 'rt'), delimiter='\t')
records = [r for r in reader]


def search(query):
    # Initialize matches.
    matches = []
    # Search person records for matches.
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
    # sort matches by score & return orderedDict
    ordered_matches = sorted(matches, key=itemgetter('score'), reverse=True)
    return ordered_matches


def get_openrefine_metadata():
    return metadata
import json,sys
n=int(sys.argv[1]); done={l.split()[0] for l in open("jobs.tsv") if l.strip()}
q=[r for r in json.load(open("shot_requests_v001.json")) if str(r["index"]) not in done][:n]
print(json.dumps(q)); print("REMAINING_AFTER", len([r for r in json.load(open("shot_requests_v001.json")) if str(r["index"]) not in done])-len(q), file=sys.stderr)

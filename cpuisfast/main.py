import csv
import json

with open("data.csv") as f:
    reader = csv.reader(f)
    dr = csv.DictReader(
        f,
        fieldnames=[
            "model",
            "loop_per_second",
            "add_per_second",
            "system",
            "arch",
            "python_implementation",
            "python_version",
            "inserted_at",
        ],
    )
    cpus = list(dr)
    print(len(cpus))

with open("template.html") as tpl, open("dist/index.html", "wt") as out:
    template = tpl.read()
    rendered = template % (json.dumps(cpus),)
    out.write(rendered)

import json
from flask import Flask, abort
from os import path

app = Flask(__name__)

@app.route('/.well-known/terraform.json', methods=['GET'])
def discovery():
    return {"providers.v1": "/v1/providers/"}

@app.route('/v1/providers/<namespace>/<name>/versions', methods=['GET'])
def versions(namespace, name):
    filepath = 'providers/' + namespace + "/" + name + ".json"

    if not path.exists(filepath):
        abort(404)

    with open(filepath) as reader:
        data = json.load(reader)

    response = { "versions" : [] }

    for elem in data["versions"]:
        version = {"version": elem["version"], "protocols": elem["protocols"], "platforms": []}

        for platform in elem["platforms"]:
            version["platforms"].append({"os": platform["os"], "arch": platform["arch"]})

        response["versions"].append(version)
    
    return response

@app.route('/v1/providers/<namespace>/<name>/<version>/download/<os>/<arch>', methods=['GET'])
def package(namespace, name, version, os, arch):
    filepath = 'providers/' + namespace + "/" + name + ".json"

    if not path.exists(filepath):
        abort(404)

    with open(filepath) as reader:
        data = json.load(reader)

    provider = None

    for elem in data["versions"]:
        if elem["version"] == version:
            for platform in elem["platforms"]:
                if platform["os"] == os and platform["arch"]:
                    provider = platform
                    provider["protocols"] = elem["protocols"]
    
    if provider is None:
        abort(404)

    return provider
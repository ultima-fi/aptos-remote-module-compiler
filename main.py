import os

from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/health")
def health():
    return "healthy"


@app.route("/compile", methods=['POST'])
def compile():
    data = request.json
    print(data)
    name = data['name']
    address = data['address']
    hex = compile_module(name, address)
    return {"hex": hex}


def compile_module(name: str, address: str) -> str:
    move = f"module 0x{address}::{name} {{ struct {name} {{}} }}"
    with open('./sources/Module.move', 'w') as outf:
        outf.write(move)
    os.system('aptos move compile')

    with open(f'./build/module/bytecode_modules/{name}.mv', 'rb') as infile:
        hex = infile.read().hex()
    return hex


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

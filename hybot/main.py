import sys
from flask import Flask
from flask import request
from flask import jsonify

import hy

class Runner:
    def __init__(self):
        self._out_w = sys.stdout.write
        self._err_w = sys.stderr.write

    def reset(self):
        self._code = None
        self._stdout = []
        self._stderr = []
        self._value = None
        self._error = None

    def get_data(self):
        return {
            "code": self._code,
            "value": self._value,
            "error": self._error,
            "stdout": ''.join(self._stdout),
            "stderr": ''.join(self._stderr),
        }

    def __enter__(self):
        self.reset()
        sys.stdout.write = self._stdout.append
        sys.stderr.write = self._stderr.append
        return self

    def eval(self, code):
        self._code = code
        expr = hy.read_str(code)
        self._value = hy.eval(expr)

    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self._out_w
        sys.stderr.write = self._err_w
        if exc_value:
            self._error = str(exc_value)
        return True

def do_cmd(user, code):
    runner = Runner()
    with runner:
        runner.eval(code)
    data = runner.get_data()

    header = f"###### Hybot executed a piece of code on behalf of @{user}"
    code = f"""
CODE:
```lisp
{data['code']}
```
"""
    value = ""
    if data["value"]:
        value = f"""
VALUE:
```
{data["value"]}
```
"""
    error = ""
    if data["error"]:
        error = f"""
ERROR:
```
{data["error"]}
```
    """
    stdout = ""
    if data["stdout"]:
        stdout = f"""
STDOUT:
```
{data["stdout"]}
```
"""
    stderr = ""
    if data["stderr"]:
        stderr = f"""
STDERR:
```
{data["stderr"]}
```
"""

    return "\n".join([header, code, value, error, stdout, stderr])

# https://docs.mattermost.com/developer/slash-commands.html
# https://developers.mattermost.com/integrate/slash-commands/#parameters
def gcp_main(request):
    user = request.form.get("user_name", "UnknownUser")
    text = request.form.get("text", "")
    return jsonify({
        "response_type": "in_channel",
        "text": do_cmd(user, text),
    })

def homepage():
    return "Hi, I'm hybot!"

def hybot():
    return gcp_main(request)


def alifunction(environ, start_response):
    app = Flask(__name__)
    app.route('/', methods=['POST'])(hybot)
    return app(environ, start_response)

if __name__ == "__main__":
    app = Flask(__name__)
    app.route('/')(homepage)
    app.route('/hybot', methods=['POST'])(hybot)
    app.run(debug=True)

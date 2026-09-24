from flask import Flask, request
from markupsafe import escape
from waitress import serve

import urllib.request
import urllib.parse
import json
import ast
import operator
import re


# ============================================================
# AKSHAR AI WEB VERSION
# PART 1 / 4
# ============================================================

app = Flask(__name__)


# ============================================================
# CALCULATOR
# ============================================================

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}


def calculate(expression):

    expression = expression.replace("×", "*")
    expression = expression.replace("÷", "/")

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        def solve(node):

            if isinstance(
                node,
                ast.Constant
            ):

                if isinstance(
                    node.value,
                    (int, float)
                ):

                    return node.value

                raise ValueError()

            if isinstance(
                node,
                ast.BinOp
            ):

                left = solve(node.left)
                right = solve(node.right)

                operation = operators.get(
                    type(node.op)
                )

                if operation is None:
                    raise ValueError()

                return operation(
                    left,
                    right
                )

            if isinstance(
                node,
                ast.UnaryOp
            ):

                value = solve(
                    node.operand
                )

                if isinstance(
                    node.op,
                    ast.USub
                ):

                    return -value

                if isinstance(
                    node.op,
                    ast.UAdd
                ):

                    return value

            raise ValueError()

        result = solve(tree.body)

        return str(result)

    except Exception:

        return None


# ============================================================
# WIKIPEDIA INTERNET SEARCH
# ============================================================

def wikipedia_search(query):

    try:

        url = (
            "https://en.wikipedia.org/w/api.php?"
            + urllib.parse.urlencode({

                "action": "query",

                "format": "json",

                "prop": "extracts",

                "exintro": True,

                "explaintext": True,

                "redirects": 1,

                "titles": query

            })
        )

        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "AksharAI/1.0"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=8
        ) as response:

            data = json.loads(
                response.read().decode(
                    "utf-8"
                )
            )

        pages = data[
            "query"
        ][
            "pages"
        ]

        for page in pages.values():

            extract = page.get(
                "extract",
                ""
            )

            if extract:

                return extract[:2500]

        return None

    except Exception:

        return None
        # ============================================================
# AKSHAR AI RESPONSE SYSTEM
# PART 2 / 4
# ============================================================


def akshar_ai(message):

    text = message.strip()

    lower = text.lower()


    # ========================================================
    # EMPTY MESSAGE
    # ========================================================

    if not text:

        return (
            "Bhai, kuch question likho 🙂"
        )


    # ========================================================
    # GREETING
    # ========================================================

    if lower in [
        "hi",
        "hello",
        "hey",
        "hii",
        "namaste",
        "namaskar"
    ]:

        return (
            "Namaste! 👋\n\n"
            "Main Akshar AI hoon. 🤖\n"
            "Mujhse apna question pucho."
        )


    # ========================================================
    # IDENTITY
    # ========================================================

    if (
        "tumhara naam" in lower
        or "your name" in lower
        or "who are you" in lower
    ):

        return (
            "Mera naam Akshar AI hai. 🤖"
        )


    # ========================================================
    # CALCULATOR
    # ========================================================

    calculation_text = re.sub(
        r"^(calculate|calc|solve)\s+",
        "",
        text,
        flags=re.I
    )


    result = calculate(
        calculation_text
    )


    if result is not None:

        return (
            "🧮 Calculation Result:\n\n"
            + result
        )


    # ========================================================
    # DATE
    # ========================================================

    if (
        "date" in lower
        or "today" in lower
    ):

        from datetime import datetime

        now = datetime.now()

        return (
            "📅 Today is: "
            + now.strftime("%d-%m-%Y")
        )


    # ========================================================
    # INTERNET INFORMATION
    # ========================================================

    if any(
        word in lower
        for word in [
            "who is",
            "what is",
            "what are",
            "where is",
            "when was",
            "tell me about",
            "information about"
        ]
    ):

        result = wikipedia_search(
            text
        )


        if result:

            return (
                "🌐 Internet Information:\n\n"
                + result
            )


    # ========================================================
    # BASIC CHAT
    # ========================================================

    if "how are you" in lower:

        return (
            "Main bilkul ready hoon bhai! 😄"
        )


    if "thank" in lower:

        return (
            "You're welcome bhai! 😊"
        )


    # ========================================================
    # FALLBACK
    # ========================================================

    return (
        "🤖 Main tumhara question samajhne "
        "ki koshish kar raha hoon.\n\n"
        "Agar information chahiye to question "
        "thoda clearly likho."
    )
    # ============================================================
# WEB PAGE + MESSAGE ROUTE
# PART 3 / 4
# ============================================================


@app.route("/", methods=["GET", "POST"])
def home():

    user_message = ""
    ai_response = ""

    if request.method == "POST":

        user_message = request.form.get(
            "message",
            ""
        )

        user_message = user_message.strip()

        if user_message:

            ai_response = akshar_ai(
                user_message
            )

        else:

            ai_response = (
                "Bhai, kuch question likho 🙂"
            )


    return f"""
<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
      content="width=device-width,
      initial-scale=1.0">

<title>Akshar AI</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f2f2f2;
    padding: 20px;
}}

.box {{
    max-width: 600px;
    margin: auto;
    background: white;
    padding: 20px;
    border-radius: 15px;
}}

h1 {{
    text-align: center;
}}

input {{
    width: 100%;
    padding: 12px;
    box-sizing: border-box;
    border-radius: 8px;
    border: 1px solid #aaa;
    margin-bottom: 10px;
}}

button {{
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 8px;
    background: #333;
    color: white;
    font-size: 16px;
}}

.question {{
    margin-top: 20px;
    padding: 12px;
    background: #eeeeee;
    border-radius: 8px;
}}

.answer {{
    margin-top: 10px;
    padding: 12px;
    background: #e8f5e9;
    border-radius: 8px;
}}

</style>

</head>


<body>

<div class="box">

<h1>🤖 Akshar AI</h1>

<p style="text-align:center;">
Ask me something!
</p>


<form method="POST">

<input
    type="text"
    name="message"
    placeholder="Type your question..."
    value="{escape(user_message)}"
    autocomplete="off"
>


<button type="submit">
Ask Akshar AI 🚀
</button>

</form>


{"<div class='question'><b>You:</b><br>"
+ escape(user_message)
+ "</div>" if user_message else ""}


{"<div class='answer'><b>Akshar AI:</b><br>"
+ escape(ai_response)
+ "</div>" if ai_response else ""}


</div>

</body>

</html>
"""
# ============================================================
# SERVER START
# PART 4 / 4
# ============================================================


if __name__ == "__main__":

    print()
    print("=" * 55)
    print("🤖 AKSHAR AI WEB VERSION")
    print("=" * 55)

    print()
    print("🚀 Starting Akshar AI server...")
    print()

    print("✅ Flask loaded!")
    print("✅ Waitress loaded!")
    print()

    print("🌐 Open this address in your browser:")
    print()
    print("🔗 http://127.0.0.1:8080")
    print()

    print("🛑 Stop server with CTRL+C")
    print("=" * 55)
    print()

    serve(
        app,
        host="0.0.0.0",
        port=8080
    )
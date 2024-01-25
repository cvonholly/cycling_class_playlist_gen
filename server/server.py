from flask import Flask, jsonify

# app instance
app = Flask(__name__)

@app.route("/api/test")
def return_test():
    return jsonify({
        'message': "Hello World!"
    })

if __name__ == "__main__":
    app.run(debug=True)
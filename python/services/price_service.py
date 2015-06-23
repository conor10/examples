from flask import app, Flask, jsonify, request
import bm


app = Flask(__name__)


@app.route('/gbm')
def gbm():
    args = request.args

    periods = int(args.get('periods'))
    start_price = float(args.get('startPrice'))
    mu = float(args.get('mu'))
    sigma = float(args.get('sigma'))
    delta = float(args.get('delta'))

    prices = bm.generate_gbm_prices(periods, start_price, mu, sigma, delta)
    return jsonify(result=prices.tolist())


if __name__ == "__main__":
    app.run()

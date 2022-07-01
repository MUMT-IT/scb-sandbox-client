from flask import jsonify
import requests

from app import app

AUTH_URL = 'https://api-sandbox.partners.scb/partners/sandbox/v1/oauth/token'
QRCODE_URL = 'https://api-sandbox.partners.scb/partners/sandbox/v1/payment/qrcode/create'
APP_KEY = ''
APP_SECRET = ''
BILLERID = ''


@app.route('/')
def index():
    return jsonify({'message': 'Hello, world'})


@app.route('/qrcode/<int:amount>')
def generate_qrcode(amount):
    # curl -X POST
    headers = {
        'Content-Type': 'application/json',
        'requestUId': '85230887-e643-4fa4-84b2-4e56709c4ac4',
        'resourceOwnerId': APP_KEY
    }
    response = requests.post(AUTH_URL, headers=headers, json={
        'applicationKey': APP_KEY,
        'applicationSecret': APP_SECRET
    })
    response_data = response.json()
    print(response_data['data'])
    access_token = response_data['data']['accessToken']
    print('The access token is {}'.format(access_token))

    headers['authorization'] = 'Bearer {}'.format(access_token)

    qrcode_resp = requests.post(QRCODE_URL, headers=headers, json={
        'qrType': 'PP',
        'amount': '{}'.format(amount),
        'ppType': 'BILLERID',
        'ppId': BILLERID,
        'ref1': '1234567890',
        'ref2': '0987654321',
        'ref3': 'MXU',
    })
    qr_image = qrcode_resp.json()['data']['qrImage']
    return """
    <html>
    <body>
    <h1>Please scan to pay</h1>
    <img src="data:image/png;base64,{}"
    </body>
    </html>
    """.format(qr_image)

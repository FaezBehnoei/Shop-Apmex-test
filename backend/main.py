from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import uuid, random, datetime

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret1'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False  # فقط برای لوکال‌ ها؛ روی سرور باید True باشه
app.config['JWT_COOKIE_HTTPONLY'] = True
app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token_cookie'
CORS(app, supports_credentials=True)

jwt = JWTManager(app)

# دیکشنری برای نگهداری کاربران ثبت نام شده نهایی
# کلید می‌تواند نام کاربری یا شناسه کاربر باشد
# مقدار می‌تواند دیکشنری شامل هش پسورد و سایر اطلاعات باشد
REGISTERED_USERS = {
    "admin": {"password_hash": "hashed_password_for_admin"} # مثال - پسوردها باید هش شوند
}

# دیکشنری برای نگهداری اطلاعات OTP های در انتظار تایید
# کلید: otp_token
# مقدار: دیکشنری شامل {'otp_code': '123456', 'phone_number': '...', 'national_id': '...', 'expires_at': datetime_object, 'verified': False}
otp_data_store = {}

# دیکشنری برای نگهداری پروفایل های کاربری موقت پس از تایید OTP و قبل از ثبت نام نهایی
# کلید: می تواند شماره تلفن یا کد ملی باشد
# مقدار: user_profile
pending_registration_profiles = {}

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == 'admin' and data['password'] == '1234':
        access_token = create_access_token(identity=data['username'])
        response = jsonify({'message': 'ورود موفق'})
        response.set_cookie('access_token_cookie', access_token, httponly=True)
        return response
    return jsonify({'message': 'ورود نامعتبر'}), 401

@app.route('/auth/initiate-registration', methods=['POST'])
def initiate_registration():
    data = request.json
    phone_number = data['phone_number']
    national_id = data['national_id']
    if not phone_number or not national_id:
        return jsonify({'message': 'شماره تلفن و کد ملی الزامی است'}), 400
    #TODO Check if Match phone_number with national_id
    otp_token = uuid.uuid4().hex
    actual_otp_code = str(random.randint(10000, 99999))
    print(actual_otp_code)
    expires_in_seconds = 120
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in_seconds)
    otp_data_store[otp_token] = {
        'otp_code': actual_otp_code,
        'phone_number': phone_number,
        'national_id': national_id,
        'expires_in': expires_in_seconds,
        'expires_at': expires_at,
        'verified': False # وضعیت تایید OTP
    }
    return jsonify({'otp_token': otp_token, 'expires_in':90})

@app.route('/auth/verify-otp', methods=['POST'])
def verify_otp():
    try:
        data = request.json
        print("🟡 OTP VERIFY Payload:", data)
        
        user_entered_otp_code = data.get('otp_code')
        otp_token = data.get('otp_token')

        if not user_entered_otp_code or not otp_token:
            return jsonify({'message': 'کد OTP و توکن OTP الزامی است'}), 400

        otp_info = otp_data_store.get(otp_token)

        if not otp_info:
            print("🔴 Token Not Found:", otp_token)
            return jsonify({'message': 'توکن OTP نامعتبر یا منقضی شده است'}), 404

        if datetime.datetime.now(datetime.timezone.utc) > otp_info['expires_at']:
            del otp_data_store[otp_token]
            return jsonify({'message': 'کد OTP منقضی شده است'}), 400

        if otp_info['otp_code'] == user_entered_otp_code:
            otp_info['verified'] = True
            user_identifier = f"user_{otp_info['phone_number']}"

            user_profile = {
                "identifier": user_identifier,
                "user_id": "",
                "first_name": f"First Name of {otp_info['phone_number']}",
                "last_name": f"Last Name of {otp_info['phone_number']}",
                "phone_number": otp_info['phone_number'],
                "national_id": otp_info.get('national_id', ""),  # اگر وجود نداشته باشد، خالی باشد
                "otp_verified_token": otp_token
            }

            pending_registration_profiles[otp_token] = user_profile

            return jsonify({
                'message': 'OTP با موفقیت تایید شد.',
                'user_profile': user_profile,
                'registration_token': otp_token
            }), 200
        else:
            return jsonify({'message': 'کد OTP نامعتبر است'}), 400
    except Exception as e:
        print("❌ OTP Verify Error:", str(e))
        return jsonify({"message": "خطای سرور", "details": str(e)}), 500


@app.route('/auth/register', methods=['POST'])
def user_register():
    data = request.json
    phone_number = data['phone_number']
    invite_code = data['invite_code']
    #TODO Check if Match otp_code with otp_token
    user_profile = {
    "identifier": "string",
    "password": "string",
    "user_id": "string",
    "first_name": "string",
    "last_name": "string",
    "phone_number": "string",
    "national_id": "string"
                    }
    return jsonify({'user_profile': user_profile})

@app.route('/logout', methods=['POST'])
def logout():
    response = jsonify({'message': 'خروج انجام شد'})
    unset_jwt_cookies(response)
    return response




@app.route('/wallet/summary')
def wallet_summary():
    method = request.args.get('method')
    res = {
            "total_value": 6243000000,
            "assets": [
                {
                "id": 1,
                "name": "موجودی ریالی",
                "amount": 16557000,
                "unit": "ریال",
                "price_per_unit": 0,
                "slug": "rial",
                "data": 4000000
                },
                {
                "id": 2,
                "name": "طلا خام",
                "amount": 5.02,
                "unit": "گرم",
                "price_per_unit": 67320,
                "slug": "gold",
                "data": 25000000
                },
                {
                "id": 3,
                "name": "نقره خام",
                "amount": 4.05,
                "unit": "گرم",
                "price_per_unit": 51300,
                "slug": "silver",
                "data": 20000000
                },
                {
                "id": 4,
                "name": "شمش",
                "amount": 2,
                "unit": "عدد",
                "price_per_unit": 0,
                "slug": "ignot",
                "data": 5000000
                }
            ]
            }
    return res

@app.route('/wallet/asset-detail/<slug>', methods=['GET'])
def get_asset_detail(slug):
    assets_data = {
        "gold": {
            "slug": "gold",
            "asset": {
                "id": 2,
                "name": "طلا",
                "amount": 5.02,
                "unit": "گرم",
                "price_per_unit": 67320,
                "slug": "gold",
                "profit_percent": 12.5,
                "profit_amount": 5557000
            },
            "transactions": [
                {
                    "id": 1,
                    "status": 2,
                    "amount": "۳۳,۵۵۷,۰۰۰",
                    "type": "تبدیل ریال به طلا",
                    "time": "۱۰:۳۰:۵۰",
                    "date": "۱۴۰۳/۰۶/۲۳"
                },
                {
                    "id": 2,
                    "status": 1,
                    "amount": "۳۳,۵۵۷,۰۰۰",
                    "type": "واریز به حساب",
                    "time": "۱۰:۳۱:۰۰",
                    "date": "۱۴۰۳/۰۶/۲۳"
                }
            ],
            "timestamps": [
                "۰۹:۳۰:۰۰", "۱۲:۳۰:۰۰", "۱۵:۳۰:۰۰", "۱۸:۳۰:۰۰", "۲۱:۳۰:۰۰", "۰۰:۳۰:۰۰"
            ],
            "chart_data": {
                "24h": {
                    "chart": [5400000, 5550000, 5650000, 5900000, 6200000, 7046600],
                    "summary": { "profit_percent": -2.7 }
                },
                "1w": {
                    "chart": [5400000, 5500000, 5600000, 5800000, 6000000, 6400000],
                    "summary": { "profit_percent": 3.7 }
                },
                "1m": {
                    "chart": [5300000, 5450000, 5600000, 5750000, 5900000, 6200000],
                    "summary": { "profit_percent": 5.7 }
                },
                "3m": {
                    "chart": [5300000, 5450000, 5600000, 5750000, 5900000, 6200000],
                    "summary": { "profit_percent": 5.7 }
                },
                "1y": {
                    "chart": [5000000, 5300000, 5600000, 6000000, 6400000, 6750000],
                    "summary": { "profit_percent": 1.7 }
                }
            }
        },
        "rial": {
            "slug": "rial",
            "asset": {
                "id": 1,
                "name": "موجودی ریالی",
                "amount": 16557000,
                "unit": "ریال",
                "price_per_unit": 0,
                "slug": "rial",
                "profit_percent": 0.5,
                "profit_amount": 80000
            },
            "transactions": [
                {
                    "id": 1,
                    "status": 3,
                    "amount": "۸۰,۰۰۰",
                    "type": "واریز",
                    "time": "۰۹:۰۰:۰۰",
                    "date": "۱۴۰۳/۰۶/۲۰"
                }
            ],
            "timestamps": [
                "۰۹:۰۰:۰۰", "۱۲:۰۰:۰۰", "۱۵:۰۰:۰۰", "۱۸:۰۰:۰۰", "۲۱:۰۰:۰۰", "۰۰:۰۰:۰۰"
            ],
            "chart_data": {
                "24h": {
                    "chart": [4000000, 4050000, 4100000, 4150000, 4200000, 4250000],
                    "summary": { "profit_percent": 1.25 }
                },
                "1w": {
                    "chart": [3900000, 3950000, 4000000, 4050000, 4100000, 4200000],
                    "summary": { "profit_percent": 2.0 }
                },
                "1m": {
                    "chart": [3500000, 3700000, 3900000, 4100000, 4300000, 4500000],
                    "summary": { "profit_percent": 4.5 }
                }
            }
        },
        "silver": {
            "slug": "silver",
            "asset": {
                "id": 3,
                "name": "نقره",
                "amount": 4.05,
                "unit": "گرم",
                "price_per_unit": 51300,
                "slug": "silver",
                "profit_percent": 3.2,
                "profit_amount": 230000
            },
            "transactions": [
                {
                    "id": 1,
                    "status": 1,
                    "amount": "۲۰۰,۰۰۰",
                    "type": "خرید نقره",
                    "time": "۱۳:۰۰:۰۰",
                    "date": "۱۴۰۳/۰۶/۲۲"
                }
            ],
            "timestamps": [
                "۰۸:۰۰:۰۰", "۱۱:۰۰:۰۰", "۱۴:۰۰:۰۰", "۱۷:۰۰:۰۰", "۲۰:۰۰:۰۰", "۲۳:۰۰:۰۰"
            ],
            "chart_data": {
                "24h": {
                    "chart": [500000, 520000, 530000, 550000, 570000, 590000],
                    "summary": { "profit_percent": 2.5 }
                },
                "1w": {
                    "chart": [480000, 490000, 500000, 520000, 540000, 560000],
                    "summary": { "profit_percent": 4.1 }
                },
                "1m": {
                    "chart": [450000, 470000, 490000, 510000, 530000, 550000],
                    "summary": { "profit_percent": 6.3 }
                }
            }
        },
        "ignot": {
            "slug": "ignot",
            "asset": {
                "id": 4,
                "name": "شمش",
                "amount": 2,
                "unit": "عدد",
                "price_per_unit": 3400000,
                "slug": "ignot",
                "profit_percent": -1.1,
                "profit_amount": -72000
            },
            "transactions": [
                {
                    "id": 1,
                    "status": 1,
                    "amount": "۶,۸۱۱,۰۰۰",
                    "type": "خرید شمش",
                    "time": "۱۴:۱۰:۰۰",
                    "date": "۱۴۰۳/۰۶/۲۳"
                }
            ],
            "timestamps": [
                "۰۹:۰۰:۰۰", "۱۱:۰۰:۰۰", "۱۳:۰۰:۰۰", "۱۵:۰۰:۰۰", "۱۷:۰۰:۰۰", "۱۹:۰۰:۰۰"
            ],
            "chart_data": {
                "24h": {
                    "chart": [3300000, 3320000, 3340000, 3360000, 3380000, 3400000],
                    "summary": { "profit_percent": 0.6 }
                },
                "1w": {
                    "chart": [3200000, 3250000, 3300000, 3350000, 3400000, 3450000],
                    "summary": { "profit_percent": 2.5 }
                },
                "1m": {
                    "chart": [3100000, 3200000, 3300000, 3400000, 3500000, 3600000],
                    "summary": { "profit_percent": 4.8 }
                }
            }
        }
    }

    asset_info = assets_data.get(slug)
    if not asset_info:
        abort(404, description="Asset not found")
    return jsonify([asset_info])



@app.route('/wallet/transactions', methods=['GET'])
def wallet_get_transactions():
    transactions = [
        {
            "id": 1,
            "status": 3,
            "amount": "۳۳,۵۵۷,۰۰۰",
            "type": "واریز",
            "time": "۱۰:۳۰:۵۰",
            "date": "۱۴۰۳/۰۶/۲۳",
            "category": "واریز"
        },
        {
            "id": 2,
            "status": 2,
            "amount": "۱۲۰,۰۰۰,۰۰۰",
            "type": "برداشت",
            "time": "۱۱:۰۰:۰۰",
            "date": "۱۴۰۳/۰۶/۲۳",
            "category": "برداشت"
        },
        {
            "id": 3,
            "status": 1,
            "amount": "۱۰۰,۰۰۰,۰۰۰",
            "type": "خرید طلا",
            "time": "۱۲:۳۰:۰۰",
            "date": "۱۴۰۳/۰۵/۲۰",
            "category": "طلا"
        }
    ]

    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    status = request.args.get("status")
    type_ = request.args.get("type")
    amount_from = request.args.get("amount_from")
    amount_to = request.args.get("amount_to")
    search = request.args.get("search")
    category = request.args.get("category")

    filtered = transactions

    if date_from:
        filtered = [t for t in filtered if t["date"] >= date_from]
    if date_to:
        filtered = [t for t in filtered if t["date"] <= date_to]
    if status:
        filtered = [t for t in filtered if str(t["status"]) == str(status)]
    if type_:
        filtered = [t for t in filtered if t["type"] == type_]
    if amount_from:
        filtered = [t for t in filtered if int(t["amount"].replace(',', '')) >= int(amount_from)]
    if amount_to:
        filtered = [t for t in filtered if int(t["amount"].replace(',', '')) <= int(amount_to)]
    if search:
        filtered = [t for t in filtered if search in t["type"] or search in t["category"]]
    if category:
        filtered = [t for t in filtered if t["category"] == category]
    return jsonify({"transactions": filtered})

@app.route('/wallet/assets', methods=['GET'])
def get_assets():
    assets = [
        {
            "id": 1,
            "name": "موجودی ریالی",
            "slug": "rial",
            "amount": "۱۶٬۵۵۷٬۰۰۰",
            "unit": "ریال",
            "pricePerUnit": None
        },
        {
            "id": 2,
            "name": "طلا خام",
            "slug": "gold",
            "amount": "۵.۰۲",
            "unit": "گرم",
            "pricePerUnit": "۶۷٬۳۲۰٬۰۰۰"
        },
        {
            "id": 3,
            "name": "نقره خام",
            "slug": "silver",
            "amount": "۴.۰۵",
            "unit": "گرم",
            "pricePerUnit": "۵۱٬۳۰۰"
        }
    ]
    return jsonify({"assets": assets})

@app.route('/wallet/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    asset_slug = data.get('asset_slug')
    amount = data.get('amount')
    shaba_number = data.get('shaba_number')
    chash_amount = data.get('chash_amount')

    # You can add your validation and processing here

    return jsonify({"Successes": True})

@app.route('/wallet/shop-products', methods=['GET'])
def get_shop_products():
    products = [
        {
            "id": 1,
            "image": "/images/Frame 2578 (1).png",
            "title": "شمش ۱ گرمی گلدیس",
            "ayar": 750,
            "price": 6811000,
            "PendingDelivery": True,
            "method": "inPerson"
        },
        {
            "id": 2,
            "image": "/images/Frame 2578 (1).png",
            "title": "شمش ۲ گرمی محمد",
            "ayar": 750,
            "price": 6811000,
            "PendingDelivery": True,
            "method": "byPost"
        },
        {
            "id": 3,
            "image": "/images/Frame 2578 (1).png",
            "title": "شمش 4 گرمی محمد",
            "ayar": 750,
            "price": 6811000,
            "PendingDelivery": False
        },
        {
            "id": 4,
            "image": "/images/Frame 2578 (1).png",
            "title": "شمش 4 گرمی محمد",
            "ayar": 750,
            "price": 6811000,
            "PendingDelivery": False
        }
    ]

    category = request.args.get("category")
    filtered_products = products
    if category:
        filtered_products = [p for p in products if category in p["title"]]

    response = {
        "shopProducts": {
            "products": filtered_products,
            "ignotAmount": 6165557000
        }
    }
    return jsonify(response)

@app.route('/wallet/shop-products/<int:id>', methods=['GET'])
def get_shop_product(id):
    products = [
        {
            "id": 1,
            "category": "شمش",
            "image": [
                "/images/products-wallet-store.png",
                "/images/Frame 2578 (1).png",
                "/images/Frame 2578 (1).png"
            ],
            "title": "شمش ۱ گرمی گلدیس",
            "ayar": 750,
            "price": 6811000,
            "PendingDelivery": True,
            "method": "inPerson",
            "orderNumber": 54453454,
            "currentPrice": 6920000,
            "profit": 25,
            "date": "1404/02/15",
            "delivery": {
                "address": "هفته دوم صادقیه، واحد ۲",
                "latitude": 35.7,
                "longitude": 51.4,
                "timing": {
                    "date": "1404/02/05",
                    "time": "12:00",
                    "day": "چهارشنبه"
                }
            }
        },
        {
            "id": 2,
            "category": "شمش",
            "image": [
                "/images/Frame 2578 (1).png"
            ],
            "title": "شمش ۲ گرمی محمد",
            "ayar": 750,
            "price": 6811000,
            "PendingDelivery": True,
            "method": "byPost",
            "orderNumber": 87654321,
            "currentPrice": 7000000,
            "profit": -15,
            "date": "1404/02/10",
            "delivery": {
                "address": "تهران، میدان ولیعصر، کوچه ۱۲",
                "latitude": 35.715,
                "longitude": 51.4045,
                "phone": 9126453763,
                "timing": {
                    "date": "1403/03/05",
                    "time": "14:00",
                    "day": "پنج‌شنبه"
                }
            }
        },
        {
            "id": 3,
            "category": "شمش",
            "image": [
                "/images/Frame 2578 (1).png"
            ],
            "title": "شمش ۴ گرمی محمد",
            "ayar": 750,
            "price": 6811000,
            "PendingDelivery": False,
            "orderNumber": 98765432,
            "currentPrice": 7200000,
            "profit": 54,
            "date": "1404/02/05"
        },
        {
            "id": 4,
            "category": "شمش",
            "image": [
                "/images/Frame 2578 (1).png",
                "/images/Frame 2578 (1).png"
            ],
            "title": "شمش ۱ گرمی گلدیس",
            "ayar": 350,
            "price": 6811000,
            "PendingDelivery": True,
            "method": "inPerson",
            "orderNumber": 54453454,
            "currentPrice": 6920000,
            "profit": 25,
            "date": "1404/02/15",
            "delivery": {
                "address": "میدان دوم صادقیه، واحد ۲",
                "latitude": 32.6546,
                "longitude": 51.4,
                "timing": {
                    "date": "1401/02/05",
                    "time": "12:00",
                    "day": "چهارشنبه"
                }
            }
        }
    ]

    filtered_products = [p for p in products if p["id"] == id]

    response = {
        "shopProducts": filtered_products,
        "shopSummary": {
            "ignotAmount": 6165557000
        }
    }
    return jsonify(response)

@app.route('/wallet/addresses-with-timestamps', methods=['GET'])
def addresses_with_timestamps():
    method = request.args.get('method', 'byPost')

    response = {
        "addresses": [
            {
                "address": "تهران، صندوق پستی 4567",
                "id": 4,
                "latitude": 35.744,
                "longitude": 51.375,
                "timestamp": "2025-05-14T10:00:00Z",
                "title": "تهران"
            },
            {
                "address": "اصفهان، صندوق پستی 8910",
                "id": 5,
                "latitude": 32.6546,
                "longitude": 51.6674,
                "timestamp": "2025-05-14T10:00:00Z",
                "title": "اصفهان"
            }
        ],
        "dates": [
            {
                "date": "۱۴",
                "day": "شنبه",
                "id": 1,
                "slots": [
                    "۱۰:۰۰ - ۱۲:۰۰",
                    "۱۲:۰۰ - ۱۴:۰۰",
                    "۱۴:۰۰ - ۱۶:۰۰",
                    "۱۶:۰۰ - ۱۸:۰۰",
                    "۱۸:۰۰ - ۲۰:۰۰"
                ]
            },
            {
                "date": "۱۵",
                "day": "یکشنبه",
                "id": 2,
                "slots": [
                    "۱۰:۰۰ - ۱۲:۰۰",
                    "۱۲:۰۰ - ۱۴:۰۰",
                    "۱۴:۰۰ - ۱۶:۰۰",
                    "۱۶:۰۰ - ۱۸:۰۰",
                    "۱۸:۰۰ - ۲۰:۰۰"
                ]
            },
            {
                "date": "۱۶",
                "day": "دوشنبه",
                "id": 3,
                "slots": [
                    "۱۰:۰۰ - ۱۲:۰۰",
                    "۱۲:۰۰ - ۱۴:۰۰",
                    "۱۴:۰۰ - ۱۶:۰۰",
                    "۱۶:۰۰ - ۱۸:۰۰",
                    "۱۸:۰۰ - ۲۰:۰۰"
                ]
            },
            {
                "date": "۱۷",
                "day": "سه‌شنبه",
                "id": 4,
                "slots": [
                    "۱۰:۰۰ - ۱۲:۰۰",
                    "۱۲:۰۰ - ۱۴:۰۰",
                    "۱۴:۰۰ - ۱۶:۰۰",
                    "۱۶:۰۰ - ۱۸:۰۰",
                    "۱۸:۰۰ - ۲۰:۰۰"
                ]
            }
        ],
        "method": method
    }
    return jsonify(response)



######################################################################################################
##################################################################### Faeze frontend test ############
######################################################################################################
# Login / register 

@app.route('/auth/request-otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    identifier = data.get('identifier')

    if not identifier:
        return jsonify({"message": "شماره موبایل الزامی است"}), 400

    # تولید OTP و token
    otp_token = uuid.uuid4().hex
    actual_otp_code = str(random.randint(10000, 99999))
    expires_in = 180
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)

    # ذخیره در دیتاست موقتی
    otp_data_store[otp_token] = {
        "otp_code": actual_otp_code,
        "phone_number": identifier,
        "expires_in": expires_in,
        "expires_at": expires_at,
        "verified": False
    }

    print("📨 OTP Code:", actual_otp_code)  # در پروژه واقعی: این ارسال باید SMS باشد

    return jsonify({
        "otp_token": otp_token,
        "message": "OTP sent successfully",
        "expires_in": expires_in
    }), 200

reset_password_tokens = {}

@app.route('/auth/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    phone_number = data.get("phone_number")

    if not phone_number:
        return jsonify({"message": "شماره موبایل الزامی است"}), 400

    reset_token = uuid.uuid4().hex
    otp_code = str(random.randint(10000, 99999))
    expires_in = 300
    expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)

    reset_password_tokens[reset_token] = {
        "otp_code": otp_code,
        "phone_number": phone_number,
        "expires_at": expires_at,
        "verified": False
    }

    # 👇 اضافه کردن این خط برای تست لوکال ضروریه
    print("📨 Forgot Password OTP:", otp_code)

    return jsonify({
        "reset_token": reset_token,
        "expires_in": expires_in
    }), 200

@app.route('/auth/verify-reset-otp', methods=['POST'])
def verify_reset_otp():
    data = request.get_json()
    otp_code = data.get("otp_code")
    otp_token = data.get("otp_token")  # یعنی reset_token

    if not otp_code or not otp_token:
        return jsonify({"message": "کد و توکن الزامی است"}), 400

    otp_info = reset_password_tokens.get(otp_token)  # ✅ اصلاح این خط

    if not otp_info:
        return jsonify({"message": "توکن نامعتبر یا منقضی شده است"}), 404

    if datetime.datetime.now(datetime.timezone.utc) > otp_info["expires_at"]:
        del reset_password_tokens[otp_token]
        return jsonify({"message": "کد OTP منقضی شده است"}), 400

    if otp_info["otp_code"] == otp_code:
        otp_info["verified"] = True
        return jsonify({"message": "OTP verified for password reset"}), 200
    else:
        return jsonify({"message": "کد نادرست است"}), 400

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    new_password = data.get("new_password")
    otp_token = data.get("otp_token")  # 👈 این باید از فرانت ارسال بشه

    if not new_password or not otp_token:
        return jsonify({"message": "پسورد جدید و توکن الزامی است"}), 400

    otp_info = reset_password_tokens.get(otp_token)

    if not otp_info:
        return jsonify({"message": "توکن نامعتبر است"}), 404

    if not otp_info.get("verified", False):
        return jsonify({"message": "کد تایید نشده است"}), 400

    phone_number = otp_info["phone_number"]

    # در دیتابیس ذخیره نشده ولی برای تست، در همین حافظه ذخیره می‌کنیم
    REGISTERED_USERS[phone_number] = {
        "password_hash": new_password  # ✅ در پروژه واقعی باید هش‌شده باشد
    }

    del reset_password_tokens[otp_token]  # پاک‌کردن توکن پس از استفاده

    return jsonify({"message": "Password updated successfully"}), 200

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/auth/is-authenticated', methods=['GET'])
@jwt_required(optional=True)
def is_authenticated():
    identity = get_jwt_identity()
    return jsonify({"authenticated": bool(identity)})

# Convert Persian digits to Latin digits
def persian_to_int(persian_num_str):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    trans_table = str.maketrans("".join(persian_digits), "0123456789")
    return int(persian_num_str.translate(trans_table))

# Convert Persian day (date) string to Gregorian date (simple example)
def get_gregorian_date(day_persian_date):
    day = persian_to_int(day_persian_date)
    return datetime.date(2025, 5, day)  # example fixed month/year

# Parse start time from slot string like '۱۰:۰۰ - ۱۲:۰۰'
def get_start_time(slot_str):
    start_time_persian = slot_str.split(' - ')[0].strip()
    start_time_latin = start_time_persian.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
    hour, minute = map(int, start_time_latin.split(':'))
    return datetime.time(hour, minute)

@app.route('/wallet/addresses-with-timestamps')
def get_addresses_with_timestamps():
    method = request.args.get('method')

    dates = [
        {
            "id": 1,
            "day": "شنبه",
            "date": "۱۴",
            "slots": ['۱۰:۰۰ - ۱۲:۰۰', '۱۲:۰۰ - ۱۴:۰۰', '۱۴:۰۰ - ۱۶:۰۰', '۱۶:۰۰ - ۱۸:۰۰', '۱۸:۰۰ - ۲۰:۰۰'],
        },
        {
            "id": 2,
            "day": "یکشنبه",
            "date": "۱۵",
            "slots": ['۱۰:۰۰ - ۱۲:۰۰', '۱۲:۰۰ - ۱۴:۰۰', '۱۴:۰۰ - ۱۶:۰۰', '۱۶:۰۰ - ۱۸:۰۰', '۱۸:۰۰ - ۲۰:۰۰'],
        },
        {
            "id": 3,
            "day": "دوشنبه",
            "date": "۱۶",
            "slots": ['۱۰:۰۰ - ۱۲:۰۰', '۱۲:۰۰ - ۱۴:۰۰', '۱۴:۰۰ - ۱۶:۰۰', '۱۶:۰۰ - ۱۸:۰۰', '۱۸:۰۰ - ۲۰:۰۰'],
        },
        {
            "id": 4,
            "day": "سه‌شنبه",
            "date": "۱۷",
            "slots": ['۱۰:۰۰ - ۱۲:۰۰', '۱۲:۰۰ - ۱۴:۰۰', '۱۴:۰۰ - ۱۶:۰۰', '۱۶:۰۰ - ۱۸:۰۰', '۱۸:۰۰ - ۲۰:۰۰'],
        }
    ]

    # Sample addresses in the format you gave:
    if method == 'inPerson':
        addresses = [
            {
                "id": 1,
                "address": "مشهد،بازار رضا،پلاک ۱۳",
                "title": "مشهد",
                "latitude": 35.744,
                "longitude": 51.375
            },
            {
                "id": 2,
                "address": "شعبه مرکزی صادقیه،خیابان محممدی،کوچه احدی،پلاک ۲",
                "title": "شعبه مرکزی",
                "latitude": 35.744,
                "longitude": 51.375
            },
            {
                "id": 3,
                "address": "تهران،پلاک ۱۳",
                "title": "تهران",
                "latitude": 35.744,
                "longitude": 51.375
            }
        ]
    elif method == 'byPost':
        addresses = [
            {
                "id": 4,
                "address": "تهران، صندوق پستی 4567",
                "title": "تهران",
                "latitude": 35.744,
                "longitude": 51.375
            },
            {
                "id": 5,
                "address": "اصفهان، صندوق پستی 8910",
                "title": "اصفهان",
                "latitude": 32.6546,
                "longitude": 51.6674
            }
        ]
    else:
        addresses = []

    # Add timestamp to each address based on first date and first slot:
    selected_date = dates[0]
    selected_slot = selected_date["slots"][0]
    gregorian_date = get_gregorian_date(selected_date["date"])
    start_time = get_start_time(selected_slot)
    dt = datetime.datetime.combine(gregorian_date, start_time)
    iso_timestamp = dt.isoformat() + 'Z'

    for addr in addresses:
        addr["timestamp"] = iso_timestamp

    return jsonify({
        "method": method,
        "addresses": addresses,
        "dates": dates
    })

# Optional: mapping Persian weekday to English/Gregorian name
weekday_mapping = {
    'شنبه': 'Saturday',
    'یکشنبه': 'Sunday',
    'دوشنبه': 'Monday',
    'سه‌شنبه': 'Tuesday',
    'چهارشنبه': 'Wednesday',
    'پنجشنبه': 'Thursday',
    'جمعه': 'Friday'
}

@app.route('/wallet/confirm-pickup', methods=['POST'])
def confirm_pickup():
    try:
        data = request.get_json()
        address_id = data.get("address_id")
        date = data.get("date")  # e.g., '۱۴'
        slot = data.get("slot")  # e.g., '۱۲:۰۰ - ۱۴:۰۰'

        if not all([address_id, date, slot]):
            return jsonify({"error": "Missing required fields"}), 400

        # Convert Persian date and time to numbers
        persian_digits = "۰۱۲۳۴۵۶۷۸۹"
        day = int(date.translate(str.maketrans(persian_digits, "0123456789")))

        start_time = slot.split(' - ')[0].strip()
        time_latin = start_time.translate(str.maketrans(persian_digits, "0123456789"))
        hour, minute = map(int, time_latin.split(':'))

        # Combine into datetime (May 2025 assumed)
        dt = datetime.datetime(2025, 5, day, hour, minute)

        # Fake Jalali conversion
        def gregorian_to_simple_jalali(date):
            jalali_year = 1404
            jalali_month = 2  # اردیبهشت
            return f"{jalali_year}/{str(jalali_month).zfill(2)}/{str(date.day).zfill(2)}"

        def weekday_to_persian(weekday_index):
            weekdays = ['دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه', 'شنبه', 'یکشنبه']
            return weekdays[weekday_index % 7]

        jalali_date = gregorian_to_simple_jalali(dt)
        weekday_persian = weekday_to_persian(dt.weekday())

        return jsonify({
            "address_id": address_id,
            "date": jalali_date,
            "weekday": weekday_persian,
            "time": start_time,
            "message": f"روز {weekday_persian} {jalali_date} در ساعت {start_time} توسط شما انجام شد. لطفا در همان روز و ساعت در محل تحویل همراه با مدارک حضور داشته باشید."
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

# Deposit page 
wallet_deposits = []

@app.route('/wallet/deposit', methods=['POST'])
def deposit_amount():
    try:
        data = request.get_json()
        print("🔵 Raw POST data:", data)  # <== این مهمه

        raw_amount = data.get("amount")
        if not raw_amount:
            return jsonify({"error": "مقدار مبلغ الزامی است"}), 400

        amount = int(raw_amount)  # اگر رشته باشه ولی عددی نباشه اینجا خطا میده

        deposit_entry = {
            "id": len(wallet_deposits) + 1,
            "amount": amount,
            "timestamp": datetime.datetime.now().isoformat()
        }

        wallet_deposits.append(deposit_entry)

        return jsonify({
            "message": "واریز با موفقیت ثبت شد",
            "deposit": deposit_entry
        }), 201

    except Exception as e:
        print("❌ Server Error:", str(e))  # 👈 این مهمه برای دیدن خط واقعی
        return jsonify({"error": "خطای داخلی سرور", "details": str(e)}), 500


quick_amounts = [
    {"id": 1, "amount": 10000000},  # 10 میلیون
    {"id": 2, "amount": 5000000},   # 5 میلیون
    {"id": 3, "amount": 20000000},  # 20 میلیون
]

@app.route('/wallet/quick-amounts', methods=['GET'])
def get_quick_amounts():
    return jsonify({"quick_amounts": quick_amounts})


# Moblie  dashboard
@app.get("/dashboard/metals")
def get_metals():
    return jsonify(content=[
        {"title": "طلا", "price": 6750000, "change": -0.82},
        {"title": "نقره", "price": 1750000, "change": 1.32},
        {"title": "پلاتین", "price": 6950000, "change": 0.45},
        {"title": "دلار", "price": 5800000, "change": 0.75}
    ])

@app.get("/dashboard/orders")
def get_orders():
    return jsonify(content=[
        {
            "id": 1,
            "status": "در انتظار دریافت حضوری",
            "orderNumber": "۱۳۳۴۵۶۷۸",
            "title": "سکه پارسیان ۱ گرمی محمد",
            "karat": 750,
            "branch": "شعبه مرکزی",
            "date": "۱۳ خرداد",
            "time": "۱۲:۰۰",
            "image": "/images/orderCoin.png"
        },
        {
            "id": 2,
            "status": "تحویل داده شده",
            "orderNumber": "۱۳۳۴۵۶۷۹",
            "title": "شمش ۵ گرمی گلدیس",
            "karat": 750,
            "branch": "شعبه غرب",
            "date": "۱۲ خرداد",
            "time": "۱۶:۰۰",
            "image": "/images/orderCoin.png"
        }
    ])

@app.get("/dashboard/chart")
def get_chart():
    return jsonify(content={
        "timestamps": ["۰۹:۳۰", "۱۲:۳۰", "۱۵:۳۰", "۱۸:۳۰", "۲۱:۳۰", "۰۰:۳۰", "۰۳:۳۰"],
        "data": {
            "24h": {
                "gold": [7800000, 8200000, 8600000, 9100000, 9400000, 9800000, 10300000],
                "coin": [7200000, 7600000, 8100000, 8600000, 8900000, 9400000, 9900000],
                "silver": [5000000, 5400000, 5800000, 6200000, 6500000, 7000000, 7500000],
                "usd": [4500000, 4700000, 5000000, 5300000, 5600000, 5900000, 6200000]
            },
            "1w": {
                "gold": [7000000, 7200000, 7500000, 7800000, 8000000, 8300000, 8600000],
                "coin": [6500000, 6700000, 6900000, 7200000, 7400000, 7700000, 8000000],
                "silver": [4600000, 4700000, 4900000, 5100000, 5300000, 5500000, 5800000],
                "usd": [4200000, 4300000, 4400000, 4600000, 4700000, 4800000, 5000000]
            }
        },
        "profit_indicators": [
            {"label": "طلا", "value": "gold", "profit": -0.82},
            {"label": "سکه", "value": "coin", "profit": 2.51},
            {"label": "نقره", "value": "silver", "profit": 1.32},
            {"label": "دلار", "value": "usd", "profit": 0.75}
        ]
    })


@app.get("/dashboard/categories")
def get_categories():
    return jsonify(content=[
        {"title": "شمش طلا", "imageUrl": "/images/dashboardIgnots.svg"},
        {"title": "طلا خام", "imageUrl": "/images/dashboardGoldIgnots.svg"},
        {"title": "شمش نقره", "imageUrl": "/images/dashboardSilverIgnots.svg"},
        {"title": "سکه", "imageUrl": "/images/dashboardCoinIgnots.svg"}
    ])

@app.get("/dashboard/best-sellers")
def get_best_sellers():
    return jsonify(content=[
        {"id": 1, "title": "شمش ۱ گرمی گلدیس", "karat": 750, "price": 6811000, "image": "/images/productDashboardImg.png"},
        {"id": 2, "title": "شمش ۷ گرمی محمدی", "karat": 750, "price": 326501000, "image": "/images/productDashboardImg.png"},
        {"id": 3, "title": "شمش ۴ گرمی محمد", "karat": 750, "price": 24500000, "image": "/images/productDashboardImg.png"},
        {"id": 4, "title": "سکه ۱ گرمی پارسیان", "karat": 750, "price": 7000000, "image": "/images/productDashboardImg.png"}
    ])

@app.get("/dashboard/news")
def get_news():
    return jsonify(content=[
        {
            "id": 1,
            "title": "پیش‌بینی رئیس اتحادیه درباره آینده بتیبانتصثتنبثصتابصتثناتثیباتنبتدرزتثصزدتثدزثقخثقتتنقبتنیسابتنیسقیمت طلا؛ فرصت طلایی یا خطر پنهان؟",
            "image": "/images/newsPicDashboard.svg",
            "source": "خبرآنلاین",
            "time": "۱ ساعت پیش"
        },
        {
            "id": 2,
            "title": "بررسی روند افزایشی قیمت سکه در بازار امروز تهران",
            "image": "/images/newsPicDashboard.svg",
            "source": "اقتصادنیوز",
            "time": "۳ ساعت پیش"
        },
        {
            "id": 3,
            "title": "بازار نقره زیر ذره‌بین تحلیلگران؛ فرصت یا تهدید؟",
            "image": "/images/newsPicDashboard.svg",
            "source": "اقتصاد آنلاین",
            "time": "دیروز"
        }
    ])


# ذخیره موقت نوتیفیکیشن‌ها و وضعیت خوانده شدن آن‌ها
notifications_store = [
    {"id": 1, "title": "سفارش جدید", "message": "سفارش شما با موفقیت ثبت شد.", "timestamp": "۱ ساعت پیش", "isRead": False},
    {"id": 2, "title": "ارسال محصول", "message": "درخواست شما توسط گلدیس تایید شد لطفا در روز چهار شنبه به تاریخ ۱۴۰۴/۰۲/۱۸ در ساعت ۱۲:۰۰-۱۴:۰۰ در شعبه مشهد حضور داشته باشید.", "timestamp": "دیروز", "isRead": False},
    {"id": 3, "title": "تحویل موفق", "message": "محصول شما تحویل داده شد.", "timestamp": "۳ روز پیش", "isRead": False},
    {"id": 4, "title": "ارسال محصول", "message": "درخواست شما توسط گلدیس تایید شد لطفا در روز چهار شنبه به تاریخ ۱۴۰۴/۰۲/۱۸ در ساعت ۱۲:۰۰-۱۴:۰۰ در شعبه مشهد حضور داشته باشید.", "timestamp": "دیروز", "isRead": False},
    {"id": 5, "title": "ارسال محصول", "message": "درخواست شما توسط گلدیس تایید شد لطفا در روز چهار شنبه به تاریخ ۱۴۰۴/۰۲/۱۸ در ساعت ۱۲:۰۰-۱۴:۰۰ در شعبه مشهد حضور داشته باشید.", "timestamp": "دیروز", "isRead": False},



]

@app.route('/notifications', methods=['GET'])
@jwt_required(optional=True)
def get_notifications():
    return jsonify(notifications_store), 200

@app.route('/notifications/read', methods=['POST'])
@jwt_required(optional=True)
def mark_notifications_as_read():
    data = request.get_json()
    ids = data.get("ids", [])
    updated = 0
    for n in notifications_store:
        if n['id'] in ids:
            n['isRead'] = True
            updated += 1
    return jsonify({"updated": updated, "ids": ids}), 200

# transactions in profile page 
all_transactions = [
    {
        "id": 1,
        "title": "دریافت حضوری",
        "dialog_title": "دریافت شمش به صورت حضوری",
        "date": "۱۴۰۴/۰۱/۲۳",
        "time": "۱۳:۲۳:۵۰",
        "amount": 33557000,
        "status": 2,
        "details": [
            {"label": "زمان", "value": "۱۳:۲۳:۵۰ - یکشنبه ۲۳ فروردین ۱۴۰۴"},
            {"label": "شماره سفارش", "value": "۱۲۳۴۵۶۷۸۹"},
            {"label": "واریز به حساب", "value": "۱۲۳۴-۵۶۷۸-۱۲۳۴-۵۶۷۸"},
            {"label": "شماره پیگیری", "value": "۱۲۳۴۵۶۷۸۹"},
            {"label": "شماره مرجع", "value": "۱۲۳۴۵۶۷۸۹"}
        ]
    },
    {
        "id": 2,
        "title": "تبدیل ریال به طلا",
        "dialog_title": "برداشت از حساب ریالی",
        "date": "۱۴۰۴/۰۱/۲۳",
        "time": "۱۴:۲۵:۱۰",
        "amount": 45000000,
        "status":3,
        "details": [
            {"label": "زمان", "value": "۱۴:۲۵:۱۰ - یکشنبه ۲۳ فروردین ۱۴۰۴"},
            {"label": "شماره سفارش", "value": "۲۳۴۵۶۷۸۹۰"},
            {"label": "واریز به حساب", "value": "۹۸۷۶-۵۴۳۲-۱۰۹۸-۷۶۵۴"},
            {"label": "شماره پیگیری", "value": "۲۳۴۵۶۷۸۹۰"},
            {"label": "شماره مرجع", "value": "۲۳۴۵۶۷۸۹۰"}
        ]
    },
    {
        "id": 3,
        "title": "خرید نقره",
        "date": "۱۴۰۴/۰۱/۲۳",
        "time": "۱۵:۳۰:۰۰",
        "amount": 27500000,
        "status": 1,
        "details": [
            {"label": "زمان", "value": "۱۵:۳۰:۰۰ - یکشنبه ۲۳ فروردین ۱۴۰۴"},
            {"label": "شماره سفارش", "value": "۳۴۵۶۷۸۹۰۱"},
            {"label": "واریز به حساب", "value": "۸۷۶۵-۴۳۲۱-۹۸۷۶-۵۴۳۲"},
            {"label": "شماره پیگیری", "value": "۳۴۵۶۷۸۹۰۱"},
            {"label": "شماره مرجع", "value": "۳۴۵۶۷۸۹۰۱"}
        ]
    }
]


@app.route('/profile/transactions', methods=['GET'])
def get_transactions():
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')

    filtered = all_transactions

    if category and category != 'all':
        filtered = [tx for tx in filtered if category in tx['title']]

    if search:
        filtered = [tx for tx in filtered if search in tx['title'] or search in str(tx.get('description', ''))]

    grouped = {}
    for tx in filtered:
        grouped.setdefault(tx['date'], []).append(tx)

    return jsonify(grouped)


# sheba bank cards 
@app.route('/profile/sheba-cards', methods=['GET'])
def get_sheba_cards():
    return jsonify(sheba_cards)


sheba_cards = [
    {
        "id": 1,
        "bank_name": "بانک پاسارگاد",
        "iban": "IR850120010000000511914396",
        "icon_url": "/images/banks/pasargad.png",
        "is_default": True
    }
]
def detect_bank_from_iban(iban):
    bank_codes = {
        "011": ("بانک ملی", "/images/banks/melli.png"),
        "012": ("بانک ملت", "/images/banks/mellat.png"),
        "013": ("بانک رفاه", "/images/banks/refah.png"),
        "017": ("بانک ملی", "/images/banks/melli.png"),
        "018": ("بانک تجارت", "/images/banks/tejarat.png"),
        "019": ("بانک صادرات", "/images/banks/saderat.png"),
        "020": ("بانک کشاورزی", "/images/banks/keshavarzi.png"),
        "021": ("بانک مسکن", "/images/banks/maskan.png"),
        "022": ("بانک توسعه صادرات", "/images/banks/edbi.png"),
        "057": ("بانک پاسارگاد", "/images/banks/pasargad.png"),
        "078": ("بانک انصار", "/images/banks/ansar.png"),
        # ...
    }

    if len(iban) >= 10:
        bank_code = iban[4:7]  # IRXX 0** ***
        return bank_codes.get(bank_code, ("بانک نامشخص", "/images/banks/default.png"))
    return ("بانک نامشخص", "/images/banks/default.png")


@app.route('/profile/add-sheba', methods=['POST'])
def add_sheba_card():
    try:
        data = request.get_json()
        iban = data.get("iban")

        if not iban:
            return jsonify({"error": "شماره شبا الزامی است"}), 400

        # تشخیص بانک
        bank_name, icon_url = detect_bank_from_iban(iban)

        # بررسی تکراری نبودن
        if any(card["iban"] == iban for card in sheba_cards):
            return jsonify({"error": "این شماره شبا قبلاً ثبت شده است"}), 409

        new_card = {
            "id": len(sheba_cards) + 1,
            "bank_name": bank_name,
            "iban": iban,
            "icon_url": icon_url,
            "is_default": False
        }

        sheba_cards.append(new_card)
        return jsonify({"message": "شماره شبا با موفقیت افزوده شد", "card": new_card}), 201

    except Exception as e:
        print("⚠️ Error in add_sheba_card:", str(e))
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

# get profile info 
@app.route('/profile', methods=['GET'])
def get_profile():
    profile_data = {
        "fullName": "پریناز قاسمی پور",
        "mobile": "09352134347",
        "verified": True,
        "assets": 1298000000,
        "total_profit": 12980000
    }
    return jsonify(profile_data)

# profile edit 

editable_user_profile = {
    "full_name": "پریناز قاسمی پور",
    "national_id": "0481017985",
    "phone_number": "093521348347",
    "password": "********",
    "gender": "زن",
    "referral_source": "",
    "email": ""
}

@app.route('/profile/edit', methods=['GET'])
def get_editable_profile():
    return jsonify(editable_user_profile)


@app.route('/profile/edit', methods=['PUT'])
def update_profile():
    data = request.json
    for key in editable_user_profile:
        if key in data:
            editable_user_profile[key] = data[key]
    return jsonify({
        "message": "پروفایل با موفقیت به‌روزرسانی شد",
        "status": "success"
    }), 200

@app.route('/profile/invite', methods=['GET'])
def get_invite_info():
    return jsonify({
        "invite_code": "MWRF23",
        "invitees": [
            {"id": 1, "name": "پریناز قاسمی پور", "date": "۱۴۰۴/۰۱/۲۴"},
            {"id": 2, "name": "نوید طباطبایی فر", "date": "۱۴۰۴/۰۱/۲۴"}
        ]
    })

# shop products 

@app.route('/shop/products', methods=['GET'])
def get_shop_productss():
    filter_type = request.args.get('filter')
    search = request.args.get('search', '').strip()

    products = [
        {"id": 1, "title": "شمش ۱ گرمی گلدیس", "image": "/images/productDashboardImg.png", "ayar": 750, "price": 6811000, "bestSelling": True},
        {"id": 2, "title": "شمش ۲ گرمی نقره", "image": "/images/productDashboardImg.png", "ayar": 500, "price": 3000000},
        {"id": 3, "title": "شمش ۳ گرمی", "image": "/images/productDashboardImg.png", "ayar": 750, "price": 10000000}
    ]

    # جستجو
    if search:
        products = [p for p in products if search in p['title']]

    # فیلتر
    if filter_type == 'cheapest':
        products.sort(key=lambda p: p['price'])
    elif filter_type == 'lower-karat':
        products = [p for p in products if p['ayar'] < 750]
    elif filter_type == 'most-popular':
        products = [p for p in products if p.get('bestSelling')]

    return jsonify({"products": products})

@app.route('/shop/product-details/<int:id>', methods=['GET'])
def get_shop_product_detail(id):
    # دیتا فیک (بعداً به دیتابیس وصل می‌شه)
    product = {
        "id": id,
        "title": "شمش محمد",
        "price": 24810000,
        "ayar": 750,
        "weight": "2 گرم",
        "images": ["/images/productDashboardImg.png", "/images/productDashboardImg.png"],
        "description": "شمش طلای محمدی، نماد اصالت، اعتماد و سرمایه‌گذاری هوشمندانه است.محمدی، نماد اصالت، اعتماد و سرمایه‌گذاری هوشمندانه است.محمدی، نماد اصالت، اعتماد و سرمایه‌گذاری هوشمندانه است. "
    }
    return jsonify(product)


######################################################################################################
##################################################################### Faeze frontend test ############
######################################################################################################

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)


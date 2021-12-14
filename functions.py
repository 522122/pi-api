from hashlib import sha256
from flask import jsonify
from config import SECRET
from datetime import datetime

def now():
    return int(datetime.utcnow().timestamp() * 1000)

def hash(string):
    return sha256(f"{string}{SECRET}".encode()).hexdigest()

def message(text, data=None):
    return jsonify({
        'message': text,
        'data': data
    })

def required_params(params, data):
  for param in params:
    if param not in data:
      return False
  return True
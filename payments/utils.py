from hashlib import sha256
import hmac

from core import settings


def verify_chapa_webhook(request):
    secret = settings.CHAPA_CONFIG['WEBHOOK_SECRET']
    signature = request.headers.get('Chapa-Signature')
    body = request.body.decode('utf-8')
    computed = hmac.new(secret.encode(), body.encode(), sha256).hexdigest()
    return hmac.compare_digest(computed, signature)
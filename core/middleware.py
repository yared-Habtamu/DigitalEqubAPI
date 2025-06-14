from django.http import HttpResponseForbidden
from core import settings


class PaymentSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Verify payment callback signatures
        if request.path.startswith('/api/v1/payments/callback/'):
            if not self._verify_chapa_signature(request):
                return HttpResponseForbidden('Invalid signature')
        return self.get_response(request)

    def _verify_chapa_signature(self, request):
        from hashlib import sha256
        import hmac
        secret = settings.CHAPA_CONFIG['WEBHOOK_SECRET']
        signature = request.headers.get('Chapa-Signature')
        body = request.body.decode('utf-8')
        computed = hmac.new(secret.encode(), body.encode(), sha256).hexdigest()
        return hmac.compare_digest(computed, signature)
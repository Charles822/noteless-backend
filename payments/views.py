from decouple import config
import stripe
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect 
from htfbi_backend import settings


stripe.api_key = config('STRIPE_API_SECRET_KEY')


# Package 1 
class StripeCheckoutViewPack1(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1QEjpjGOOnj1bmYlvEtsTtjb',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.dev.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}&product_id=prod_R5rTPmubeChRMz',
                cancel_url=settings.dev.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        
        except Exception as e:
            print(str(e))
            return Response( 
                {'error': f'Something went wrong: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Package 2 
class StripeCheckoutViewPack2(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1QEjr9GOOnj1bmYlxcqdceez',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.dev.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}&product_id=prod_R6dDRuy9ZZcwCe', 
                cancel_url=settings.dev.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        
        except Exception as e:
            print(str(e))
            return Response( 
                {'error': f'Something went wrong: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StripeCheckoutViewPack3(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1QEjs7GOOnj1bmYllJsiRSRJ',
                        'quantity': 1,
                    },
                ],
                payment_method_types=['card',],
                mode='payment',
                success_url=settings.dev.SITE_URL + '?success=true&session_id={CHECKOUT_SESSION_ID}&product_id=prod_R6xnZCLfbtRFcg',
                cancel_url=settings.dev.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        
        except Exception as e:
            print(str(e))
            return Response( 
                {'error': f'Something went wrong: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    
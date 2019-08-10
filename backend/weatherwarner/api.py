import logging

import phonenumbers
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from .clients.twilio import send_text
from .models import Recipient
from .serializers import RecipientSerializer, VerificationCodeSerializer

log = logging.getLogger(__name__)


@ensure_csrf_cookie
def app(request, **kwargs):
    """
    View to render the react app.
    """
    return render(request, "app.html")


class VerificationViewSet(viewsets.ViewSet):
    throttle_classes = [AnonRateThrottle]

    @action(detail=False, methods=["post"])
    def request(self, request):
        """
        Validate Recipient Information, and send a verification code
        """

        data = request.data.copy()

        if "phone_number" in data:
            try:
                data["phone_number"] = phonenumbers.parse(data["phone_number"], "AU")
            except Exception:
                content = {
                    "phone_number": ["Invalid Phone Number. Please try another. e.g. 0421 900 800"]
                }
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = RecipientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
        else:
            content = serializer.errors
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        message = f"Your 6 digit verification code is {serializer.instance.verification_code}"

        # Send a verification code and link to the customer
        if send_text(phone_number=serializer.instance.phone_number.as_e164, message=message):
            content = {
                "message": "You have been sent a 6 digit verification code. Please enter it here."
            }
            request.session["phone_number"] = serializer.instance.phone_number.as_e164
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["post"])
    def validate(self, request):
        """
        Check the returned phone number matches the one associated with the user.
        """

        serializer = VerificationCodeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = request.session["phone_number"]
        verification_code = serializer.validated_data["verification_code"]

        try:
            recipient = Recipient.objects.get(
                verification_code=verification_code, phone_number=phone_number
            )
        except Recipient.DoesNotExist:
            content = {"verification_code": ["Invalid verification code. Please try again."]}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        recipient.verified = True
        recipient.save()

        return Response(status=status.HTTP_200_OK)

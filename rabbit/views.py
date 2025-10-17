from django.shortcuts import render
import requests
from datetime import datetime, timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import logging

# Create your views here.

# Configure logging
logger = logging.getLogger(__name__)

class MeView(APIView):
    """
    GET /me
    Returns profile info + dynamic cat fact in JSON format
    """

    def get(self, request):
        # ---Step 1: Get a random cat fact from the external API ---
        cat_fact_url = "https://catfact.ninja/fact"
        try:
            response = requests.get(cat_fact_url, timeout=5)
            response.raise_for_status()  # raises an error for non-200 responses
            cat_fact = response.json().get("fact", "Cats are awesome creatures!")
        except requests.exceptions.RequestException as e:
            logger.error(f"Cat Facts API error: {e}")
            cat_fact = "Could not fetch a cat fact at this time."

        # --- Step 2: Build user info ---
        user_data = {
            "email": "ugonjokubarthlomew@gmail.com",
            "name": "Chiebuka Ugo-Njoku",
            "stack": "Python/Django,Django RESTFUL API, HTML, CSS, JavaScript, BootStrap",
            "github": "https://github.com/tufatty",
        }

        # --- Step 3: Generate current UTC timestamp ---
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        # --- Step 4: Construct final response ---
        data = {
            "status": "success",
            "user": user_data,
            "timestamp": timestamp,
            "fact": cat_fact,
        }

        # --- Step 5: Return JSON response ---
        return Response(data, status=status.HTTP_200_OK, content_type="application/json")

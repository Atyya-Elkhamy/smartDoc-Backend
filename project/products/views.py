from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import Q
from langdetect import detect
from .models import Product
from .serializers import ProductSerializer

class ProductSearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get("q", "").strip()

        if not query:
            return Response({"error": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Auto-detect language using langdetect
        try:
            detected_lang = detect(query)
        except Exception:
            detected_lang = "en"  # fallback to English on error

        # Map language code to PostgreSQL language config
        lang_map = {
            "en": "english",
            "ar": "arabic",
            # Add more if needed
        }
        pg_lang = lang_map.get(detected_lang, "english")  # fallback to english if unsupported

        # Create full-text search vector and query
        vector = SearchVector("name", "description", config=pg_lang)
        search_query = SearchQuery(query, config=pg_lang)

        # Annotate rank and similarity
        products = Product.objects.annotate(
            rank=SearchRank(vector, search_query),
            similarity=TrigramSimilarity("name", query),
        ).filter(
            Q(rank__gte=0.1) | Q(similarity__gt=0.2)
        ).order_by("-rank", "-similarity")

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

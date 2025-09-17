from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection

@api_view(["GET"])
def medicines(request):
    page = int(request.GET.get("page", 1))
    size = int(request.GET.get("page_size", 20))
    offset = (page-1)*size
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM v_medicine_public ORDER BY published_at DESC, id DESC LIMIT %s OFFSET %s", [size, offset])
        rows = [dict(zip([c.name for c in cur.description], r)) for r in cur.fetchall()]
    return Response({"page": page, "items": rows})
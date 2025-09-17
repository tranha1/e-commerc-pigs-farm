from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import connection

@api_view(["GET"])
def medicines(request):
    default_page = 1
    default_size = 20

    try:
        page = int(request.GET.get("page", default_page))
    except (TypeError, ValueError):
        page = default_page

    try:
        size = int(request.GET.get("page_size", default_size))
    except (TypeError, ValueError):
        size = default_size

    if page < 1 or size < 1:
        return Response({"detail": "page and page_size must be positive integers."}, status=400)

    offset = (page - 1) * size
    with connection.cursor() as cur:
        cur.execute(
            "SELECT * FROM v_medicine_public ORDER BY published_at DESC, id DESC LIMIT %s OFFSET %s",
            [size, offset],
        )
        rows = [dict(zip([c.name for c in cur.description], r)) for r in cur.fetchall()]
    return Response({"page": page, "items": rows})

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from alumni.models import AlumniProfile
from django.db.models import Count, Q

class EmploymentStatsView(APIView):
    """
    Возвращает статистику трудоустройства:
      - общее количество выпускников по годам
      - количество трудоустроенных / безработных
      - % трудоустроенных
    Формат ответа:
    {
      "2021": {"total": 50, "employed": 35, "unemployed": 15, "percent_employed": 70.0},
      "2022": {"total": 60, "employed": 50, "unemployed": 10, "percent_employed": 83.33},
      ...
    }
    """
    permission_classes = (permissions.IsAuthenticated,)  # доступно для авторизованных (либо можно AllowAny)

    def get(self, request):
        # Группируем по graduation_year
        qs = AlumniProfile.objects.values("graduation_year").annotate(
            total=Count("id"),
            employed_count=Count("id", filter=Q(is_employed=True)),
            unemployed_count=Count("id", filter=Q(is_employed=False)),
        ).order_by("graduation_year")

        result = {}
        for entry in qs:
            year = entry["graduation_year"]
            total = entry["total"]
            employed = entry["employed_count"]
            unemployed = entry["unemployed_count"]
            percent = round(employed / total * 100, 2) if total else 0
            result[year] = {
                "total": total,
                "employed": employed,
                "unemployed": unemployed,
                "percent_employed": percent,
            }
        return Response(result)

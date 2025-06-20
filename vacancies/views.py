from rest_framework import viewsets, permissions
from .models import Vacancy
from .serializers import VacancySerializer

class IsVacancyOwnerOrReadOnly(permissions.BasePermission):
    """
    Только работодатель-владелец или ADMIN может редактировать / удалять вакансию.
    Остальным – только смотреть.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # ADMIN может всё
        if request.user.role == request.user.Roles.ADMIN:
            return True
        # владелец вакансии: obj.employer.user == request.user
        return obj.employer.user == request.user

class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all().select_related("employer")
    serializer_class = VacancySerializer

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [permissions.AllowAny()]  # вакансии могут просматривать даже незалогиненные
        return [permissions.IsAuthenticated(), IsVacancyOwnerOrReadOnly()]

    def perform_create(self, serializer):
        # находим профиль работодателя текущего пользователя
        employer = self.request.user.employer_profile
        serializer.save(employer=employer)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == user.Roles.EMPLOYER:
            # если работодатель, показываем только его вакансии (для CRUD)
            return Vacancy.objects.filter(employer__user=user)
        # для остальных отображаем только активные вакансии
        return Vacancy.objects.filter(is_active=True)

from django.utils import timezone
from django.http import JsonResponse

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated:
            user = request.user
            
            if user.is_banned:
                return JsonResponse({"message": "Banned"}, status=401)
            
            if user.is_suspended:
                if timezone.now().date() <= user.suspended_date:
                    return JsonResponse({"message": f"Suspended until {user.suspended_date}"}, status=401)
                else:
                    user.is_suspended = False
                    user.save()

        return response

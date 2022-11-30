from .models import Cart

def get_objects_count(request):
    if request.user.is_authenticated:
        cart_obj=Cart.objects.filter(user=request.user)
        total_objects=0
        if cart_obj.exists():
            for i in cart_obj:
                total_objects+=1
        return {"objects_count":total_objects}
    else:
        return {"objects_count":0}
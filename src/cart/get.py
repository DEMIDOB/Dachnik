from .models import Cart

def u_cart(request):
    uid = request.session._session_key
    print(request.session._session_key)

    thisCart = Cart.objects.filter(id=uid)
    
    if not len(thisCart) == 0:
        print("\nA user's {uid} cart has already existed\n")
        return thisCart[0]

    thisCart = Cart(id=uid)
    thisCart.save()
    
    print(f"\nCreated a new cart for user {uid}\n")

    return thisCart
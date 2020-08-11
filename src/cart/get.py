from .models import Cart

# def u_cart(request):
#     # TODO: if there is no _session_key, just return -1 and then check if -1 returned
#     uid = request.session._session_key
#
#     thisCart = Cart.objects.filter(id=uid)
#
#     if not len(thisCart) == 0:
#         print("\nA user's {uid} cart has already existed\n")
#         return thisCart[0]
#
#     thisCart = Cart(id=uid)
#     thisCart.save()
#
#     print(f"\nCreated a new cart for user {uid}\n")
#
#     return thisCart

def cartForUserWithID(id):
    try:
        thisCart = Cart.objects.get(id=id)
    except:
        thisCart = Cart(id=id)
        thisCart.save()

    return thisCart

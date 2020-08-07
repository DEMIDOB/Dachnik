import json
from django.http import HttpResponse

def myname_api(request):
    request.session['initialized'] = True
    name = request.session.get('name', "-1")
    print("XUIXUIXUXIXUIUXIUXU", name)
    exists = name != "-1"

    myContext = {
        "name": name,
        "exists": exists
    }

    response_str = json.dumps(myContext, ensure_ascii=False)
    response = HttpResponse(response_str)
    response["Access-Control-Allow-Origin"] = "*"

    return response
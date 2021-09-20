from datetime import datetime
from django.shortcuts import render


def all_rooms(request):
    now = datetime.now()
    hungry = True

    # all_room.html "now", "hungry" 에 값 넣어서 랜더링
    return render(request, "all_rooms.html", context={"now": now, "hungry": hungry})

from django.http import HttpResponseBadRequest
from django.shortcuts import render


def user_chat_response(request):
    if request.htmx:
        message_content = request.POST.get("message_content")
        message_id = request.POST.get("message_id")

        return render(
            request,
            "home/partials/_user_message.html",
            {
                "message_content": message_content,
                "message_id": message_id,
            },
        )
    return HttpResponseBadRequest()

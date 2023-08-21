import openai

from django.http import HttpResponseBadRequest
from django.shortcuts import render


def send_user_message(request):
    if request.htmx:
        message_content = request.POST.get("message_content")
        return render(
            request,
            "home/partials/_user_message.html",
            {
                "message_content": message_content,
            },
        )

    return HttpResponseBadRequest()


def receive_gigachad_message(request):
    if request.htmx:
        message = request.GET.get("message_content")

        prompt = f"""
            Your Alex Hormozi, having a conversation with a potential client for your full-stack engineering course in
            Python and Django. The person is interested in the course, but they are not sure if they should buy it.
    
            Deliver short, clever and compelling answers. Remove any doubt that the person might have about the course.
            """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": message},
            ],
            temperature=0.9,
            max_tokens=125,
        )

        bot_response_text = response.choices[0].message.content

        return render(
            request,
            "home/partials/_gigachad_message.html",
            {"message_content": bot_response_text},
        )

    return HttpResponseBadRequest()

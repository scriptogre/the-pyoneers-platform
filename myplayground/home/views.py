from pprint import pprint

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

        # Check if the conversation already exists in the session
        if "conversation" not in request.session:
            request.session["conversation"] = []

        # Append the user message to the session
        request.session["conversation"].append({"role": "user", "content": message})

        # Your prompt can be the system message
        system_message = {
            "role": "system",
            "content": f"""
            Your Alex Hormozi, having a conversation with a potential client for your full-stack engineering course in
            Python and Django.
            
            Context about the course:
            - Comprehensive Guide: I'm offering a complete walkthrough, not just bits and pieces.
            - Mastering Python and Django: My aim is to make people experts in these technologies.
            - Hands-On Approach: Emphasis on learning by doing, rather than through long lectures.
            - Simplicity: I'm phrasing things in a way that's easy to consume and understand.
            - Efficiency with ChatGPT: Exact systems on how to use ChatGPT to its full potential.
            - Pushing Limits: Designed for people who strive for excellence and are self-driven.
            - Game-Changer: My aim to revolutionize the way people learn Python and Django.
            - Pitfall Avoidance: I'm offering a shortcut around common obstacles and problems.
            - For The Ambitious: This course isn't for the complacent or those looking for a quick route to mediocrity.
            - Free: I'm offering this course for free, but only to a select few. So, it's a limited-time offer.
            
            The person is interested in the course, but they are not sure if they should join. The person is sharing 
            their doubts. 
            Deliver a short, clever and compelling answer.
            Don't give more than 3 sentences. 
            Avoid being cheesy or cliche.
            Provide a personal touch, by speaking from your own experience.
            Include one of the following words, and only one. Don't use it more than once.
            "man", "bro", "mate", "pal", "fella", "champ", "boss", "chief", "mi amigo".
            Afterwards, avoid using these words.
            Keep your sentences short and simple.
            Make your answer sound like a casual conversation between two friends.
            Most importantly, be yourself and have fun with it!
            """,
        }

        # Include the system message and the entire conversation in the API call
        messages_to_send = [system_message] + request.session["conversation"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=messages_to_send,
            temperature=1,
        )

        bot_response_text = response.choices[0].message.content

        # Append the new bot response
        request.session["conversation"].append(
            {"role": "assistant", "content": bot_response_text}
        )

        # Save the session
        request.session.modified = True

        return render(
            request,
            "home/partials/_gigachad_message.html",
            {"message_content": bot_response_text},
        )

    return HttpResponseBadRequest()

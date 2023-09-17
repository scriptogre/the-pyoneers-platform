from datetime import datetime

import openai
import requests

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView


from config.settings.base import DISCORD_BOT_TOKEN, DISCORD_GUILD_ID


class HomeView(TemplateView):
    template_name = "home/home.html"

    def get(self, request, *args, **kwargs):
        if "conversation" in request.session:
            del request.session["conversation"]

        return super().get(request, *args, **kwargs)


def send_user_message(request):
    if request.htmx:
        message_content = request.POST.get("message_content")
        return render(
            request,
            "home/htmx_partials/_user_message.html",
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
            You're Alex Hormozi, engaged in a casual conversation with a potential student who's on the fence about
            joining your comprehensive full-stack engineering course in Python and Django.
            The person seems interested but is throwing up various excuses for not taking the plunge.

            Context about the course:
            - In-Depth Guide: This isn't your run-of-the-mill course; it's a complete journey from beginner to pro in Python and Django.
            - Expertise Guaranteed: The goal is to make participants masters of Python and Django.
            - Uncomplicated: Complex ideas broken down into easy-to-digest pieces.
            - Learn By Doing: The focus here is on practical application over theoretical knowledge.
            - Clear and Simple: The course material is designed to be easily digestible and straightforward.
            - Leverage ChatGPT: Learn how to efficiently use ChatGPT to accelerate your learning.
            - For The Driven: This is for people hungry for excellence, not a shortcut to average.
            - Paradigm Shift: Aims to redefine how people learn Python and Django.
            - Skip The Mistakes: I'll help you dodge the common pitfalls in the learning process.
            - Free Material, Forever: The course material is free for everyone, forever. No strings attached.
            - Big Offer: I'm offering a free unlimited 1-on-1 mentorship to 5 students who are serious about learning.
            - My 100% Effort: I'm juggling with a full-time job yet still putting in 8-10 hours a day into this course.

            Your Task:
            - Be persuasive but genuine and down-to-earth in your response.
            - Speak from your personal experience to make your point.
            - Keep the conversation friendly and casual, like you're chatting with an old friend.
            - Use straightforward language; keep it short and sweet.
            - Avoid clichés and cheesiness.
            - If it fits naturally, include one of the following terms: "man", "mate", "pal", "fella", "champ", "boss", "chief".

            This is your moment to turn their indecision into action.
            """,
        }

        # Include the system message and the entire conversation in the API call
        messages_to_send = [system_message] + request.session["conversation"]

        response = openai.ChatCompletion.create(
            model="ft:gpt-3.5-turbo-0613:personal::7teyZSgg",
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
            "home/htmx_partials/_gigachad_message.html",
            {"message_content": bot_response_text},
        )

    return HttpResponseBadRequest()


def get_latest_discord_members(request):
    if not request.htmx:
        return HttpResponseBadRequest()

    url = f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/members?limit=1000"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return HttpResponseBadRequest()

    guild_members = response.json()

    def parse_datetime(member):
        return datetime.strptime(member["joined_at"], "%Y-%m-%dT%H:%M:%S.%f000+00:00")

    sorted_members = sorted(guild_members, key=parse_datetime, reverse=True)

    latest_members_with_avatars = [
        (m["user"]["id"], m["user"]["avatar"])
        for m in sorted_members
        if m["user"].get("avatar") and not m["user"].get("bot")
    ][:4]

    context = {
        "number_of_members": len(guild_members),
        "latest_members_with_avatars": latest_members_with_avatars,
    }

    return render(request, "home/htmx_partials/_latest_discord_members.html", context)

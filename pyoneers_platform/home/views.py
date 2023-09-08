from datetime import datetime

import openai
import requests

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import TemplateView


from config.settings.base import DISCORD_BOT_TOKEN, DISCORD_GUILD_ID


class HomeView(TemplateView):
    template_name = "home_page.html"

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
            You're Alex Hormozi, having a conversation with a potential client for your full-stack engineering course in
            Python and Django. The person is interested in the course, but they are not sure if they should join. 
            The person is sharing their excuses for not joining the course. 
            
            Context about the course:
            - Comprehensive Guide: I'm offering a complete walkthrough, not just bits and pieces.
            - Mastering Python and Django: My aim is to make people experts in these technologies.
            - Hands-On Approach: Emphasis on learning by doing, rather than through long lectures.
            - Simplicity: I'm phrasing things in a way that's easy to consume and understand.
            - Efficiency with ChatGPT: Exact systems on how to use ChatGPT to its full potential.
            - Pushing Limits: Designed for people who strive for excellence and are self-driven.
            - Game-Changer: My aim to revolutionize the way people learn Python and Django.
            - Pitfall Avoidance: I'm offering a shortcut around common obstacles and problems.
            - For The Ambitious: It isn't for the complacent or those looking for a quick route to mediocrity.
            - Free: I'm offering this for free, but only to a select few. So, it's a limited-time offer.
            
            Be clever and compelling with your answer.
            Keep the sentences short and simple.
            Avoid being cheesy or cliche.
            Provide a personal touch, by speaking from your own experience.
            Make your answer sound like a casual conversation between two friends.
            Include one of the following words, but only if it makes sense: "man", "mate", "pal", "fella", "champ", 
            "boss", "chief".
            """,
        }

        # Include the system message and the entire conversation in the API call
        messages_to_send = [system_message] + request.session["conversation"]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
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

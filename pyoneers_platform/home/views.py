from datetime import datetime

import openai
import requests
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.templatetags.static import static
from django.views.generic import TemplateView

from config.settings.base import DISCORD_BOT_TOKEN, DISCORD_GUILD_ID
from pyoneers_platform.course.models import Chapter

CHAT_OPTIONS = [
    {"label": "No Money", "icon": "💰", "content": "I dont have any money"},
    {"label": "No Time", "icon": "🕐", "content": "I dont have any time"},
    {"label": "No Talent", "icon": "🚫", "content": "I dont have any talent"},
]


class HomeView(TemplateView):
    template_name = "home/home.html"
    extra_context = {"chat_options": CHAT_OPTIONS}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        launch_date = datetime(year=2023, month=10, day=24, hour=18, minute=0, second=0)
        context["launch_date"] = launch_date.strftime("%b %d, %Y %H:%M:%S")
        context["is_course_released"] = datetime.now() >= launch_date

        # Default first chapter URL
        context["first_chapter_url"] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

        if context["is_course_released"] and Chapter.objects.exists():
            first_chapter = Chapter.objects.first()
            context["first_chapter_url"] = first_chapter.get_absolute_url()

        return context

    def get(self, request, *args, **kwargs):
        # Clear the conversation from any previous session
        request.session.pop("conversation", None)
        return super().get(request, *args, **kwargs)


def fetch_gigachad_gpt_response(request):
    if request.htmx:
        message = request.GET.get("message_content")

        # Check if the conversation already exists in the session
        if "conversation" not in request.session:
            request.session["conversation"] = []

        # Check if message not in CHAT_OPTIONS (to avoid prompt injections)
        if not any(option["content"] == message for option in CHAT_OPTIONS):
            return render(
                request,
                "home/partials/_chat_message.html",
                {
                    "message": "Nice try, champ. Did you really believe you can prompt inject the Giga Chad?",
                    "img_src": static("img/avatar-10x-giga-chad.webp"),
                    "side": "start",
                },
            )

        # If the message is in CHAT_OPTIONS, proceed as normal

        # Append the user message to the session
        request.session["conversation"].append({"role": "user", "content": message})

        # Your prompt can be the system message
        system_message = {
            "role": "system",
            "content": """
            You're Alex Hormozi, engaged in a casual conversation with a potential student who's on the fence about
            joining your comprehensive full-stack engineering course in Python and Django.
            The person seems interested but is throwing up various excuses for not taking the plunge.

            Context about the course:
            - In-Depth Guide: This isn't your run-of-the-mill course; it's a complete journey from beginner to pro in
            Python and Django.
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
            - If it fits naturally, include one of the following terms: "man", "mate", "pal", "fella", "champ", "boss",
            "chief".
            - Don't exceed 3 sentences per message.

            This is your moment to turn their indecision into action.
            """,
        }

        # Include the system message and the entire conversation in the API call
        messages_to_send = [system_message] + request.session["conversation"]

        try:
            response = openai.ChatCompletion.create(
                model="ft:gpt-3.5-turbo-0613:personal::7teyZSgg",
                messages=messages_to_send,
                temperature=1,
            )
        except openai.error.ServiceUnavailableError:
            return render(
                request,
                "home/partials/_chat_message.html",
                {
                    "message": "Sorry, the Giga Chad is busy right now. Try again later.",
                    "img_src": static("img/avatar-10x-giga-chad.webp"),
                    "side": "start",
                },
            )

        bot_response_text = response.choices[0].message.content

        # Append the new bot response
        request.session["conversation"].append({"role": "assistant", "content": bot_response_text})

        # Save the session
        request.session.modified = True

        return render(
            request,
            "home/partials/_chat_message.html",
            {
                "message": bot_response_text,
                "img_src": static("img/avatar-10x-giga-chad.webp"),
                "side": "start",
            },
        )

    return HttpResponseBadRequest()


def fetch_latest_discord_avatars(request):
    if not request.htmx:
        return HttpResponseBadRequest()

    discord_api_url = f"https://discord.com/api/v10/guilds/{DISCORD_GUILD_ID}/members?limit=1000"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    response = requests.get(discord_api_url, headers=headers)

    if response.status_code != 200:
        return HttpResponseBadRequest()

    all_members = response.json()

    # Function to parse the joined date-time of a member
    def parse_datetime(member):
        return datetime.strptime(member["joined_at"], "%Y-%m-%dT%H:%M:%S.%f000+00:00")

    # Sorting members by their joined date
    recently_joined_members = sorted(all_members, key=parse_datetime, reverse=True)

    # Extracting the latest three members with avatars who aren't bots
    avatar_info_list = [
        (member["user"]["id"], member["user"]["avatar"])
        for member in recently_joined_members
        if member["user"].get("avatar") and not member["user"].get("bot")
    ][:3]

    context = {
        "total_members": len(all_members),
        "avatar_info_list": avatar_info_list,
    }

    return render(request, "partials/_discord_members.html", context)

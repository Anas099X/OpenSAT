from fasthtml.common import *
from main import *
import requests  # ensure requests is imported
import markdown

# Route for listing all announcements as cards
@rt('/blogs')
def announcements_list(request, session):
    test = requests.get("https://api.github.com/repos/anas099x/opensat/discussions")
    data = test.json()

    def display():
        cards = []
        for i, blog in enumerate(data):
            cards.append(
                Div(
                    H2(blog['title'], cls="text-2xl font-bold"),
                    P(blog['body'][:100] + '...', cls="text-base"),
                    A("Read More", href=f"/blogs/{i}", cls="btn btn-primary mt-2"),
                    cls="p-4 border border-gray-300 rounded-lg shadow-md mb-4"
                )
            )
        return cards  # return list of cards

    navigation = mobile_menu if is_mobile(request) else Navbar()
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 z-50"),
            Div(*display(), cls="grid gap-4"),  # render cards in a grid
            data_theme="silk",
            cls="bg-base-200"
        )
    )

# New route to display full discussion details using list index
@rt('/blogs/{discussion}')
def announcement_detail(request, session, discussion:str):
    try:
        index = int(discussion)
    except ValueError:
        return ("Invalid discussion index", 400)

    test = requests.get("https://api.github.com/repos/anas099x/opensat/discussions")
    data = test.json()
    if index < 0 or index >= len(data):
        return ("Discussion not found", 404)
    discussion = data[index]

    navigation = mobile_menu if is_mobile(request) else Navbar()
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 z-50"),
            Div(
                H2(NotStr(markdown.markdown(discussion['title'])), cls="text-3xl font-bold mb-4"),
                P(NotStr(markdown.markdown(discussion['body'])), cls="text-base"),
                A("Back to Announcements", href="/blogs", cls="btn btn-secondary mt-4"),
                cls="p-6 border border-gray-300 rounded-lg shadow-md"
            ),
            data_theme="silk",
            cls="bg-base-200"
        )
    )

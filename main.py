from fasthtml.common import *
from services import *
from datetime import *
import asyncio
import random, json, time
from starlette.responses import StreamingResponse
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()


app = FastHTML(hdrs=Meta(name="google-site-verification" ,content="DRvUtrkp21eFen9JI4r7FREzHHMrCDzK96VBWWh52eE"))
rt = app.route

site_title = Title("OpenSAT - Free SAT Question Bank with Endless Possibilities"),

Defaults = (Meta(name="viewport", content="width=device-width"),
            Meta(property="og:title" ,content="OpenSAT: SAT Question Bank with Endless Possibilities"),
            Meta(property="og:description" ,content="OpenSAT, a free and open-source SAT question bank. Dive into a massive pool of SAT practice problems, constantly growing thanks to a dedicated community of contributors."),
            Meta(property="og:image" ,content="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true"),
            Meta(property="og:url" ,content="https://opensat.fun/"),
            Meta(property="og:type" ,content="website"),
            site_title,
            Link(rel="icon",href="public/graduation-cap-solid.svg", sizes="any", type="image/svg+xml"),
            Link(rel="stylesheet" ,href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"),
            Script('''
MathJax = {
  tex: {
    inlineMath: [['$', '$'],['$$', '$$'],['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]'],['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};
''')
,
            Script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),
            Script(src="https://unpkg.com/htmx.org@2.0.2"),
            Script(src="https://unpkg.com/htmx.org@1.9.12/dist/ext/ws.js"),
            Script(src="/_vercel/insights/script.js"),
            Link(href="https://cdn.jsdelivr.net/npm/daisyui@5",rel="stylesheet",type="text/css"),
            Link(href="https://cdn.jsdelivr.net/npm/daisyui@5.0.0/themes.css",rel="stylesheet",type="text/css"),
            Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
            Script(src="https://ss.mrmnd.com/banner.js"),
            Script(src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"),
            Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
                Title("OpenSAT"),
            Style(open('main.css').read())    
                )



def is_mobile(request):
    ua = request.headers.get("user-agent", "").lower()
    return any(x in ua for x in ["mobile", "android", "iphone", "ipad"])


def menu_button():
    """Render a proper menu card with navigation links using DaisyUI's drawer component."""

    # Define menu items
    menu_items = [
        ("ti ti-home", "Home", "/"),
        ("ti ti-highlight", "Practice", "/practice/explore"),
        ("ti ti-books", "Explore", "/explore"),
        ("ti ti-bookmarks", "Tutors", "/tutors"),
        ("ti ti-book-2", "Prep Books", "/books"),
        # Added Subscribe menu button
        ("ti ti-credit-card", "Subscribe", "/subscription"),
        ("ti ti-user-circle", "Profile", "/profile"),
    ]

    # Create menu buttons dynamically
    menu_buttons = [
        A(Div(cls=f"{icon} text-2xl"), label, href=link, cls="btn btn-warning btn-wide btn-rounded m-1")
        for icon, label, link in menu_items
    ]

    # Special buttons
    report_button = A(Div(cls="ti ti-exclamation-circle text-2xl"), "Issue Report",
                      href="https://tally.so/r/312ovO", cls="btn btn-error btn-wide btn-rounded m-1")
    github_button = A(Div(cls="ti ti-brand-github text-2xl"), "GitHub",
                      href="https://github.com/Anas099X/OpenSAT", cls="btn btn-info btn-wide btn-rounded m-1")
    


    # Drawer structure
    return Div(
        Div(
            # Drawer toggle checkbox (hidden)
            Input(id="menu-drawer", type="checkbox", cls="drawer-toggle"),

            # **Drawer Button (Opens Menu)**
            Div(
                Label("☰ Menu", cls="btn btn-warning btn-ghost btn-outline justify-end", **{"for": "menu-drawer"}),
                cls="drawer-content"
            ),

            # **Drawer Sidebar (Menu Items)**
            Div(
                Label(cls="drawer-overlay", **{"for": "menu-drawer"}),  # Click outside to close

                # **Menu Card**
                Div(
                    Div(
                        # **Menu Header**
                        Div(
                            H2("Navigation", cls="text-xl font-bold text-center p-2"),
                            cls="relative text-center"
                        ),
                        Hr(cls="my-2"),

                        # **Menu Items**
                        *menu_buttons,
                        Hr(cls="my-2"),

                        # **Footer Buttons (Report & GitHub)**
                        report_button,
                        github_button,

                        Label("Close", cls="btn btn-dash btn-error btn-wide m-6", **{"for": "menu-drawer"}),

                        cls="flex flex-col items-center"
                    ),
                    cls="bg-base-300 shadow-lg rounded-lg w-80 min-h-screen"
                ),
                cls="drawer-side"
            ),
            cls="drawer drawer-end justify-end"
        ),
        cls="navbar-end"
    )

mobile_menu = Div(
    A(
        I(cls="ti ti-home text-xl"),
        "Home",
        cls="dock-label mt-3 text-lg",href="/"
    ),
    A(
        I(cls="ti ti-books text-xl"),
        "Explore",
        cls="dock-label mt-3 text-lg",href="/explore"
    ),
    A(
        I(cls="ti ti-highlight text-xl"),
        "Practice",
        cls="dock-label mt-3 text-lg",href="/practice/explore"
    ),
    menu_button(),
    cls="dock bg-warning text-warning-content shadow-xl"
)

def Navbar():
    test = requests.get("https://api.github.com/repos/anas099x/opensat/discussions")
    data = test.json()
    return Div(
        # Left section remains unchanged
        Div(
            A(
                I(cls="ti ti-school text-warning-content text-4xl"),
                P("opensat", cls="puff text-xl text-warning-content"),
                cls="btn rounded-full btn-ghost normal-case text-lg",
                href="/"
            ),
            cls="navbar-start"
        ),
        # Center toast updated with bg-success and a close button
        Div(
            Div(
                Div(
                data[-1]['title'], 
                A("Open", cls="btn btn-xs btn-success",href=data[-1]['html_url']),
                Button("Close", cls="btn btn-xs btn-error", onclick="this.parentElement.style.display='none';"),
                cls="alert alert-info"),
                cls="toast flex items-center justify-between rounded"
            ),
            cls="navbar-center"
        ),
        # Right section remains unchanged
        menu_button(),
        cls="navbar bg-warning shadow-lg text-warning-content"
    )

graduation_icon = 'https://raw.githubusercontent.com/Anas099X/OpenSAT/28581a0e460f99f2ccb2e8a717e72baf3221a1b0/public/graduation-cap-solid.svg'
graduation_icon_white = 'https://raw.githubusercontent.com/Anas099X/OpenSAT/0fd7e3b980f71fe315b286fec9c87d1d53cc39ed/public/graduation-cap-solid-white.svg'


@rt("/")
def get(request, session):
    """Render the home page with fully responsive hero sections."""

    # Choose navigation bar based on device type
    navigation = mobile_menu if is_mobile(request) else Navbar()

    first_hero = Div(
        Div(
            Div(
                I(cls="ti ti-school text-9xl mb-3 text-warning-content"),
                H2(
                    "Question Bank with ",
                    P("Endless", cls=" puff"),
                    " Possibilities",
                    cls="text-4xl text-warning-content lg:text-5xl font-bold text-center mb-4"
                ),
                P(
                    "OpenSAT, a free and ",
                    A("open-source", href="https://github.com/Anas099X/OpenSAT", cls="text-blue-600 font-bold"),
                    " SAT question bank. Dive into a massive pool of SAT practice problems and tests, "
                    "constantly growing thanks to a dedicated community of contributors.",
                    cls="text-lg text-warning-content lg:text-xl text-center max-w-2xl mx-auto mb-4"
                ),
                cls="text-center"
            ),
            cls="hero-content text-center"
        ),
        cls="hero bg-warning min-h-screen mb-0 rounded-b-3xl"
    )

    second_hero = Div(
        Div(
            # Removed Img component
            Div(
                I(cls="ti ti-books text-9xl mb-6"),
                H1("Practice SAT with over 1000 Unique Questions!", cls="text-3xl md:text-4xl font-bold mb-3 text-center"),
                P(
                    "Get access to lots of Unique Custom SAT questions just like the real test. New questions are always being added—start learning now!",
                    cls="py-2 md:text-xl mb-3 text-center"
                ),
                cls="text-center px-4"
            ),
            A(
                Div(cls="ti ti-books text-xl"),
                "Explore",
                href="/explore",
                cls="btn btn-lg btn-rounded btn-warning mt-2"
            ),
            cls="hero-content flex flex-col items-center"
        ),
        cls="hero bg-base-200 min-h-screen mb-0 rounded-b-3xl"
    )

    third_hero = Div(
        Div(
            # Removed Img component
            Div(
                I(cls="ti ti-highlight text-9xl mb-6"),
                H1("Level Up with Practice Tests!", cls="text-3xl md:text-4xl font-bold mb-3 text-center"),
                P(
                    "Try full-length, uniquely made practice tests for free. Sharpen your skills, track your progress, and get fully prepared for test day!",
                    cls="py-2 md:text-xl mb-3 text-center"
                ),
                cls="text-center px-4"
            ),
            A(
                Div(cls="ti ti-highlight text-xl"),
                "Practice",
                href="/practice/explore",
                cls="btn btn-lg btn-rounded btn-warning mt-2"
            ),
            cls="hero-content flex flex-col items-center"
        ),
        cls="hero bg-base-200 min-h-screen mb-5 rounded-b-3xl"
    )

    fourth_hero = Div(
        Div(
            # Removed Img component
            Div(
                I(cls="ti ti-brand-open-source text-9xl mb-6"),
                H1("Open-Sourced!", cls="text-3xl md:text-4xl font-bold mb-3 text-center"),
                P(
                    "OpenSAT is open-source, allowing free access to SAT practice and community-driven improvements.",
                    cls="py-2 md:text-xl mb-3 text-center"
                ),
                cls="text-center px-4"
            ),
            A(
                Div(cls="ti ti-brand-github text-xl"),
                "Github",
                href="https://github.com/Anas099X/OpenSAT",
                cls="btn btn-lg btn-rounded btn-info mt-2"
            ),
            cls="hero-content flex flex-col items-center"
        ),
        cls="hero bg-base-200 min-h-screen mb-5 rounded-b-3xl"
    )

    # Footer remains unchanged
    footer = Footer(
        Aside(
            Span(cls="ti ti-school text-6xl"),
            Div("OpenSAT", cls="text-lg font-bold"),
            Div("Your go-to platform for SAT practice and preparation.", cls="font-bold"),
            Div("NOT AFFILIATED WITH OR ENDORSED BY COLLEGE BOARD.", cls="text-xs"),
            A("Privacy Policy",cls="text-info-content underline" ,href="/privacy"),
            cls="text-center"
        ),
        Nav(
            H6("Links", cls="footer-title"),
            Div(
                A(cls="ti ti-brand-github-filled text-2xl", href="https://github.com/Anas099X/OpenSAT"),
                A(cls="ti ti-brand-discord-filled text-2xl", href="https://discord.gg/nrXfMDvU"),
                A(cls="ti ti-brand-instagram-filled text-2xl", href="https://www.instagram.com/anas099x/"),
                cls="grid grid-flow-col gap-4"
            )
        ),
        cls="footer bg-base-300 p-10 rounded-t-3xl"
    )


    # Return page structure
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 z-50"),
            Main(
                first_hero,
                second_hero,
                third_hero,
                fourth_hero,),
            footer,
            data_theme="silk",
            cls="bg-base-200"
        )
    )


@rt('/privacy')
def privacy(request, session):
    # Choose navigation bar based on device type
    navigation = mobile_menu if is_mobile(request) else Navbar()
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 z-50"),
            Main(
                Div(
                    H1("Privacy Policy", cls="text-3xl font-bold mb-4"),
                    P(
                        "OpenSAT is an open-sourced project dedicated to providing free SAT practice resources. Our transparent approach means that our code and data practices are open for public review.",
                        cls="text-lg mb-4"
                    ),
                    P(
                        "We collect only the minimal user data required for site functionality and third-party integrations. Our open-source community continually scrutinizes our methods to ensure compliance with best privacy practices.",
                        cls="text-lg mb-4"
                    ),
                    P(
                        "By using our platform, you acknowledge and agree to our transparent practices, knowing that any improvements or issues are publicly addressed by contributors worldwide.",
                        cls="text-lg mb-4"
                    ),
                    P(
                        "If you have any questions or concerns, please contact us through the available support channels.",
                        cls="text-lg mb-4"
                    ),
                    cls="container mx-auto my-12 p-8 bg-white shadow-lg rounded-lg"
                ),
            ),
            data_theme="silk",
            cls="bg-base-200"
        )
    )


#import other routes and run server
from routes import account, explore, tutors, questions, practice, books, subscription
serve()
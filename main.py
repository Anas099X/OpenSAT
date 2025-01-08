from fasthtml.common import *
from services import *
from datetime import *
import asyncio
import random, json, time
from starlette.responses import StreamingResponse
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()


app = FastHTML(exts='ws')
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
            Link(href="https://cdn.jsdelivr.net/npm/daisyui@4.12.12/dist/full.min.css",rel="stylesheet",type="text/css"),
            Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
            Meta(name="5e561dd7ae7c1408af4aa0d65e34d2a23de4a0b2" ,content="5e561dd7ae7c1408af4aa0d65e34d2a23de4a0b2"),
            Meta(name="google-adsense-account" ,content="ca-pub-2090178937498462"),
            Meta(name="mnd-ver" ,content="abysxla5bnhhtfnlvwpq"),
            Script(src="https://ss.mrmnd.com/banner.js"),
            Script(src="https://cdn.tailwindcss.com"),
                Title("OpenSAT"),
            Style(open('main.css').read())    
                )




def menu_button(session):
    """Render the home page with Login/Profile management using DaisyUI drawer."""

    # Define menu items as links
    home_button = A(Div(cls="ti ti-home text-2xl"), "Home", href="/", cls="btn btn-wide btn-primary btn-rounded btn-outline rounded-lg m-1.5")
    practice_button = A(Div(cls="ti ti-highlight text-2xl"), "Practice", href="/practice/explore", cls="btn btn-primary btn-rounded btn-outline rounded-lg m-1.5")
    explore_button = A(Div(cls="ti ti-compass text-2xl"), "Explore", href="/explore", cls="btn btn-wide btn-primary btn-outline btn-rounded rounded-lg m-1.5")
    tutors_button = A(Div(cls="ti ti-bookmarks text-2xl"), "Tutors", href="/tutors", cls="btn btn-primary btn-outline btn-rounded rounded-lg m-1.5")
    report_button = A(Div(cls="ti ti-exclamation-circle text-2xl text-neutral"), "Issue Report", href="https://tally.so/r/312ovO", cls="btn btn-error btn-rounded rounded-lg m-1.5")
    github_button = A(Div(cls="ti ti-brand-github text-2xl"), "Github", href="https://github.com/Anas099X/OpenSAT", cls="btn bg-blue-700 btn-outline btn-rounded rounded-lg m-1.5")

    # Drawer structure
    return Div(
        Div(
            # Drawer input (toggle)
            Input(
                id="menu-drawer",
                type="checkbox",
                cls="drawer-toggle"
            ),
            # Drawer content
            Div(
                Label("Menu", cls="drawer-button btn btn-primary btn-outline btn-rounded", **{"for": "menu-drawer"}),  # Open drawer button
                cls="drawer-content"
            ),
            # Drawer sidebar (menu items)
            Div(
                Label(
                    cls="drawer-overlay",
                    **{"for": "menu-drawer"}  # Close drawer overlay
                ),
                Div(
                    Div(
                        Div("Navigation", cls="flex justify-center text-xl font-bold mb-4"),
                        home_button,
                        practice_button,
                        explore_button,
                        tutors_button,
                        cls="menu pink rounded-lg text-base-content mt-4 max-w-2xl"
                    ),
                    cls="p-4"
                ),
                cls="drawer-side"
            ),
            cls="drawer drawer-end navbar-end space-x-2"
        ),
        cls="navbar-end space-x-2"
    )


graduation_icon = 'https://raw.githubusercontent.com/Anas099X/OpenSAT/28581a0e460f99f2ccb2e8a717e72baf3221a1b0/public/graduation-cap-solid.svg'
graduation_icon_white = 'https://raw.githubusercontent.com/Anas099X/OpenSAT/0fd7e3b980f71fe315b286fec9c87d1d53cc39ed/public/graduation-cap-solid-white.svg'


@rt("/")
def get(session):
    """Render the home page with fully responsive hero sections."""
      # Fetch user data from session

    first_hero = Div(
     Div(
        Div(
            Img(src=graduation_icon_white,cls="avatar w-48 mb-3"),  # Adjusted spacing
                H2(
                    "Question Bank with ", 
                    P("Endless", cls="text-pink puff"), 
                    " Possibilities",
                    cls="text-4xl text-white lg:text-5xl font-bold text-center mb-4"  # Reduced bottom margin
                ),
                P(
                    "OpenSAT, a free and ",
                    A("open-source", href="https://github.com/Anas099X/OpenSAT", cls="text-info font-bold"),
                    " SAT question bank. Dive into a massive pool of SAT practice problems and tests, "
                    "constantly growing thanks to a dedicated community of contributors.",
                    cls="text-lg text-white lg:text-xl text-center max-w-2xl mx-auto mb-4"  # Reduced bottom margin
                ),
                cls="text-center"
        ),
        cls="hero-content text-center"
    ),
    cls="hero bg-black min-h-screen mb-0"
 )


    second_hero = Div(
        Div(
            Img(
                src="https://i.ibb.co/sq8ptWZ/Screenshot-from-2024-11-30-19-24-43.png",
                cls="max-w-full sm:max-w-sm md:max-w-lg rounded-lg shadow-xl glass mx-auto mb-4"  # Made image fully responsive
            ),
            Div(
                H1("Practice SAT with over 1000 Unique Questions!", cls="text-3xl md:text-4xl font-bold mb-3"),
                P(
                    "Get access to lots of Unique Custom SAT questions just like the real test. New questions are always being added—start learning now!",
                    cls="py-4 text-sm md:text-lg mb-3"
                ),
                A(
                    Div(cls="ti ti-compass text-xl"),
                    "Explore",
                    href="/explore",
                    cls="btn btn-rounded btn-primary btn-outline mt-2"
                ),
                cls="text-center md:text-left px-4"  # Added padding for smaller screens
            ),
            cls="hero-content flex-col lg:flex-row items-center"
        ),
        cls="hero rounded-3xl pink min-h-screen mb-0"
    )

    third_hero = Div(
        Div(
            Img(
                src="https://i.ibb.co/hyd1dDN/Screenshot-from-2024-11-30-21-55-31.png",
                cls="max-w-full sm:max-w-sm md:max-w-lg rounded-lg shadow-xl glass mx-auto mb-4"
            ),
            Div(
                H1("Level Up with Practice Tests!", cls="text-3xl md:text-4xl font-bold mb-3"),
                P(
                    "Try full-length, uniquely made practice tests for free. Sharpen your skills, track your progress, and get fully prepared for test day!",
                    cls="py-4 text-sm md:text-lg mb-3"
                ),
                A(
                    Div(cls="ti ti-highlight text-xl"),
                    "Practice",
                    href="/practice/explore",
                    cls="btn btn-rounded btn-primary btn-outline mt-2"
                ),
                cls="text-center md:text-left px-4"
            ),
            cls="hero-content flex-col lg:flex-row-reverse items-center"
        ),
        cls="hero bg-base-200 min-h-screen mb-0"
    )

    footer = Footer(
        Aside(
            Span(cls="ti ti-school text-6xl"),
            Div("OpenSAT", cls="text-lg font-bold"),
            Div("Your go-to platform for SAT practice and preparation.", cls="font-bold"),
            Div("NOT AFFILIATED WITH OR ENDORSED BY COLLEGE BOARD.", cls="text-xs"),
            cls="text-center"
        ),
        Nav(
            H6("Links", cls="footer-title"),
            Div(
                A(cls="ti ti-brand-github-filled text-2xl", href="https://github.com/Anas099X/OpenSAT"),
                A(cls="ti ti-brand-discord-filled text-2xl",href="https://discord.gg/7KNg9zHRUk"),
                A(cls="ti ti-brand-instagram-filled text-2xl",href="https://www.instagram.com/anas099x/"),
                cls="grid grid-flow-col gap-4"
            )
        ),
        cls="footer bg-base-200 text-base-content p-10"
    )

    return (
        site_title,
            Head(Defaults),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Img(src=graduation_icon,cls="avatar w-8"),
                                P("opensat", cls="puff text-xl"),
                                cls="btn rounded-full btn-ghost normal-case text-lg",
                                href="/"
                            ),
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar pink"
                    ),
                    cls="sticky top-0 bg-gray-800 z-50"
                ),
                Main(
                    first_hero,
                    second_hero,
                    third_hero
                ),
                footer,
                data_theme="lofi",
                cls=""
            )
        )




#import other routes and run server
from routes import explore, tutors, questions, practice
serve()
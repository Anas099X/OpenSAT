from fasthtml.common import *
from settings import *
from datetime import *
import asyncio
import random, json, time
from starlette.responses import StreamingResponse
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

#oauth
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = 'https://www.patreon.com/oauth2/authorize'
TOKEN_URL = 'https://www.patreon.com/api/oauth2/token'
IDENTITY_URL = 'https://www.patreon.com/api/oauth2/v2/identity'



def get_user_data(session):
    """Fetch user data and campaign ID from the Patreon API."""
    access_token = session.get('access_token')
    if not access_token:
        return None, None

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {
        'fields[user]': 'email,full_name,thumb_url',
        'fields[member]': 'patron_status,currently_entitled_amount_cents',
        'include': 'memberships.campaign'
    }

    try:
        response = requests.get(IDENTITY_URL, headers=headers, params=params)
        response.raise_for_status()
        user_data = response.json()
    except requests.RequestException:
        return None, None

    campaign_ids = []
    is_active_paid_member = False
    
    for item in user_data.get('included', []):
        if item['type'] == 'member':
            if 'campaign' in item.get('relationships', {}):
                campaign_id = item['relationships']['campaign']['data']['id']
                campaign_ids.append(campaign_id)
                
                # Combined check for target campaign membership and paid status
                if campaign_id == "7055998":
                    patron_status = item.get('attributes', {}).get('patron_status')
                    entitled_amount = item.get('attributes', {}).get('currently_entitled_amount_cents', 0)
                    is_active_paid_member = patron_status == 'active_patron' and entitled_amount > 0
        
        elif item['type'] == 'campaign':
            campaign_ids.append(item['id'])

    return user_data, is_active_paid_member

app = FastHTML(exts='ws')
rt = app.route

Defaults = (Meta(name="viewport", content="width=device-width"),
            Meta(property="og:title" ,content="OpenSAT: SAT Question Bank with Endless Possibilities"),
            Meta(property="og:description" ,content="OpenSAT, a free and open-source SAT question bank. Dive into a massive pool of SAT practice problems, constantly growing thanks to a dedicated community of contributors."),
            Meta(property="og:image" ,content="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true"),
            Meta(property="og:url" ,content="https://opensat.fun/"),
            Meta(property="og:type" ,content="website"),
            Title("OpenSAT - Free SAT Question Bank with Endless Possibilities"),
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


def mondiad_ad_card(top:str):
     """
     Returns a FastHTML component rendering a custom advertisement card.
     """
     return Div(
     Div(
        # Overlay content
        "Ads provided here",
        cls="absolute inset-0 flex items-center justify-center text-black font-bold",
        style="z-index: 10;",
        data_mndbanid="44750640-a162-4ff6-8dfd-0b26283ea347"
     ),
     cls="relative card bg-base-200 shadow-xl rounded-lg mx-auto",
     style=f"max-width: 80%; height: 25px; top:{top}; overflow: hidden; display: flex; align-items: center; justify-content: center;"
    )

def menu_button(session):
    """Render the home page with Login/Profile management."""
    user_data, _ = get_user_data(session)  # Fetch user data from session
    
    home_button = tutors_button =  A(Div(cls="ti ti-home text-2xl text-neutral"),"Home", href="/", cls="btn btn-primary m-1")
    practice_button = A(Div(cls="ti ti-highlight text-2xl text-neutral"),"Practice", href="/practice/explore", cls="btn btn-primary m-1")
    explore_button =  A(Div(cls="ti ti-compass text-2xl text-neutral"),"Explore", href="/explore", cls="btn btn-primary m-1")
    tutors_button =  A(Div(cls="ti ti-bookmarks text-2xl text-neutral"),"Tutors", href="/tutors", cls="btn btn-primary m-1")
    report_button = A(Div(cls="ti ti-exclamation-circle text-2xl text-neutral"),"Issue Report", href="https://tally.so/r/312ovO",cls="btn btn-error m-1")
    github_button =  A(Div(cls="ti ti-brand-github text-2xl text-neutral"),"Github", href="https://github.com/Anas099X/OpenSAT",cls="btn btn-ghost m-1")

    if user_data:
        # User is logged in; show profile and logout buttons
        profile_image = Img(src=user_data['data']['attributes']['thumb_url'])
        profile_button = A(Div(cls='ti ti-user-cog text-2xl text-neutral'),"Profile", href="/profile", cls="btn btn-primary m-1")
        logout_button = A("Logout", href="/logout", cls="btn rounded-full btn- btn-secondary m-1")

        

    else:
        # User is not logged in; show login button
        profile_button = A(Div(cls="ti ti-brand-patreon-filled text-2xl text-neutral"),"login", href="/login", cls="btn btn-primary m-1")

    return Div(
                            Div(
                             Div(
                                Div(cls="ti ti-category text-xl text-neutral"),"Menu",role="button",tabindex="0",cls="btn btn-ghost rounded"),
                                     Ul(home_button,explore_button,practice_button,tutors_button,report_button,
                            tabindex="0", cls="dropdown-content menu menu-sm bg-base-200 rounded-box z-[1] w-44 p-2 shadow")
                                    ,cls="dropdown dropdown-bottom dropdown-end"),
                            cls="navbar-end space-x-2"
                        )




@rt("/")
def get(session):
    """Render the home page with fully responsive hero sections."""
    user_data, _ = get_user_data(session)  # Fetch user data from session

    first_hero = Div(
     Div(
        Div(
            Span("🎓", cls="text-9xl block mx-auto mb-4"),  # Adjusted spacing
                H2(
                    "Question Bank with ", 
                    U("Endless", cls="text-primary"), 
                    " Possibilities",
                    cls="text-4xl lg:text-5xl font-bold text-center mb-4"  # Reduced bottom margin
                ),
                P(
                    "OpenSAT, a free and ",
                    A(U("open-source"), href="https://github.com/Anas099X/OpenSAT", cls="text-info font-bold"),
                    " SAT question bank. Dive into a massive pool of SAT practice problems and tests, "
                    "constantly growing thanks to a dedicated community of contributors.",
                    cls="text-lg lg:text-xl text-center max-w-2xl mx-auto mb-4"  # Reduced bottom margin
                ),
                cls="text-center"
        ),
        cls="hero-content text-center"
    ),
    cls="hero bg-ghost min-h-screen mb-0"
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
                    Div(cls="ti ti-compass text-xl text-neutral"),
                    "Explore",
                    href="/explore",
                    cls="btn btn-primary mt-2"
                ),
                cls="text-center md:text-left px-4"  # Added padding for smaller screens
            ),
            cls="hero-content flex-col lg:flex-row items-center"
        ),
        cls="hero bg-ghost min-h-screen mb-0"
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
                    Div(cls="ti ti-highlight text-xl text-neutral"),
                    "Practice",
                    href="/practice/explore",
                    cls="btn btn-primary mt-2"
                ),
                cls="text-center md:text-left px-4"
            ),
            cls="hero-content flex-col lg:flex-row-reverse items-center"
        ),
        cls="hero bg-ghost min-h-screen mb-0"
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
        cls="footer bg-base-300 text-base-content p-10"
    )

    return (
        Html(
            Head(Defaults),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Span("🎓", style="font-size:2rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-lg",
                                href="/"
                            ),
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar shadow-lg bg-ghost"
                    )
                ),
                Main(
                    first_hero,
                    second_hero,
                    third_hero
                ),
                footer,
                data_theme="retro",
                cls="bg-base-200"
            )
        )
    )


@rt("/logout")
def logout(session):
    """Logout the user by clearing the session."""
    del session['access_token']  # Remove the access token from the session
    return RedirectResponse('/')


@rt("/login")
def login():
    """Redirect to Patreon OAuth page."""
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'identity identity.memberships'
    }
    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return RedirectResponse(f"{AUTH_URL}?{query_string}")


@rt("/callback")
def callback(request, session):
    """Handle OAuth callback and store the access token."""
    code = request.query_params.get('code')
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI
    }
    token_response = requests.post(TOKEN_URL, data=data)

    if token_response.status_code != 200:
        return "Failed to get access token", 400

    access_token = token_response.json().get('access_token')
    session['access_token'] = access_token  # Store the access token in session
    return RedirectResponse('/')


@rt("/profile")
def get(session):
    """Render the home page with Login/Profile management."""
    user_data, check_membership = get_user_data(session)  # Fetch user data from session
    #if user not logged in, return to patreon
    if user_data is None:
     return RedirectResponse('/patreon')

    if user_data:
        # User is logged in; show profile and logout buttons
        name = H4(user_data['data']['attributes']['full_name'],cls="card-title text-2xl")

        logout_button = A("Logout", href="/logout", cls="btn btn-sm btn-secondary m-1")
        profile_image = Img(src=user_data['data']['attributes']['thumb_url'])

    else:
        # User is not logged in; show login button
        name = A("Profile", href="/profile", cls="btn rounded-full btn-sm btn-primary m-1")
        logout_button = Div()  # Empty div to maintain layout consistency
        profile_image = Img(src="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true")
    
    
    if check_membership:
        tier = "OpenSAT+"
    elif user_data.get('data', {}).get('attributes', {}).get('email') in os.getenv("SPECIAL_ACCESS", "").split(","):
        tier = "Special Access"       
    else:
        tier = "Free"


    return (
       Html(
            Head(Defaults),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar bg-base-90 shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                         Div(Div(profile_image,cls="w-20 rounded-full"),cls="avatar m-1"),
                       name,
                       Div(f"Tier: {tier}",cls="font-bold"),
                       logout_button,
                        cls="card card-body bg-base-100 shadow-xl mx-auto p-10 mt-10",
                        style="max-width:100vh;"
                    )
                )
            ), data_theme="retro"
        )
    )





@rt("/patreon")
def get(session):
    """Render the home page with Login/Profile management."""


    return (
        Html(
            Head(Defaults),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar bg-base-90 shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
            Div(
                H2(
                    "Become a Patreon to Access Exclusive Content", 
                    cls="text-2xl font-bold text-center"
                ),
                P(
                    "To access premium content and support the project, please subscribe to our Patreon membership for little price of 2.79$/month to access over 100+ of practice tests!",
                    cls="text-center text-gray-600 mt-4"
                ),
                Div(
                    A(
                        Img(src='public/brand-patreon.png',cls="w-8 rounded"),"Became a Patreon", 
                        href="https://www.patreon.com",  # Replace with actual Patreon link
                        cls="btn btn-primary w-full mb-2"
                    ),
                    A(
                        "Login", 
                        href="/login", 
                        cls="btn btn-secondary w-full"
                    ),
                    
                    cls="card-actions justify-center mt-6"
                ),
                cls="card-body"
            ),
            cls="card bg-base-100 shadow-xl w-full max-w-lg mx-auto mt-12"
        ),
        cls="container mx-auto py-12 px-4"
                )
            ), data_theme="retro"
        )
    )


@rt("/explore")
def get(request, session):

    # Get section and domain from query parameters, with defaults
    section = request.query_params.get("section", "english")  # Default section: English
    domain = request.query_params.get("domain", "any")  # Default domain: any

    def domain_lower(input):
        return str(input).lower()

    # Generate filter buttons dynamically
    def filter_switch():
        filters = {
            "english": [
                {"label": "Information and Ideas", "value": "information and ideas"},
                {"label": "Craft and Structure", "value": "craft and structure"},
                {"label": "Expression of Ideas", "value": "expression of ideas"},
                {"label": "Standard English Conventions", "value": "standard english conventions"}
            ],
            "math": [
                {"label": "Algebra", "value": "algebra"},
                {"label": "Advanced Math", "value": "advanced math"},
                {"label": "Problem-Solving and Data Analysis", "value": "problem-solving and data analysis"},
                {"label": "Geometry and Trigonometry", "value": "geometry and trigonometry"}
            ]
        }

        category_filters = filters.get(section.lower(), [])
        return [
            A(
                f["label"],
                href=f"?{urlencode({'section': section, 'domain': f['value']})}",
                cls=f"btn btn-secondary btn-sm {'btn-active' if domain == f['value'] else ''}"
            )
            for f in category_filters
        ]

    # Question card generation function
    def generate_question_cards():
        questions = question_objects(section)  # Fetch questions for the section
        return [
            A(
                Div(
                    Div(Div(cls="ti ti-books text-4xl text-neutral"), cls="text-3xl"),  # Icon
                    Div(f'Question #{i + 1}', cls="font-bold text-xl"),  # Question title
                    Div(x['domain'], cls="font-bold text-pink-400"),  # Domain badge
                    cls="card-body"
                ),
                cls="card bg-base-200 shadow-2xl w-96 mx-auto hover:bg-base-300 transition-all rounded-lg",
                href=f"/questions?{urlencode({'section': section, 'index': i})}"
            ) if domain.lower() == "any" or domain_lower(x['domain']) == domain.lower() else Div('', hidden=True)
            for i, x in enumerate(questions)
        ]

    # AdSense card
    def ads_card():
     return Div(
        Div(
            Span("Ad", cls="indicator-item badge badge-success"),  # Badge with "Ad"
            data_mndazid="54740ac2-34e1-4bcb-b575-b9e67b4d11e0",
            cls="indicator"  # Indicator class for styling
        ),
        cls="card bg-base-200 shadow-2xl w-96 h-20 mx-auto rounded-lg"
    )
    def responsive_ads_card():
     return Div(
        Div(
            Span("Ad", cls="indicator-item badge badge-success"),  # Ad indicator badge
            Div(
                Script(
                    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2090178937498462",
                    crossorigin="anonymous"
                ),
                Ins(
                    cls="adsbygoogle",
                    style="display:block",
                    data_ad_client="ca-pub-2090178937498462",
                    data_ad_slot="8188391527",
                    data_ad_format="auto",
                    data_full_width_responsive="true"
                ),
                Script('(adsbygoogle = window.adsbygoogle || []).push({});'),
                cls="card bg-base-200 mx-auto rounded-lg"
            ),
            cls="indicator"  # Indicator class for proper positioning
        ),
         cls="card bg-base-200 shadow-2xl w-96 mx-auto rounded-lg"
    )


    # Generate filter buttons
    filter_buttons = filter_switch()

    # Generate question cards
    question_cards = generate_question_cards()

    return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Span("🎓", style="font-size:2rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-lg",
                                href="/"
                            ),
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Filters section - centered and styled
                        Div(
                            H1(
                                Div(cls="ti ti-filter text-4xl text-neutral"), 
                                "Filters", 
                                cls="text-2xl font-bold mb-4"
                            ),
                            # Section Filters with Labels
                            Div(
                                Div("Section:", cls="text-sm text-gray-600 font-semibold mb-2"),  # Section Label
                                Div(
                                    A(
                                        Div(cls="ti ti-a-b-2 text-2xl text-neutral"), 
                                        "English",
                                        href=f"?{urlencode({'section': 'english', 'domain': 'any'})}",
                                        cls=f"btn btn-primary btn-sm {'btn-active' if section == 'english' else ''}"
                                    ),
                                    A(
                                        Div(cls="ti ti-math-symbols text-2xl text-neutral"), 
                                        "Math",
                                        href=f"?{urlencode({'section': 'math', 'domain': 'any'})}",
                                        cls=f"btn btn-primary btn-sm {'btn-active' if section == 'math' else ''}"
                                    ),
                                    cls="btn-group space-x-2"
                                ),
                                cls="mb-6"  # Adds spacing between section and domain filters
                            ),
                            # Domain Filters with Labels
                            Div(
                                Div("Domain:", cls="text-sm text-gray-600 font-semibold mb-2"),  # Domain Label
                                Div(
                                    *filter_buttons,  # Dynamically generated domain filter buttons
                                    cls="flex flex-wrap gap-2"
                                ),
                                cls="mb-4"
                            ),
                            cls="p-4 rounded-lg shadow-xl mx-auto bg-base-200", 
                            style="max-width:100vh; margin-bottom:4vh;"
                        ),
                        # Questions list section - responsive grid layout with 3 columns max
                        Div(
                            *question_cards,  # Generates all question cards
                            cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"  # Responsive grid
                        ),
                        cls="flex flex-col space-y-6"
                    ),
                    cls="container mx-auto py-8"
                )
            ), data_theme="retro", cls='bg-base-200'  # DaisyUI's retro theme
        )
    )


@rt('/questions')
def get(request, session):
    # Extract query parameters
    section = request.query_params.get("section", "english")  # Default section: English
    num = int(request.query_params.get("num", 0))  # Default question number: 0

    # Fetch the specified question object
    question_obj = question_objects(section)[num]

    # Button for copying the question's URL
    copy_question_btn = Button(
        Div(cls="ti ti-link text-3xl text-info"),
        cls="tooltip",
        data_tip="Click to copy",
        onclick="copyHref(this)",
        copy_href=f"opensat.fun/questions?section={section}&num={num}"
    )

    # Return the HTML response
    return (
        Html(
            Head(
                Defaults,
                Script('''function copyHref(button) {
      // Get the href from the button's data-href attribute
      var href = button.getAttribute("copy-href");

      // Create a temporary textarea to hold the href value
      var textArea = document.createElement('textarea');
      textArea.value = href;
      document.body.appendChild(textArea);

      // Select and copy the content of the textarea
      textArea.select();
      document.execCommand('copy');

      // Remove the temporary textarea
      document.body.removeChild(textArea);
    }''')
            ),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Span("🎓", style="font-size:2rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-lg",
                                href="/"
                            ),
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Card component for question display
                        Div(
                            Div(
                                H2(copy_question_btn, f"Question #N{num + 1}", cls="card-title text-2xl font-bold"),
                                P(question_obj['question'].get('paragraph', "").replace('null', ""), cls="text-base mt-4"),
                                B(question_obj['question']['question'], cls="text-lg"),
                                Div(
                                    Div(B("A. "), question_obj['question']['choices']['A'], cls="py-2"),
                                    Div(B("B. "), question_obj['question']['choices']['B'], cls="py-2"),
                                    Div(B("C. "), question_obj['question']['choices']['C'], cls="py-2"),
                                    Div(B("D. "), question_obj['question']['choices']['D'], cls="py-2"),
                                    cls="mt-4"
                                ),
                                Div(
                                    Input(type="checkbox"),
                                    Div("Click to reveal answer", cls="collapse-title flex items-center justify-center text-l font-bold"),
                                    Div(
                                        B(f"Correct Answer is: {question_obj['question']['correct_answer']}"),
                                        Br(),
                                        P(question_obj['question']['explanation']),
                                        cls="collapse-content"
                                    ),
                                    cls="collapse collapse-plus glass"
                                ),
                                cls="card-body"
                            ),
                            cls="card bg-base-200 shadow-lg mx-auto w-full max-w-2xl"
                        ),
                        cls="container mx-auto py-8 px-4"
                    )
                )
            ), data_theme="retro", cls="bg-base-200"
        )
    )


@rt("/tutors")
def get(session):
    firestore_docs = db.collection('users').stream()

    return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    Div(
                        Div(
                           A(
                                Span("🎓", style="font-size:2rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-lg",
                                href="/"
                            ),
                            cls="navbar"
                        ),
                        menu_button(session),
                        cls="navbar shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Tutor cards in grid format
                        *[Div(
                                Div(
                                    # Avatar (Image) and Card Body
                                    Div(
                                        H2(Div(Img(src=doc.to_dict()['banner'],cls="rounded-full"),cls="bg-neutral text-neutral-content w-12 rounded-full"),doc.to_dict()['username'], cls="card-title"),
                                        P(doc.to_dict()['description'], cls="text-sm text-gray-500"),
                                        P(f"Availability: {doc.to_dict()['availability']}", cls="text-sm text-gray-500"),
                                        P(f"Email: {doc.to_dict()['email']}", cls="text-sm text-gray-500"),
                                        P(f"Country: {doc.to_dict()['country']}", cls="text-sm text-gray-500"),
                                        cls="card-body"
                                    ),
                                    # Card Actions with Button
                                    Div(
                                        A(f"Contact: {doc.to_dict()['contact']}", href=f"mailto:{doc.to_dict()['email']}", cls="btn btn-primary"),
                                        cls="card-actions justify-end"
                                    ),
                                    cls="card bg-base-200 w-96 shadow-xl p-2"
                                ),
                                cls="max-w-sm mx-auto"
                            ) for doc in firestore_docs],
                        cls="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
                    ),
                    cls="container mx-auto py-6"
                )
            ), data_theme="retro",cls="bg-base-200"
        )
    )



@rt("/practice/explore")
def get(session):

    user_data, check_membership = get_user_data(session)

    unused_membership = '''
    #if user not logged in, return to patreon
    if user_data is None:
     return RedirectResponse('/patreon')

    #check membership or special access
    if check_membership:
        ""
    elif user_data.get('data', {}).get('attributes', {}).get('email') in os.getenv("SPECIAL_ACCESS", "").split(","):
        ""      
    else:
        return RedirectResponse('/patreon')
    '''    
    
    # reset tests
    if 'page' not in session or session['page'] is None:
        session['page'] = 0
    del session['page']    

    # Load modules from JSON file
    modules = question_objects('practice_test')


    return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Span("🎓", style="font-size:2rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-lg",
                                href="/"
                            ),
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Loop through modules and create a card for each one
                        *[
                            Div(
                                A(
                                    Div(Div(cls="ti ti-highlight text-4xl text-neutral"), cls="text-3xl"),  # Icon for each module
                                    H2(module['name'], cls="card-title text-xl font-bold mt-1"),  # Module name
                                    P("Practice Test", cls="text-primary font-bold"),
                                    cls="card bg-base-200 shadow-xl w-96 mx-auto hover:bg-base-300 transition-all rounded-lg p-8",
                                    href=f"/practice/{i}/module/1" 
                                )
                            )
                            for i, module in enumerate(modules)
                        ],
                        cls="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"  # Responsive grid layout
                    ),
                    cls="container mx-auto py-8"
                )
            ), data_theme="retro",cls="bg-base-200"
        )
    )


@rt("/practice/{practice_num}/module/{module_number}")
def get(session, practice_num: int, module_number: int):
    #del session['page']

    user_data, check_membership = get_user_data(session)


    # Load the current module and initialize session state
    module = f'module_{module_number}'
    
    if 'page' not in session or session['page'] is None:
        session['page'] = 0
    if module not in session or session[module] is None:
        session[module] = []

    # Load practice questions
    practice_en_questions = question_objects('practice_test')
    
    # Get the current question object
    question_obj = question_objects('english' if module_number < 3 else 'math')[practice_en_questions[practice_num][module][session['page']]]

    # Helper to retrieve answers from session
    def answers_session(count):
        for answer in session[module]:
            if str(count) in answer:
                return answer[str(count)]
            
    def module_title():
        if module == "module_1" or module == "module_2":
            return "Reading & Writing"
        if module == "module_3" or module == "module_4":
            return "Math"           

    # Button for navigating to the next page/module
    def module_switcher():
        #checking different states of module
        if session['page'] < len(practice_en_questions[practice_num][module]) - 1:
            return A("Next", hx_post=f'/switch_page/{practice_num}/{module_number}/{session["page"]+1}', hx_swap="innerHTML", hx_target='#practice_html', cls="btn btn-primary rounded-full")
        elif module == "module_2":
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/break', cls="btn btn-secondary rounded-full")
        elif module == "module_4":
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/check', cls="btn btn-secondary rounded-full")
        else:
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/module/{module_number + 1}', cls="btn btn-secondary rounded-full")

    # Timer time (optional)
    timer_time = 10

    # Function for radio options (answer selection)
    def practice_options(value: str):
        if answers_session(session['page']) == value:
            return Input(type="radio", name="answer", value=value, checked=True, cls="radio radio-primary")
        else:
            return Input(type="radio", name="answer", value=value, cls="radio radio-primary")

    return (
        Html(
            Head(Defaults),
            Body(
                Header(
                    Div(
                        Div(
                            Div(f"Module {module_number}: {module_title()}",cls="text-xl font-bold"),
                            cls="navbar"
                        ),
                        menu_button(session),
                        cls="navbar shadow bg-ghost"
                    )
                ),
                Main(
                  Div(
                      # Dropdown for page selection
                         
                 
                        # Question content inside a DaisyUI card
                        Div(
    
                            Div(
                                P(question_obj['question'].get('paragraph', "").replace('null',''), cls="text-base mb-4"),
                                B(question_obj['question']['question'], cls="text-lg font-bold"),
                                Form(
                                    Div(
                                        Label(
                                            practice_options('A'),
                                            Span("A. " + question_obj['question']['choices']['A'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        Br(),
                                        Label(
                                            practice_options('B'),
                                            Span("B. " + question_obj['question']['choices']['B'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        Br(),
                                        Label(
                                            practice_options('C'),
                                            Span("C. " + question_obj['question']['choices']['C'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        Br(),
                                        Label(
                                            practice_options('D'),
                                            Span("D. " + question_obj['question']['choices']['D'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        cls="mt-4"
                                    ),
                                    cls="form-control",
                                    hx_post=f"/page/{module}/{session['page']}",
                                    hx_trigger="change",
                                    hx_swap="none"
                                ),
                                cls="card-body"
                            ),
                            Div(
                                A("Back", hx_post=[f'/switch_page/{practice_num}/{module_number}/{session["page"]-1}' if session['page'] > 0 else None], hx_swap="innerHTML", hx_target='#practice_html', cls="btn rounded-full bg-base-300"),
                                Div(
        Div(f"Question {session['page'] + 1}", cls="btn btn-secondary m-1", tabindex="0", role="button"),
        Div(
            Div(
                H3(f"Select a Question", cls="card-title text-lg font-semibold mb-4"),
                Div(
                    # Grid layout for page buttons
                    *[
                        A(
                            f"{i + 1}", 
                            hx_post=f"/switch_page/{practice_num}/{module_number}/{i}",
                            hx_swap="innerHTML",
                            hx_target='#practice_html', 
                            cls="btn btn-outline btn-secondary w-12 h-10 m-1 text-lg font-semibold shadow"
                        ) 
                        for i, _ in enumerate(practice_en_questions[practice_num][module])
                    ],
                    cls=" gap-3 justify-items-center"  # Ensures buttons align properly
                ),
                cls="card-body"
            ),
            cls="dropdown-content card bg-base-200 z-[1] w-[300px] h-[480px] absolute left-1/2 top-12 transform -translate-x-1/2 z-10 shadow",
            tabindex="0"
        ),
        cls="dropdown dropdown-top dropdown-hover"
    ),
                                module_switcher(),
                                cls="flex justify-between items-center mt-6 p-5"
                            )
                            ,
                            cls="card bg-base-200 shadow-xl w-full max-w-3xl mx-auto mt-8"
                        ),
                        # Navigation: Back, Page Number, Next/Finish
                       
                    ),
                    cls="container mx-auto py-8 px-4"
                ),
                id="practice_html"
            ),
            data_theme="retro",cls="bg-base-200"  # Retro theme enabled
        )
    )


@rt('/switch_page/{practice}/{module_number}/{value}')
def post(session,practice:str,module_number:str,value:int):
 # Initialize module in the session if it doesn't exist or if it's None
    session.setdefault('page', 0)
    session['page'] = value
    return RedirectResponse(f'/practice/{practice}/module/{module_number}', status_code=303)



@rt("/practice/{practice_num}/break")
def get(practice_num:int):
    return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Main(
                    Div(
                        H2("Break Time!",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("click continue to start the next module",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("Continue", href=f"/practice/{practice_num}/module/3", cls="btn btn-primary"),
                            style="display:flex; justify-content:center;"
                            
                        ),
                        cls="card bg-base-200 w-96 shadow-xl mx-auto py-8"
                    )
                ),cls="flex items-center justify-center"
            ),data_theme="retro",cls="bg-base-200"
        )
    )

@rt("/practice/{practice_num}/check")
def get(practice_num: int, session):
    practice_en_questions = question_objects('practice_test')

    def checker():
        correct_answers = []
        results = []
        mistakes = []

        def answer_collecter(module_num):
            section = 'english' if module_num < 3 else 'math'
            for question_num in practice_en_questions[practice_num][f'module_{module_num}']:
                answer = question_objects(section)[question_num]['question']['correct_answer']
                correct_answers.append((answer, section, question_num))

        for num in [1, 2, 3, 4]:
            correct_answers.clear()
            user_answers = session[f'module_{num}']
            answer_collecter(num)

            for d in user_answers:
                index_str, user_answer = list(d.items())[0]
                index = int(index_str)

                if 0 <= index < len(correct_answers):
                    correct_answer, section, question_num = correct_answers[index]
                    if correct_answer == user_answer:
                        results.append(1)
                    else:
                        results.append(0)
                        mistakes.append((question_num, user_answer, correct_answer, section))
                else:
                    results.append(0)
                    mistakes.append((index + 1, user_answer, "Out of bounds", "N/A"))

            del session[f'module_{num}']
            session['page'] = 0
        return sum(results), mistakes

    # Calculate score and gather mistakes
    score, mistakes = checker()

    # HTML structure with score and mistakes table inside cards using DaisyUI classes
    return (
    Html(
        Head(
            Defaults
        ),
        Body(
            Main(
                # Card for score display
                Div(
                    H2("Your Score", style="font-size: 2.25rem; font-weight: 700; text-align: center; color: #333;"),
                    P(f"{score}/96", style="font-size: 1.5rem; text-align: center; color: #333; margin-top: 10px; font-weight: 600;"),
                    Br(),
                    Div(
                            A("Finish", href=f"/practice/{practice_num}/module/3", cls="btn btn-primary"),
                            style="display:flex; justify-content:center;"
                       ),

                    cls="card bg-base-200 w-96 shadow-xl mx-auto py-8 mb-6"
                ),
                
                # Card for mistakes table
                Div(
                    H2("Mistakes", style="font-size: 1.5rem; font-weight: 600; text-align: center; color: #333; margin-bottom: 20px;"),
                    Div(
                        Table(
                            Thead(
                                Tr(
                                    Th("Questions", cls="px-8 py-2"),
                                    Th("Your Answer", cls="px-8 py-2"),
                                    Th("Correct Answer", cls="px-8 py-2"),
                                    Th("Action", cls="px-8 py-2")
                                )
                            ),
                            Tbody(
                                *[
                                    Tr(
                                        Td(str(question_num), cls="border border-neutral px-8 py-2"),
                                        Td(user_answer, cls="border border-neutral px-8 py-2"),
                                        Td(correct_answer, cls="border border-neutral px-8 py-2"),
                                        Td(
                                            A("Go to question", href=f"/questions/{section}/{question_num}/True", cls="text-info underline"),
                                            cls="border border-neutral px-8 py-2"
                                        )
                                    )
                                    for question_num, user_answer, correct_answer, section in mistakes
                                ]
                            ),
                            cls="table w-full border-collapse border border-neutral"
                        ),
                        cls="overflow-x-auto px-4"  # Responsive container for table
                    ),
                    cls="card bg-base-100 shadow-xl mx-auto w-full max-w-3xl py-8"
                )
            ),
            cls="flex items-center justify-center min-h-screen"
        ),
        data_theme="retro",cls="bg-base-200"
    )
)
    
    


@rt('/page/{module}/{count}')
def post(session, count: int, module: str, answer: str):
 # Initialize module in the session if it doesn't exist or if it's None
    if module not in session or session[module] is None:
        session[module] = []
    practice_answers = session[module]

    # Ensure count is an integer, but we need it as a string to use as a key in the dictionary
    count_str = str(count)

    # Update or append the new item
    for item in practice_answers:
        if count_str in item:
            # If the count already exists, update the answer
            item[count_str] = answer
            break
    else:
        # If the count doesn't exist, append a new item
        practice_answers.append({count_str: answer})

    # Sort the practice_answers list by the integer value of the 'count' key in each dictionary
    practice_answers.sort(key=lambda item: int(list(item.keys())[0]))

    # Update the session with the modified and sorted practice_answers
    session[module] = practice_answers


    # Update the session
    session[module] = practice_answers



@rt("/time-sender/{time}")
async def get(session,time:int):
    # Total duration of the countdown (54 minutes)
    total_duration = timedelta(minutes=int(time))

    # Ensure the start time is in the session
    if 'start_time' not in session:
        session['start_time'] = datetime.now().isoformat()

    async def time_generator():
        while True:
            # Retrieve the start time from the session at the start of each iteration
            start_time = datetime.fromisoformat(session['start_time'])

            # Calculate the elapsed time
            elapsed_time = datetime.now() - start_time
            
            # Calculate the remaining time
            remaining_time = total_duration - elapsed_time
            
            if remaining_time.total_seconds() > 0:
                # Calculate minutes and seconds left
                minutes, seconds = divmod(remaining_time.total_seconds(), 60)
                time_str = f"{int(minutes):02d}:{int(seconds):02d}"
            else:
                # If time is up, reset the timer
                session['start_time'] = datetime.now().isoformat()
                start_time = datetime.fromisoformat(session['start_time'])
                time_str = "00:00"

            # Send the remaining time to all connected clients
            yield f"""event: TimeUpdateEvent\ndata: {to_xml(P(time_str, sse_swap="TimeUpdateEvent"))}\n\n"""

            # Use asyncio.sleep to keep the loop non-blocking
            await asyncio.sleep(1)

    try:
        # Start streaming the countdown timer
        return StreamingResponse(time_generator(), media_type="text/event-stream")
    except asyncio.CancelledError:
        # This block will be executed when the server is shutting down
        print("Timer stream was cancelled")

serve()
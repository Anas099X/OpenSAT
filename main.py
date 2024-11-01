from fasthtml.common import *
from settings import *
from datetime import *
import asyncio
import random, json, time
from starlette.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()

#oauth
CLIENT_ID = 'CTqlZU5Du7n2eA3yuZoRP3eOi9eqMrj89QmSZR9DuqMzVAd2cc90FC1DY_XtASv4'
CLIENT_SECRET = '7BF-vtstFA7HjCrziAAXrCu3WSU7g81Izfem6tiBCxRIhYi9QcJxJN-kRSsPZDUk'
REDIRECT_URI = 'http://0.0.0.0:5001/callback'

AUTH_URL = 'https://www.patreon.com/oauth2/authorize'
TOKEN_URL = 'https://www.patreon.com/api/oauth2/token'
IDENTITY_URL = 'https://www.patreon.com/api/oauth2/v2/identity'


def get_user_data(session):
    """Fetch user data and campaign ID from the Patreon API."""
    access_token = session.get('access_token')
    if not access_token:
        return None, None  # Return None for both user data and campaign ID if not logged in

    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'fields[user]': 'email,full_name,thumb_url', 'include': 'memberships.campaign'}

    try:
        response = requests.get(IDENTITY_URL, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        user_data = response.json()
    except requests.RequestException:
        return None, None  # Handle API failure gracefully

    # Extract campaign ID if available
    campaign_id = next(
        (item['relationships']['campaign']['data']['id']
         for item in user_data.get('included', [])
         if item['type'] == 'member' and 'campaign' in item.get('relationships', {})), 
        None
    )

    return user_data, campaign_id  # Return user data and campaign ID




app,rt = fast_app(debug=True,live=True)

Defaults = (Meta(name="viewport", content="width=device-width"),
            Meta(property="og:title" ,content="OpenSAT: Question Bank with Endless Possibilities"),
            Meta(property="og:description" ,content="OpenSAT, a free and open-source SAT question bank. Dive into a massive pool of SAT practice problems, constantly growing thanks to a dedicated community of contributors."),
            Meta(property="og:image" ,content="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true"),
            Meta(property="og:url" ,content="https://opensat.fun/"),
            Meta(property="og:type" ,content="website"),
            Title("OpenSAT"),
            Link(rel="icon",href="public/graduation-cap-solid.svg", sizes="any", type="image/svg+xml"),
            Link(rel="stylesheet" ,href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"),
            Script('''MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};'''),
            Script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),
            Script(src="https://unpkg.com/htmx.org@2.0.2"),
            Script(src="/_vercel/insights/script.js"),
            Link(href="https://cdn.jsdelivr.net/npm/daisyui@4.12.12/dist/full.min.css",rel="stylesheet",type="text/css"),
            Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
            Script(src="https://cdn.tailwindcss.com"),
                Title("OpenSAT"),
            Style(open('main.css').read())    
                
)


def menu_button(session):
    """Render the home page with Login/Profile management."""
    user_data, _ = get_user_data(session)  # Fetch user data from session
    
    home_button = tutors_button =  A(Div(cls="ti ti-home text-2xl text-neutral"),"Home", href="/", cls="btn rounded-full btn btn-primary m-1")
    practice_button = A(Div(cls="ti ti-highlight text-2xl text-neutral"),"Practice",Div(
                    Div(cls="ti ti-brand-patreon-filled w-3 h-3"),
                    cls="absolute -bottom-1 -right-1 bg-white rounded-full p-1 shadow"
                ), href="/practice/explore", cls="btn rounded-full relative btn btn-primary m-1")
    explore_button =  A(Div(cls="ti ti-compass text-2xl text-neutral"),"Explore", href="/explore/english/any", cls="btn rounded-full btn- btn-primary m-1")
    tutors_button =  A(Div(cls="ti ti-bookmarks text-2xl text-neutral"),"Tutors", href="/tutors", cls="btn rounded-full btn btn-primary m-1")
    github_button =  A(Div(cls="ti ti-brand-github text-2xl text-neutral"),"Github", href="https://github.com/Anas099X/OpenSAT", cls="btn rounded-full btn btn-secondary m-1")

    if user_data:
        # User is logged in; show profile and logout buttons
        profile_image = Img(src=user_data['data']['attributes']['thumb_url'])
        profile_button = A(Div(cls='ti ti-user-cog text-2xl text-neutral'),"Profile", href="/profile", cls="btn rounded-full btn btn-primary m-1")
        logout_button = A("Logout", href="/logout", cls="btn rounded-full btn- btn-secondary m-1")

        

    else:
        # User is not logged in; show login button
        profile_button = A(Div(cls="ti ti-brand-patreon-filled text-2xl text-neutral"),"login", href="/login", cls="btn rounded-full btn-sm btn-primary m-1")

    return Div(
                            Div(
                             Div(
                                Div(cls="ti ti-category text-2xl text-neutral"),"Menu",role="button",tabindex="0",cls="btn btn-primary rounded-full"),
                                     Ul(home_button,explore_button,practice_button,tutors_button,profile_button,github_button,
                            tabindex="0", cls="dropdown-content menu menu-lg bg-base-100 rounded-box z-[1] w-52 p-2 shadow")
                                    ,cls="dropdown dropdown-bottom dropdown-end"),
                            cls="navbar-end space-x-2"
                        )



def footer():
    """Reusable footer component for FastHTML routes."""
    return Footer(
        Div(
            Svg(
                Path(
                    d="M22.672 15.226l-2.432.811.841 2.515c.33 1.019-.209 2.127-1.23 2.456-1.15.325-2.148-.321-2.463-1.226l-.84-2.518-5.013 1.677.84 2.517c.391 1.203-.434 2.542-1.831 2.542-.88 0-1.601-.564-1.86-1.314l-.842-2.516-2.431.809c-1.135.328-2.145-.317-2.463-1.229-.329-1.018.211-2.127 1.231-2.456l2.432-.809-1.621-4.823-2.432.808c-1.355.384-2.558-.59-2.558-1.839 0-.817.509-1.582 1.327-1.846l2.433-.809-.842-2.515c-.33-1.02.211-2.129 1.232-2.458 1.02-.329 2.13.209 2.461 1.229l.842 2.515 5.011-1.677-.839-2.517c-.403-1.238.484-2.553 1.843-2.553.819 0 1.585.509 1.85 1.326l.841 2.517 2.431-.81c1.02-.33 2.131.211 2.461 1.229.332 1.018-.21 2.126-1.23 2.456l-2.433.809 1.622 4.823 2.433-.809c1.242-.401 2.557.484 2.557 1.838 0 .819-.51 1.583-1.328 1.847m-8.992-6.428l-5.01 1.675 1.619 4.828 5.011-1.674-1.62-4.829z",
                    fill_rule="evenodd", clip_rule="evenodd"
                ),
                width="50", height="50", viewBox="0 0 24 24", 
                xmlns="http://www.w3.org/2000/svg", cls="fill-current"
            ),
            P(
                "ACME Industries Ltd.",
                Br(),
                "Providing reliable tech since 1992"
            )
        ),
        Nav(
            H6("Services", cls="footer-title"),
            A("Branding", cls="link link-hover"),
            A("Design", cls="link link-hover"),
            A("Marketing", cls="link link-hover"),
            A("Advertisement", cls="link link-hover")
        ),
        Nav(
            H6("Company", cls="footer-title"),
            A("About us", cls="link link-hover"),
            A("Contact", cls="link link-hover"),
            A("Jobs", cls="link link-hover"),
            A("Press kit", cls="link link-hover")
        ),
        Nav(
            H6("Legal", cls="footer-title"),
            A("Terms of use", cls="link link-hover"),
            A("Privacy policy", cls="link link-hover"),
            A("Cookie policy", cls="link link-hover")
        ),
        cls="footer bg-ghost shadow-lg text-base-content p-10"
    )


@rt("/")
def get(session):
    """Render the home page with Login/Profile management."""
    user_data, _ = get_user_data(session)  # Fetch user data from session

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
                        Span("🎓", style="display: flex; font-size: 5rem; margin-bottom: 20px; justify-content: center;"),
                        H2("Question Bank with ", U("Endless", cls="text-primary"), 
                           " Possibilities",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("OpenSAT, a free and ",A(U("open-source"),href="https://github.com/Anas099X/OpenSAT",cls="text-secondary font-bold")," SAT question bank. "
                          "Dive into a massive pool of SAT practice problems, "
                          "constantly growing thanks to a dedicated community of contributors.",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A(Div(cls="ti ti-compass text-2xl text-neutral"),"Explore", href="/explore/english/any", cls="btn rounded-full btn-primary"),
                            A(Div(cls="ti ti-highlight text-2xl text-neutral"),"Practice",Div(
                            Div(cls="ti ti-brand-patreon-filled w-3 h-3"),
                            cls="absolute -bottom-1 -right-1 bg-white rounded-full p-1 shadow"
                        ), href="/practice/explore", cls="btn rounded-full relative btn btn-primary"),
                            style="display: flex; justify-content: center; gap: 15px;"
                        ),
                        cls="card bg-base-100 shadow-xl mx-auto p-10 mt-10",
                        style="max-width:100vh;"
                    )
                )
            ), data_theme="retro"
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
    user_data, camp_id = get_user_data(session)  # Fetch user data from session

    if user_data:
        # User is logged in; show profile and logout buttons
        name = H4(user_data['data']['attributes']['full_name'],cls="card-title text-2xl")
        email = user_data['data']['attributes']['email']
        logout_button = A("Logout", href="/logout", cls="btn btn-sm btn-secondary m-1")
        profile_image = Img(src=user_data['data']['attributes']['thumb_url'])

    else:
        # User is not logged in; show login button
        name = A("Profile", href="/profile", cls="btn rounded-full btn-sm btn-primary m-1")
        email = A("Profile", href="/profile", cls="btn rounded-full btn-sm btn-primary m-1")
        logout_button = Div()  # Empty div to maintain layout consistency
        profile_image = Img(src="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true")
    
    if camp_id != 7055998 and user_data['data']['attributes']['email'] not in os.getenv("SPECIAL_ACCESS", "").split(","):
        tier = "OpenSAT+"
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
                       Div(f"Email: {email}",cls="font-bold"),
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
    user_data, _ = get_user_data(session)  # Fetch user data from session

    if user_data:
        # User is logged in; show profile and logout buttons
        name = H3(user_data['data']['attributes']['full_name'],cls="card-title")
        email = user_data['data']['attributes']['email']
        logout_button = A("Logout", href="/logout", cls="btn btn-sm btn-secondary m-1")
        profile_image = Img(src=user_data['data']['attributes']['thumb_url'])

    else:
        # User is not logged in; show login button
        name = A("Profile", href="/profile", cls="btn rounded-full btn-sm btn-primary m-1")
        email = A("Profile", href="/profile", cls="btn rounded-full btn-sm btn-primary m-1")
        logout_button = Div()  # Empty div to maintain layout consistency
        profile_image = Img(src="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true")

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


@rt("/explore/{section}/{domain}")
def get(section: str, domain: str,session):

    def domain_lower(input):
        return str(input).lower()

    def filter_switch():
        if section == 'english':
            return (
                A("Information and Ideas", href=f'/explore/{section}/information and ideas', cls="btn btn-secondary btn-sm"),
                A("Craft and Structure", href=f'/explore/{section}/craft and structure', cls="btn btn-secondary btn-sm"),
                A("Expression of Ideas", href=f'/explore/{section}/expression of ideas', cls="btn btn-secondary btn-sm"),
                A("Standard English Conventions", href=f'/explore/{section}/standard english conventions', cls="btn btn-secondary btn-sm")
            )
        else:
            return (
                A("Algebra", href=f'/explore/{section}/algebra', cls="btn btn-secondary btn-sm"),
                A("Advanced Math", href=f'/explore/{section}/advanced math', cls="btn btn-secondary btn-sm"),
                A("Problem-Solving and Data Analysis", href=f'/explore/{section}/problem-solving and data analysis', cls="btn btn-secondary btn-sm"),
                A("Geometry and Trigonometry", href=f'/explore/{section}/geometry and trigonometry', cls="btn btn-secondary btn-sm")
            )

    # Question card generation function
    def generate_question_cards():
        return [
            A(
                Div(
                    Div(Div(cls="ti ti-books text-4xl text-neutral"), cls="text-3xl"),  # Icon
                    Div(f'Question #{i + 1}', cls="font-bold text-xl"),  # Question title
                    Div(x['domain'], cls="font-bold text-primary"),  # Domain badge
                    cls="card-body"
                ),
                cls="card bg-base-100 shadow-xl w-96 mx-auto hover:bg-base-200 transition-all rounded-lg",  # Fixed width and centered
                href=f"/questions/{section}/{i}/True"
            ) if domain.lower().replace('%20', ' ') == 'any' or domain_lower(x['domain']) == domain.lower().replace('%20', ' ') else Div('', hidden=True)
            for i, x in enumerate(question_objects(section))
        ]

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
                        # Filters section - centered and styled
                        Div(
                            H1(Div(cls="ti ti-filter text-4xl text-neutral"),"Filters", cls="text-2xl font-bold mb-4"),
                            Div(
                                A(Div(cls="ti ti-a-b-2 text-2xl text-neutral"),"English", href=f'/explore/english/any', cls=["btn btn-primary rounded-" if section == 'english' else "btn rounded"]),
                                A(Div(cls="ti ti-math-symbols text-2xl text-neutral"),"Math", href=f'/explore/math/any', cls=["btn btn-primary rounded" if section == 'math' else "btn rounded"]),
                                cls="btn-group space-x-2"
                            ),
                            Br(),
                            Div(filter_switch(), cls="flex flex-wrap gap-2 mt-4 justify-center"),  # Centered filter buttons
                            cls="p-4 rounded-lg shadow-xl mx-auto bg-base-100", style="max-width:100vh;"
                        ),
                        # Questions list section - responsive grid layout with 3 columns max
                        Div(
                            *generate_question_cards(),  # Generates all question cards
                            cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"  # Responsive grid with 1, 2, or 3 columns
                        ),
                        cls="flex flex-col space-y-6"
                    ),
                    cls="container mx-auto py-8"
                )
            ), data_theme="retro"  # DaisyUI's retro theme
        )
    )





@rt('/questions/{section}/{num}/{answer}')
def get(section: str, num: int, answer: bool, session):
    question_obj = question_objects(section)[num]

    def hide_switch(input):
        return not input

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
                        # Card component for question display
                        Div(
                            Div(
                                H2(f"Question #{question_obj['id']}", cls="card-title text-2xl font-bold"),
                                P(question_obj['question'].get('paragraph', ""), cls="text-base mt-4"),
                                B(question_obj['question']['question'], cls="text-lg"),
                                Div(
                                    Div(B("A. "), question_obj['question']['choices']['A'], cls="py-2"),
                                    Div(B("B. "), question_obj['question']['choices']['B'], cls="py-2"),
                                    Div(B("C. "), question_obj['question']['choices']['C'], cls="py-2"),
                                    Div(B("D. "), question_obj['question']['choices']['D'], cls="py-2"),
                                    cls="mt-4"
                                ),
                                Div(
                                    A("Reveal Answer", href=f'/questions/{section}/{num}/{hide_switch(answer)}', cls="btn btn-primary text-sm"),
                                    A("Go Back", href=f'/explore/{section}/any', cls="btn btn-secondary text-sm ml-4"),
                                    cls="flex mt-4 space-x-4"
                                ),
                                Div(
                                    Br(),
                                    B(f"Correct Answer is: {question_obj['question']['correct_answer']}"),
                                    P(question_obj['question']['explanation']),
                                    hidden=bool(answer),
                                    cls="mt-4"
                                ),
                                cls="card-body"
                            ),
                            cls="card bg-base-100 shadow-lg mx-auto w-full max-w-2xl"
                        ),
                        cls="container mx-auto py-8 px-4"
                    )
                )
            ), data_theme="retro"
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
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar"
                        ),
                        menu_button(session),
                        cls="navbar bg-base-90 shadow bg-ghost"
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
                                    cls="card bg-base-100 w-96 shadow-xl p-2"
                                ),
                                cls="max-w-sm mx-auto"
                            ) for doc in firestore_docs],
                        cls="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
                    ),
                    cls="container mx-auto py-6"
                )
            ), data_theme="retro"
        )
    )



@rt("/practice/explore")
def get(session):
    
    # reset tests
    if 'page' not in session or session['page'] is None:
        session['page'] = 0
    del session['page']    

    # Load modules from JSON file
    modules = question_objects('practice_test')

    #check if user is subbed to patreon
    user_data, camp_id = get_user_data(session)
    if user_data['data']['attributes']['email'] not in os.getenv("SPECIAL_ACCESS").split(","):
     return RedirectResponse('/patreon')
 
    

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
                        # Loop through modules and create a card for each one
                        *[
                            Div(
                                A(
                                    Div(Div(cls="ti ti-highlight text-4xl text-neutral"), cls="text-3xl"),  # Icon for each module
                                    H2(module['name'], cls="card-title text-xl font-bold mt-1"),  # Module name
                                    P("Practice Test", cls="text-primary font-bold"),
                                    cls="card bg-base-100 shadow-xl w-96 mx-auto hover:bg-base-200 transition-all rounded-lg p-8",
                                    href=f"/practice/{i}/module/1" 
                                )
                            )
                            for i, module in enumerate(modules)
                        ],
                        cls="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"  # Responsive grid layout
                    ),
                    cls="container mx-auto py-8"
                )
            ), data_theme="retro"
        )
    )


@rt("/practice/{practice_num}/module/{module_number}")
def get(session, practice_num: int, module_number: int):
    #del session['page']
    #check if user is subbed to patreon
    user_data, camp_id = get_user_data(session)
    if camp_id == 7055998:
     ""
    elif user_data['data']['attributes']['email'] in os.getenv("SPECIAL_ACCESS", "").split(","):
     ""          
    else:
     return RedirectResponse('/patreon')

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
                        cls="navbar bg-base-90 shadow bg-ghost"
                    )
                ),
                Main(
                  Div(
                      # Dropdown for page selection
                         
                 
                        # Question content inside a DaisyUI card
                        Div(
                            Div(
                                P(question_obj['question'].get('paragraph', ""), cls="text-base mb-4"),
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
                            cls="card bg-base-100 shadow-xl w-full max-w-3xl mx-auto mt-8"
                        ),
                        # Navigation: Back, Page Number, Next/Finish
                       
                    ),
                    cls="container mx-auto py-8 px-4"
                ),
                id="practice_html"
            ),
            data_theme="retro"  # Retro theme enabled
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
                        cls="card bg-base-100 w-96 shadow-xl mx-auto py-8"
                    )
                ),cls="flex items-center justify-center"
            ),data_theme="retro"
        )
    )


@rt("/practice/{practice_num}/check")
def get(practice_num:int,session):
 

 practice_en_questions = json.load(open('data.json'))['practice_test']

 
 def checker():
    correct_answers = []
    results = []
    def answer_collecter(module_num):
     for question_num in practice_en_questions[practice_num][f'module_{module_num}']:
      answer =  question_objects('english' if module_num < 3 else 'math')[question_num]['question']['correct_answer']
      correct_answers.append(answer)

    for num in [1,2,3,4]:
     correct_answers.clear()
     user_answers = session[f'module_{num}']
     answer_collecter(num)
     # Comparison result list
     # Loop through each dictionary in the list
     for d in user_answers:
     # Extract the number (as string) and the expected string
      index_str, expected_value = list(d.items())[0]
      index = int(index_str)  # Convert index to integer

     # Check if the index is within the bounds of the list_of_values
      if 0 <= index < len(correct_answers):
        # Compare the value in list_of_values at index with expected_value
        if correct_answers[index] == expected_value:
            results.append(1)
        else:
            results.append(0)
      else:
        # If index is out of bounds, consider it a mismatch
        results.append(0)
     del session[f'module_{num}']
     session['page'] = 0       
    return sum(results)

    

 return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Main(
                    Div(
                       
                        H2(f"Your Score is {checker()}/98",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("click continue to start the next module",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("End", href=f"/", cls="btn btn-primary"),
                            style="display:flex; justify-content:center;"
                            
                        ),
                        cls="card bg-base-100 w-96 shadow-xl mx-auto py-8"
                    )
                ),cls="flex items-center justify-center"
            ),data_theme="retro"
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
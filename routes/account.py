from main import *
from fasthtml.oauth import GoogleAppClient
from starlette.responses import RedirectResponse  # added import
from main import db  # add Firestore db instance import

# Load environment variables from .env file
load_dotenv()

# Auth client
client = GoogleAppClient(os.getenv("AUTH_CLIENT_ID"),
                         os.getenv("AUTH_CLIENT_SECRET"))

redirect_uri = "http://localhost:5001/redirect"


@rt('/login')
def login(request, session):
    # If already logged in, go to profile
    if session.get("user"):
        return RedirectResponse("/profile", status_code=303)
    # Render a proper login page
    login_link = client.login_link(redirect_uri)
    navigation = mobile_menu if is_mobile(request) else Navbar()

    return (
        Html(
            Head(Defaults),
            Header(navigation),
            Body(
                Div(
                    # Card container with organized layout and spacing
                    Div(
                        H1("Login", cls="text-3xl font-bold mb-4"),
                        A(Div(cls="ti ti-brand-google-filled text-2xl"),"Login with Google", href=login_link, cls="btn btn-warning btn-lg"),
                        cls="card bg-white p-8 shadow-lg rounded-lg text-center"
                    ),
                    cls="container mx-auto my-12 w-96"
                ),
                cls="bg-base-200"
            ),
            data_theme="silk"
        )
    )

@rt('/redirect')
def auth_redirect(request, code: str, session):
    info = client.retr_info(code, redirect_uri)
    # Filter out unwanted fields
    filtered_info = {
        "name": info.get("name"),
        "email": info.get("email"),
        "picture": info.get("picture"),
        "email_verified": info.get("email_verified")
    }
    user_email = filtered_info.get("email")
    if user_email:
        db.collection("users").document(user_email).set(filtered_info, merge=True)
    # Store filtered user info in session
    session["user"] = filtered_info
    return RedirectResponse("/profile", status_code=303)

@rt('/profile')
def profile(request, session):
    user = session.get("user")
    navigation = mobile_menu if is_mobile(request) else Navbar()
    if not user:
        return RedirectResponse("/login", status_code=303)
    
    # Determine membership tier and define extra content
    def tier():
        doc = db.collection('users').document(user.get("email", 'N/A')).get()
        if doc.exists and doc.to_dict().get('subscribed') == True:
            return "Premium"
        else:
            return "Free"
    
    membership = tier()
    premium_extra = ""
    if membership == "Premium":
        premium_extra = Div(
            Span("Premium Member", cls="badge badge-lg badge-accent"),
            H2("Welcome, valued Premium Member!", cls="text-2xl font-bold text-center text-white"),
            P("Enjoy exclusive features and benefits.", cls="text-md text-center text-white"),
            cls="mt-4 p-4 bg-gradient-to-r from-purple-500 via-pink-500 to-red-500 rounded-lg"
        )
    else:
        premium_extra = Div(
            P("Upgrade to Premium for exclusive features!", cls="text-md text-center mb-3"),
            A("Upgrade Now", href="/subscription", cls="btn btn-primary btn-block"),
            cls="mt-4 p-5 bg-warning rounded-lg"
        )
    
    return (
        Html(
            Head(Defaults),
            Header(navigation),
            Body(
                Div(
                    # Profile card with enhanced styling
                    Div(
                        Img(src=user.get("picture"), alt="Profile Picture", cls="rounded-full w-32 h-32 mx-auto mb-4 shadow-xl"),
                        H1(user.get("name", "N/A"), cls="text-3xl font-bold text-center mb-2"),
                        P(f"Email: {user.get('email', 'N/A')}", cls="text-md text-center mb-2"),
                        P(f"Membership: {membership}", cls="text-md text-center mb-4"),
                        premium_extra,
                        Div(
                            A("Logout", href="/logout", cls="btn btn-warning btn-block mt-6"),
                            cls="mt-4"
                        ),
                        cls="card bg-white p-8 shadow-lg rounded-lg max-w-md mx-auto"
                    ),
                    cls="container mx-auto my-12"
                ),
                cls="bg-base-200"
            ),
            data_theme="silk"
        )
    )

@rt('/logout')
def logout(session):
    session.pop("user", None)
    return RedirectResponse("/login", status_code=303)

serve()

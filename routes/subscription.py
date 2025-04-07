from main import *
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta  # Ensure timedelta is imported

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase Admin if not already initialized
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()

# PayPal API credentials (replace with real credentials)
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET")
PAYPAL_API_BASE = os.getenv("PAYPAL_API_BASE")  # Use live API for production
UNI_REDIRECT_URL  = os.getenv("UNI_REDIRECT_URL")



def get_paypal_token():
    """Retrieve OAuth token from PayPal."""
    auth = (PAYPAL_CLIENT_ID, PAYPAL_CLIENT_SECRET)
    response = requests.post(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        auth=auth
    )
    return response.json().get("access_token")

def check_subscription_expired(email: str):
    """Remove subscription details if subscription_date is older than 1 month."""
    doc_ref = db.collection("users").document(email)
    doc = doc_ref.get()
    if not doc.exists:
        return
    data = doc.to_dict()
    sub_date = data.get("subscription_date")
    if sub_date and isinstance(sub_date, datetime):
        # Convert sub_date to naive datetime by removing tzinfo
        naive_sub_date = sub_date.replace(tzinfo=None)
        if datetime.utcnow() - naive_sub_date > timedelta(days=30):
            doc_ref.update({
                "subscribed": firestore.DELETE_FIELD,
                "subscription_date": firestore.DELETE_FIELD
            })

def subscription_card():
    return Div(
        Div(
            Span("Most Popular", cls="badge badge-xs badge-warning mb-2 block text-center"),
            Div(
                H2("Premium", cls="text-3xl font-bold"),
                Span("$29/mo", cls="text-xl"),
                cls="flex justify-center items-center space-x-2"
            ),
            Ul(
                Li("- Full Access to OpenSAT 100+ Practice Tests", cls="flex items-center"),
                Li("- More features coming soon!", cls="flex items-center"),
                cls="mt-5 flex flex-col gap-2.5 text-sm text-center"
            ),
            Div(
                A("Subscribe", cls="btn btn-warning btn-block mt-6", href="/subscribe"),
                cls="flex justify-center"
            ),
            cls="card-body"
        ),
        cls="card w-96 shadow-lg bg-base-100 mx-auto transform transition hover:scale-105"
    )

def paypal_subscribe():
    return Div(
        Button(I(cls="ti ti-brand-paypal text-xl"),"Subscribe with PayPal", cls="btn btn-info w-full",
               hx_post="/subscription/create-order", hx_target="#subscription-response"),
        cls="mb-4"
    )

def creditcard_form():
    return Div(
        Form(
            # Fieldset for credit card details
            Fieldset(
                Legend("Credit Card Information", cls="legend text-xl font-bold mb-2"),
                Div(
                    Div(
                        Label("Card Number", cls="label"),
                        Input(name="card_number", placeholder="4111 1111 1111 1111", cls="input input-bordered w-full"),
                        cls="form-control mb-2"
                    ),
                    Div(
                        Label("Expiry", cls="label"),
                        Input(name="expiry", placeholder="12/26", cls="input input-bordered w-full"),
                        cls="form-control mb-2"
                    ),
                    Div(
                        Label("CVV", cls="label"),
                        Input(name="cvv", type="password", placeholder="123", cls="input input-bordered w-full"),
                        cls="form-control mb-2"
                    ),
                    Div(
                        Label("Cardholder Name", cls="label"),
                        Input(name="cardholder", placeholder="John Doe", cls="input input-bordered w-full"),
                        cls="form-control mb-2"
                    ),
                    Div(
                        Label("Billing Address", cls="label"),
                        Input(name="billing_address", placeholder="123 Main St", cls="input input-bordered w-full"),
                        cls="form-control mb-1"
                    ),
                    cls="space-y-3"
                ),
                cls=" p-4 rounded-lg"  # Optional styling for fieldset
            ),
            Button(I(cls="ti ti-credit-card text-xl"), "Subscribe with Credit Card", cls="btn btn-warning w-full",
                   hx_post="/subscription/create-credit-order", hx_target="#subscription-response"),
            id="credit-card-form",
            cls="space-y-4"
        ),
        cls="card bg-base-100 shadow-md p-6"
    )

@rt("/subscription")
def get(request, session):
    """Display subscription page with full HTML structure and organized forms."""
    # Check logged-in and subscribed status
    email = session.get("user", {}).get("email")
    doc = db.collection('users').document(email).get()

    #check if subscribed
    subscribed = False
    if email:
        doc = db.collection("users").document(email).get()
        subscribed = doc.exists and doc.to_dict().get("subscribed", False)

    if subscribed:
        return Redirect("/profile")    
        
    navigation = mobile_menu if is_mobile(request) else Navbar()

    return (
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 bg-gray-800 z-50"),
            Main(
                Div(
                    subscription_card(),
                    cls="container mx-auto py-8"
                )
            ),
            cls="bg-base-200",
            data_theme="silk"
        )
    )



@rt("/subscribe")
def get(request, session):
    """Display subscription page with full HTML structure and organized forms."""
    # Check logged-in and subscribed status
    email = session.get("user", {}).get("email")
    if not email:
        return Redirect("/profile")
    doc = db.collection('users').document(email).get()
    
    #check if subscribed
    subscribed = False
    if email:
        doc = db.collection("users").document(email).get()
        subscribed = doc.exists and doc.to_dict().get("subscribed", False)

    if subscribed:
        return Redirect("/profile")    
        
    navigation = mobile_menu if is_mobile(request) else Navbar()

    return (
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 bg-gray-800 z-50"),
            Main(
                Div(
                    Div(
                        H1("Subscribe", cls="text-3xl font-bold"),
                        P("Subscribe now to enjoy premium features!", cls="text-lg"),
                        cls="mb-6 text-center"
                    ),
                    Div(
                        creditcard_form(),
                        Div("Or", cls="text-center text-xl font-bold mb-2"),
                        paypal_subscribe(),
                        Div(id="subscription-response"),
                        cls="space-y-8 w-full md:w-1/3 mx-auto"
                    ),
                    cls="container mx-auto py-8"
                )
            ),
            cls="bg-base-200",
            data_theme="silk"
        )
    )

@rt("/subscription/create-order")
def post(request, session):
    """Create a PayPal order for subscription."""
    # Define subscription price and description.
    token = get_paypal_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {"currency_code": "USD", "value": "15.00"},
            "description": "OpenSAT Subscription"
        }],
        "application_context": {
            "return_url": f"{UNI_REDIRECT_URL}/subscribe/paypal-success",
            "cancel_url": f"{UNI_REDIRECT_URL}/subscribe/paypal-cancel"
        }
    }
    response = requests.post(f"{PAYPAL_API_BASE}/v2/checkout/orders", json=data, headers=headers)
    if response.status_code == 201:
        approval_url = next(link["href"] for link in response.json()["links"] if link["rel"] == "approve")
        return Script(f'window.location.href="{approval_url}"')
    return Titled("Error", Container(H1("❌ Subscription order creation failed!")))

@rt("/subscription/create-credit-order")
def post_credit(request, session, card_number: str, expiry: str, cvv: str, cardholder: str, billing_address: str):
    """Create a direct credit card payment for subscription and update Firestore."""
    if not session.get("user").get("email"):
        return Redirect("/profile")
    token = get_paypal_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {
        "intent": "CAPTURE",
        "payment_source.card": {
            "card": {
                "number": card_number,
                "expiry": expiry,
                "security_code": cvv,
                "name": cardholder,
                "billing_address": {
                    "address_line_1": billing_address,
                    "admin_area_2": "San Jose",
                    "admin_area_1": "CA",
                    "postal_code": "95131",
                    "country_code": "US"
                }
            }
        },
        "purchase_units": [{
            "amount": {"currency_code": "USD", "value": "15.00"},
            "description": "OpenSAT Subscription - Credit Card Payment"
        }],
        "application_context": {
            "return_url": f"{UNI_REDIRECT_URL}/subscribe/paypal-success",
            "cancel_url": f"{UNI_REDIRECT_URL}/subscribe/paypal-cancel"
        }
    }
    response = requests.post(f"{PAYPAL_API_BASE}/v2/checkout/orders", json=data, headers=headers)
    if response.status_code == 201:
        email = session.get("user").get("email")
        db.collection('users').document(email).update({
            "subscribed": True,
            "subscription_date": datetime.utcnow()
        })
        return Redirect("/subscribe/success")
    return Redirect("/subscribe/failed")


@rt("/subscribe/success")
def get(request, session):
    """Display payment success page."""
    # ...existing login and subscription check code...
    email = session.get("user", {}).get("email")
    if not email:
        return Titled("Error", Container(H1("Please log in to continue.")), A("Profile", cls="btn btn-primary", href="/profile"))
    
    subscribed = False
    if email:
        doc = db.collection("users").document(email).get()
        subscribed = doc.exists and doc.to_dict().get("subscribed", False)

    if subscribed:
        return Redirect("/profile")    
    
    navigation = mobile_menu if is_mobile(request) else Navbar()

    return (
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 bg-gray-800 z-50"),
            Main(
                Div(
                    Div(
                        H1("Payment Success!", cls="text-4xl font-bold text-center"),
                        P("Thank you for your payment. Your subscription has been activated. Enjoy premium features!", cls="text-xl text-center mt-4"),
                        A("Go to Dashboard", href="/profile", cls="btn btn-success mt-6 block mx-auto w-max"),
                        cls="bg-white w-96 p-6 rounded-lg shadow-md"
                    ),
                    cls="container mx-auto py-12 flex justify-center items-center min-h-screen"
                )
            ),
            cls="bg-base-200",
            data_theme="silk"
        )
    )


@rt("/subscribe/failed")
def get(request, session):
    """Display payment failure page."""
    email = session.get("user", {}).get("email")
    if not email:
        return Titled("Error", Container(H1("Please log in to continue.")), A("Profile", cls="btn btn-primary", href="/profile"))

    #check if subscribed
    subscribed = False
    if email:
        doc = db.collection("users").document(email).get()
        subscribed = doc.exists and doc.to_dict().get("subscribed", False)

    if subscribed:
        return Redirect("/profile")
            
    navigation = mobile_menu if is_mobile(request) else Navbar()

    return (
        Head(Defaults),
        Body(
            Header(navigation, cls="sticky top-0 bg-gray-800 z-50"),
            Main(
                Div(
                    Div(
                        H1("Payment Failed!", cls="text-4xl font-bold text-center text-error"),
                        P("Unfortunately, your transaction could not be processed. Please try again or contact support.", cls="text-xl text-center mt-4"),
                        A("Try Again", href="/subscribe", cls="btn btn-warning mt-6 block mx-auto w-max"),
                        cls="bg-white w-96 p-6 rounded-lg shadow-md"
                    ),
                    cls="container mx-auto py-12 flex justify-center items-center min-h-screen"
                )
            ),
            cls="bg-base-200",
            data_theme="silk"
        )
    )


@rt("/subscribe/paypal-success")
def get(request, session, token: str):
    """Capture the PayPal payment and store subscription data into Firestore."""
    if not session.get("user").get("email"):
        return Titled("Error", Container(H1("User not logged in.")))
    paypal_token = get_paypal_token()
    headers = {"Authorization": f"Bearer {paypal_token}", "Content-Type": "application/json"}
    capture_url = f"{PAYPAL_API_BASE}/v2/checkout/orders/{token}/capture"
    response = requests.post(capture_url, headers=headers)
    if response.status_code == 201:
        email = session.get("user").get("email")
        # Store subscription info on Firestore for the logged-in user.
        db.collection('users').document(email).update({
            "subscribed": True,
            "subscription_date": datetime.utcnow()
        })
        return Titled("Subscription Successful", Container(H1("✅ You have successfully subscribed!")))
    return Titled("Payment Failed", Container(H1("❌ Payment capture failed.")))

@rt("/subscribe/paypal-cancel")
def get(request, session):
    """Handle cancelled subscription payment."""
    return Titled("Subscription Cancelled", Container(H1("❌ Subscription process was cancelled.")))

serve()

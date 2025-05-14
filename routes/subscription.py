from main import *
import firebase_admin
from firebase_admin import credentials, firestore
import uuid
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
                Span("$3.99/mo", cls="text-xl"),
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

def subscription_buttons():
    return (
        Script(src=f"https://www.paypal.com/sdk/js?client-id={PAYPAL_CLIENT_ID}&components=buttons,funding-eligibility&enable-funding=card"),
        NotStr('''
<div id="paypal-button-container" class="-z-30"></div>
<script>
paypal.Buttons({
  style: {
    layout: 'vertical',
    color: 'gold',
    shape: 'rect',
    label: 'paypal'
  },
  createOrder: (data, actions) => {
    return actions.order.create({
      purchase_units: [{
        amount: {
          value: '3.99'
        }
      }]
    });
  },
  onApprove: (data, actions) => {
    return actions.order.capture().then(details => {
      // POST to your backend to mark subscription active
      fetch('/subscribe/api-confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          orderID: data.orderID,
          payerID: data.payerID
        })
      });
      window.location.href = "/subscribe/success";
    });
  }
}).render('#paypal-button-container');
</script>
'''))

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
                        #creditcard_form(),
                        #Div("Or", cls="text-center text-xl font-bold mb-2"),
                        subscription_buttons(),
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


@rt("/subscribe/api-confirm")
async def post(request, session):
    data = await request.json()
    """Handle PayPal payment success."""
    if not session.get("user").get("email"):
        return Titled("Error", Container(H1("User not logged in.")))
    paypal_token = get_paypal_token()
    headers = {"Authorization": f"Bearer {paypal_token}", "Content-Type": "application/json"}
    capture_url = f"{PAYPAL_API_BASE}/v2/checkout/orders/{data['orderID']}"
    response = requests.get(capture_url, headers=headers)
    print(response.text, response.status_code)
    if response.status_code == 200 or 201:
        email = session.get("user").get("email")
        # Store subscription info on Firestore for the logged-in user.
        db.collection('users').document(email).update({
            "subscribed": True,
            "subscription_date": datetime.utcnow()
        })
        return Titled("Subscription Successful", Container(H1("✅ You have successfully subscribed!")))
    return Titled("Payment Failed", Container(H1("❌ Payment capture failed.")))


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


serve()

from fasthtml.common import *
from main import *

@rt("/tutors")
def get(session):
    firestore_docs = db.collection('users').stream()

    return (
        Div(
            Head(
                Defaults
            ),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Img(src=graduation_icon, cls="avatar w-8"),
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
                    Div(
                        H1("Meet Your Tutors", cls="text-4xl font-extrabold text-center my-8 text-gray-700"),
                        P("Browse through a list of available tutors and find the perfect match for your learning needs.", 
                          cls="text-center text-gray-500 mb-8 text-lg"),
                        # Tutor cards in grid format
                        Div(
                            *[
                                Div(
                                    Div(
                                        # Card Header: Image and Name
                                        Div(
                                            Div(
                                                Img(src=doc.to_dict()['banner'], cls="w-20 h-20 rounded-full shadow-lg mx-auto"),
                                                cls="text-center"
                                            ),
                                            H3(doc.to_dict()['username'], cls="text-2xl font-bold text-gray-800 mt-4 text-center"),
                                            cls="mb-4"
                                        ),
                                        # Card Body: Description and Details
                                        Div(
                                            P(doc.to_dict()['description'], 
                                              cls="text-gray-600 text-center text-base mb-4"),
                                            Div(
                                                P(f"🕒 Availability: {doc.to_dict()['availability']}", 
                                                  cls="text-base text-gray-700 font-medium"),
                                                P(f"🌍 Country: {doc.to_dict()['country']}", 
                                                  cls="text-base text-gray-700 font-medium"),
                                                cls="mb-4 text-center"
                                            ),
                                            cls="flex-1"  # Ensures even height
                                        ),
                                        # Contact Button
                                        Div(
                                            A(
                                                "Contact Tutor", 
                                                href=f"mailto:{doc.to_dict()['email']}", 
                                                cls="btn btn-outline btn-primary w-full"
                                            ),
                                            cls="mt-4"
                                        ),
                                        cls="card bg-gray-50 shadow-md rounded-lg p-6 flex flex-col justify-between transition hover:bg-gray-100 hover:shadow-lg h-full"
                                    ),
                                    cls="w-full max-w-xs mx-auto"
                                ) for doc in firestore_docs
                            ],
                            cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 px-6"
                        ),
                        cls="container mx-auto py-8"
                    ),
                    cls="pink"
                ),
                cls="pink w-full"
            ),
            data_theme="lofi", cls="pink w-full"
        )
    )

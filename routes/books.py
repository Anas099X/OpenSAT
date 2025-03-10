from fasthtml.common import *
from main import *

@rt("/books")
def get(request, session):
    navigation = mobile_menu if is_mobile(request) else navbar
    firestore_docs = db.collection('books').stream()  # Assuming you have a 'books' collection in Firestore

    return (
        Div(
            Head(
                Defaults
            ),
            Body(
                Header(
                    navigation,
                    cls="sticky top-0 bg-gray-800 z-50"
                ),
                Main(
                    Div(
                        H1("Top SAT Prep Books", cls="text-4xl font-extrabold text-center my-8"),
                        P(
                            "Explore our curated selection of the best SAT preparation books. Click on the links to learn more or purchase your copy.",
                            cls="text-center mb-10 text-lg"
                        ),
                        # SAT Books in grid format
                        Div(
                            *[
                                Div(
                                    Div(
                                        # Book Image and Title
                                        Div(
                                            Div(
                                                Img(
                                                    src=doc.to_dict()['cover_image'], 
                                                    cls="w-32 h-48 rounded-md shadow-lg mx-auto"
                                                ),
                                                cls="text-center"
                                            ),
                                            H3(
                                                doc.to_dict()['title'], 
                                                cls="text-lg font-bold text-gray-700 mt-4 text-center"
                                            ),
                                            cls="mb-4"
                                        ),
                                        # Book Description
                                        Div(
                                            P(
                                                doc.to_dict()['description'],
                                                cls="text-center text-sm mb-4 line-clamp-3"  # Truncated to 3 lines
                                            ),
                                            cls="flex-1"  # Ensures content fills available space
                                        ),
                                        # Referral Link Button
                                        Div(
                                            A(
                                                "Buy Now", 
                                                href=doc.to_dict()['referral_link'], 
                                                cls="btn btn-warning w-full",
                                                target="_blank",  # Opens the link in a new tab
                                            ),
                                            cls="mt-4"
                                        ),
                                        cls="card bg-base-300 shadow-md rounded-lg p-6 flex flex-col justify-between transition hover:shadow-lg h-full"
                                    ),
                                    cls="w-full max-w-xs mx-auto"
                                ) for doc in firestore_docs
                            ],
                            cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8 px-6"
                        ),
                        cls="container mx-auto py-8"
                    ),
                    cls=""
                ),
                cls="bg-base-200 w-full",
                data_theme="silk"
            )
        )
    )

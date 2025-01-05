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
            ), data_theme="lofi",cls="bg-base-200"
        )
    )


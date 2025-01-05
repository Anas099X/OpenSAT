from main import *



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
        Div(
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
            ), data_theme="lofi", cls="bg-base-200"
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
            ), data_theme="lofi",cls="bg-base-200"
        )
    )

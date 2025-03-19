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

    # Determine navigation based on device type
    navigation = mobile_menu if is_mobile(request) else Navbar()

    # Return the HTML response
    return (
        site_title,
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
                    navigation,
                    cls="sticky top-0 z-50"
                ),
                Main(
                    Div(
                        # Card component for question display
                        Div(
                            Div(
                                Div(
                                    H2(copy_question_btn, f"Question #N{num + 1}", cls="card-title text-xl font-bold"),
                                    A(Div(cls="ti ti-exclamation-circle text-2xl"),
                                    "Report a mistake",
                                    href="https://tally.so/r/312ovO",
                                    cls="btn btn-error btn-sm btn-rounded m-1 flex items-center"),
                                cls="flex items-center justify-between w-full"),
                                P(question_obj['question'].get('paragraph', "").replace('null', ""), cls="text-base text-lg mt-2"),
                                B(question_obj['question']['question'], cls="text-lg"),
                                Div(
                                    Div(B("A. "), question_obj['question']['choices']['A'], cls="py-2"),
                                    Div(B("B. "), question_obj['question']['choices']['B'], cls="py-2"),
                                    Div(B("C. "), question_obj['question']['choices']['C'], cls="py-2"),
                                    Div(B("D. "), question_obj['question']['choices']['D'], cls="py-2"),
                                    cls="text-lg"
                                ),
                                Div(
                                    Input(type="checkbox"),
                                    Div("Click to reveal answer", cls="collapse-title flex items-center justify-center text-lg font-bold"),
                                    Div(
                                        B(f"Correct Answer is: {question_obj['question']['correct_answer']}"),
                                        Br(),
                                        P(question_obj['question']['explanation']),
                                        cls="collapse-content text-lg"
                                    ),
                                    cls="collapse collapse-plus bg-warning text-warning-content mt-4"
                                ),
                                cls="card-body"
                            ),
                            cls="card bg-base-300 shadow-lg mx-auto w-full max-w-2xl"
                        ),
                        cls="container mx-auto py-8 px-4"
                    ),cls="bg-base-200" 
                )
               ,data_theme="silk"
            )
        
)



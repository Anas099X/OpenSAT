from main import *

@rt("/explore")
def get(request, session):
    # Removed session-based filtering
    navigation = mobile_menu if is_mobile(request) else Navbar()
    
    return (
        site_title,
        Head(Defaults),
        Body(
            Header(
                # ...existing header code...
                navigation,
                cls="sticky top-0 bg-warning z-50"
            ),
            Main(
                H1("Explore", cls="text-4xl font-extrabold text-center my-8"),
                Div(
                    Div(
                        Div(
                            H1(
                                Div(cls="ti ti-filter text-4xl "),
                                "Filters",
                                cls="text-2xl font-bold mb-4"
                            ),
                            Form(
                                # Section Filter
                                Div(
                                    Div("Section:", cls="text-sm font-semibold mb-2"),
                                    Select(
                                        Option('Pick Section', disabled=True, selected=True),
                                        Option('english'),
                                        Option('math'),
                                        cls='select select-warning bg-warning text-warning-content font-bold',
                                        name="section"
                                    ),
                                    cls="mb-6"
                                ),
                                # Domain Filter
                                Div(
                                    Div("Domain:", cls="text-sm text-gray-600 font-semibold mb-2"),
                                    Select(
                                        Option('Pick Domain', disabled=True, selected=True),
                                        Option('any'),
                                        Option('algebra'),
                                        Option('advanced math'),
                                        Option('problem-solving and data analysis'),
                                        Option('geometry and trigonometry'),
                                        Option('Information and Ideas'),
                                        Option('Craft and Structure'),
                                        Option('Expression of Ideas'),
                                        Option('Standard English Conventions'),
                                        cls='select select-warning bg-warning text-warning-content font-bold',
                                        name="domain"
                                    ),
                                    cls="mb-5"
                                ),
                                Div(
                                    Button("Search", type="submit", cls="btn btn-warning w-full")
                                ),
                                hx_post="/questions_list",
                                hx_target="#question-container",
                                id="search_form"
                            ),
                            cls="p-4 rounded-lg shadow-xl mx-auto bg-base-300 max-w-xl mb-15"
                        ),
                        cls="card bg-ghost max-w-lg mx-auto w-full rounded-box flex-grow justify-center items-start flex"
                    ),
                    Div(cls="divider divider-horizontal mx-4 self-stretch"),  # ...existing code...
                    Div(
                        Div(
                            hx_post="/questions_list",
                            hx_trigger="load",
                            hx_target="#question-container",
                            hx_indicator="#spinner",
                            cls="overflow-auto max-h-[400px] w-full mt-5",
                            id="question-container"
                        ),
                        Div(
                            Span(cls="htmx-indicator loading loading-spinner loading-xl", id="spinner"),
                            cls="flex justify-center items-center w-full mt-5"
                        ),
                        cls="card bg-ghost rounded-box flex flex-grow justify-center items-start self-stretch"
                    ),
                    cls="flex w-full flex-col lg:flex-row",
                    id="explore-container"
                ),
                cls="container mx-auto py-4"
            ),
            data_theme="silk",
            cls="bg-base-200"
        )
    )

# Removed old filtering endpoints: /section_filter, /domain_filter, and /filters_switch

@rt('/questions_list')
def post(section: str = "english", domain: str = "any"):
    questions = question_objects(section)  # Use provided section
    return Div(
        *[
            A(
                Div(
                    Div(Div(cls="ti ti-books text-4xl"), cls="flex-shrink-0 p-2"),
                    Div(
                        H2(f"Question #{i + 1}", cls="font-bold text-lg "),
                        P(x["domain"], cls="text-sm"),
                        Div(Div(f"Difficulty: {x.get('difficulty', 'N/A')}", cls="text-xs"), cls="flex space-x-4 mt-1"),
                        cls="flex-grow"
                    ),
                    cls="flex items-center bg-base-300 hover:bg-warning hover:text-warning-content rounded-lg shadow-md p-4 transition-all"
                ),
                href=f"/questions?{urlencode({'section': section, 'num': i})}",
                cls="block w-full mb-3"
            ) if str(domain).lower() == "any" or str(x['domain']).lower() == str(domain).lower() else Div("", hidden=True)
            for i, x in enumerate(questions)
        ],
        id="question-container"
    )

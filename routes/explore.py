from main import *

@rt("/explore")
def get(request, session):

    # Get section and domain from query parameters, with defaults
    section = request.query_params.get("section", "english")  # Default section: English
    domain = request.query_params.get("domain", "any")  # Default domain: any

    def domain_lower(input):
        return str(input).lower()

    # Generate filter buttons dynamically
    def filter_switch():
        filters = {
            "english": [
                {"label": "Information and Ideas", "value": "information and ideas"},
                {"label": "Craft and Structure", "value": "craft and structure"},
                {"label": "Expression of Ideas", "value": "expression of ideas"},
                {"label": "Standard English Conventions", "value": "standard english conventions"}
            ],
            "math": [
                {"label": "Algebra", "value": "algebra"},
                {"label": "Advanced Math", "value": "advanced math"},
                {"label": "Problem-Solving and Data Analysis", "value": "problem-solving and data analysis"},
                {"label": "Geometry and Trigonometry", "value": "geometry and trigonometry"}
            ]
        }

        category_filters = filters.get(section.lower(), [])
        return [
            A(
                f["label"],
                href=f"?{urlencode({'section': section, 'domain': f['value']})}",
                cls=f"btn btn-pink btn-rounded btn-outline btn-sm {'btn-active' if domain == f['value'] else ''}"
            )
            for f in category_filters
        ]

    # Question list view generation function
    def generate_question_list_view():
        questions = question_objects(section)  # Fetch questions for the section
        return [
            A(
                Div(
                    Div(  # Icon section
                        Div(cls="ti ti-books text-4xl text-primary"),  # Example icon, adjust as needed
                        cls="flex-shrink-0 p-2"
                    ),
                    Div(  # Content section
                        H2(f"Question #{i + 1}", cls="font-bold text-lg"),  # Question title
                        P(x["domain"], cls="text-sm text-gray-500"),  # Domain or category
                        Div(  # Metadata (e.g., stats)
                            Div(f"Difficulty: {x.get('difficulty', 'N/A')}", cls="text-xs text-gray-400"),
                            cls="flex space-x-4 mt-1"
                        ),
                        cls="flex-grow"
                    ),
                    cls="flex items-center bg-base-200 hover:bg-base-300 rounded-lg shadow-md p-4 transition-all"
                ),
                href=f"/questions?{urlencode({'section': section, 'num': i})}",
                cls="block w-full mb-3"
            ) if domain.lower() == "any" or domain_lower(x['domain']) == domain.lower() else Div("", hidden=True)
            for i, x in enumerate(questions)
        ]

    # Generate filter buttons
    filter_buttons = filter_switch()

    # Generate question list view
    question_list_view = generate_question_list_view()

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
                        Div(
                            Div(
                                H1(
                                    Div(cls="ti ti-filter text-4xl text-neutral"),
                                    "Filters",
                                    cls="text-2xl font-bold mb-4"
                                ),
                                # Section Filters with Labels
                                Div(
                                    Div("Section:", cls="text-sm text-gray-600 font-semibold mb-2"),  # Section Label
                                    Div(
                                        A(
                                            Div(cls="ti ti-a-b-2 text-2xl"),
                                            "English",
                                            href=f"?{urlencode({'section': 'english', 'domain': 'any'})}",
                                            cls=f"btn btn-primary btn-rounded btn-outline btn-sm {'btn-active' if section == 'english' else ''}"
                                        ),
                                        A(
                                            Div(cls="ti ti-math-symbols text-2xl"),
                                            "Math",
                                            href=f"?{urlencode({'section': 'math', 'domain': 'any'})}",
                                            cls=f"btn btn-primary btn-rounded btn-outline btn-sm {'btn-active' if section == 'math' else ''}"
                                        ),
                                        cls="btn-group space-x-2"
                                    ),
                                    cls="mb-6"  # Adds spacing between section and domain filters
                                ),
                                # Domain Filters with Labels
                                Div(
                                    Div("Domain:", cls="text-sm text-gray-600 font-semibold mb-2"),  # Domain Label
                                    Div(
                                        *filter_buttons,  # Dynamically generated domain filter buttons
                                        cls="flex flex-wrap gap-2"
                                    ),
                                    cls="mb-4"
                                ),
                                cls="p-4 rounded-lg shadow-xl mx-auto bg-base-200 max-w-xl mt-10"
                            ),
                            cls="card bg-ghost max-w-lg rounded-box flex-grow"
                        ),
                        Div(cls="divider divider-horizontal p-3"),
                        Div(
                            Div(
                                *question_list_view,  # Generates all questions in list view
                                cls="overflow-auto max-h-[500px]"  # Adds scrollable overflow to questions
                            ),
                            cls="card bg-ghost rounded-box flex flex-grow"
                        ),
                        cls="flex w-full flex-col lg:flex-row"
                    ),
                    cls="container mx-auto py-4"
                )
            ),
            data_theme="lofi", cls="pink"  # DaisyUI's lofi theme
        )
    )

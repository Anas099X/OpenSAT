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
                cls=f"btn btn-secondary btn-sm {'btn-active' if domain == f['value'] else ''}"
            )
            for f in category_filters
        ]

    # Question card generation function
    def generate_question_cards():
        questions = question_objects(section)  # Fetch questions for the section
        return [
            A(
                Div(
                    Div(Div(cls="ti ti-books text-4xl text-neutral"), cls="text-3xl"),  # Icon
                    Div(f'Question #{i + 1}', cls="font-bold text-xl"),  # Question title
                    Div(x['domain'], cls="font-bold text-pink-400"),  # Domain badge
                    cls="card-body"
                ),
                cls="card bg-base-200 shadow-2xl w-96 mx-auto hover:bg-base-300 transition-all rounded-lg",
                href=f"/questions?{urlencode({'section': section, 'index': i})}"
            ) if domain.lower() == "any" or domain_lower(x['domain']) == domain.lower() else Div('', hidden=True)
            for i, x in enumerate(questions)
        ]

    # AdSense card
    def ads_card():
     return Div(
        Div(
            Span("Ad", cls="indicator-item badge badge-success"),  # Badge with "Ad"
            data_mndazid="54740ac2-34e1-4bcb-b575-b9e67b4d11e0",
            cls="indicator"  # Indicator class for styling
        ),
        cls="card bg-base-200 shadow-2xl w-96 h-20 mx-auto rounded-lg"
    )
    def responsive_ads_card():
     return Div(
        Div(
            Span("Ad", cls="indicator-item badge badge-success"),  # Ad indicator badge
            Div(
                Script(
                    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2090178937498462",
                    crossorigin="anonymous"
                ),
                Ins(
                    cls="adsbygoogle",
                    style="display:block",
                    data_ad_client="ca-pub-2090178937498462",
                    data_ad_slot="8188391527",
                    data_ad_format="auto",
                    data_full_width_responsive="true"
                ),
                Script('(adsbygoogle = window.adsbygoogle || []).push({});'),
                cls="card bg-base-200 mx-auto rounded-lg"
            ),
            cls="indicator"  # Indicator class for proper positioning
        ),
         cls="card bg-base-200 shadow-2xl w-96 mx-auto rounded-lg"
    )


    # Generate filter buttons
    filter_buttons = filter_switch()

    # Generate question cards
    question_cards = generate_question_cards()

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
                            cls="navbar-start"
                        ),
                        menu_button(session),
                        cls="navbar shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Filters section - centered and styled
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
                                        Div(cls="ti ti-a-b-2 text-2xl text-neutral"), 
                                        "English",
                                        href=f"?{urlencode({'section': 'english', 'domain': 'any'})}",
                                        cls=f"btn btn-primary btn-sm {'btn-active' if section == 'english' else ''}"
                                    ),
                                    A(
                                        Div(cls="ti ti-math-symbols text-2xl text-neutral"), 
                                        "Math",
                                        href=f"?{urlencode({'section': 'math', 'domain': 'any'})}",
                                        cls=f"btn btn-primary btn-sm {'btn-active' if section == 'math' else ''}"
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
                            cls="p-4 rounded-lg shadow-xl mx-auto bg-base-200", 
                            style="max-width:100vh; margin-bottom:4vh;"
                        ),
                        # Questions list section - responsive grid layout with 3 columns max
                        Div(
                            *question_cards,  # Generates all question cards
                            cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"  # Responsive grid
                        ),
                        cls="flex flex-col space-y-6"
                    ),
                    cls="container mx-auto py-8"
                )
            ), data_theme="retro", cls='bg-base-200'  # DaisyUI's retro theme
        )
    )

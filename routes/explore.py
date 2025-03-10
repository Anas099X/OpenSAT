from main import *


@rt("/explore")
def get(request, session):
    # Use session filters if present, otherwise use query parameters
    session["filter_section"] = "english"
    session["filter_domain"] = "any"

    section = session.get("filter_section")
    domain  = session.get("filter_domain")
    

    return (
        site_title,
        Head(Defaults),
        Body(
            Header(
                # ...existing header code...
                navbar,
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
                # Section Filters with Labels
                Div(
                    Div("Section:", cls="text-sm font-semibold mb-2"),
                    Div(
                        Form(
                            Input(cls="btn btn-warning m-1", type="radio", name="filters", aria_label="english", value="english", hx_post="/section_filter", hx_target="#section-filter"),
                            Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="math", value="math", hx_post="/section_filter", hx_target="#section-filter"),
                            id="section-filter"
                        ),
                    ),
                    cls="mb-6"
                ),
                # Domain Filters with Labels
                Div(
                    Div("Domain:", cls="text-sm text-gray-600 font-semibold mb-2"),
                    Div(
                        hx_post="filters_switch",
                        hx_trigger="load, change from:#section-filter",
                        hx_target="#domain-filter",
                        cls="flex flex-wrap gap-2 w-full",
                        id="domain-filter"
                    ),
                    cls="mb-4"
                ),
                Div(A("Search", cls="btn btn-primary w-full", hx_post="/questions_list", hx_target="#question-container", hx_trigger="click"), id="test_button"),
                cls="p-4 rounded-lg shadow-xl mx-auto bg-base-300 max-w-xl mb-15"
            ),
            cls="card bg-ghost max-w-lg mx-auto w-full rounded-box flex-grow justify-center items-start flex"
        ),
        Div(cls="divider divider-horizontal mx-4 self-stretch"),  # Ensures alignment
        Div(
            Div(
                hx_post="questions_list",
                hx_trigger="load, change from:#test_button",
                hx_target="#question-container",
                hx_indicator="#spinner",
                cls="overflow-auto max-h-[400px] w-full mt-10",
                id="question-container"
            ),
            Div(
                Span(cls="htmx-indicator loading loading-spinner loading-xl", id="spinner"),
                cls="flex justify-center items-center w-full mt-5"
            ),
            cls="card bg-ghost rounded-box flex flex-grow justify-center items-start self-stretch"
        ),
        cls="flex w-full flex-col lg:flex-row",  # Keeps both sections aligned
        id="explore-container"
    ),
    cls="container mx-auto py-4"
),
            data_theme="silk", cls="bg-base-200"
        )
    )

@rt('/section_filter')
def post(filters: str, session):
    session["filter_section"] = filters
    session["filter_domain"] = "any"

    if filters == "english":
     return Input(cls="btn btn-warning m-1", type="radio", name="filters", aria_label="english", value="english", hx_post="/section_filter", hx_target="#section-filter"),Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="math", value="math", hx_post="/section_filter", hx_target="#section-filter")
    else:
     return Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="english", value="english", hx_post="/section_filter", hx_target="#section-filter"),Input(cls="btn btn-warning m-1", type="radio", name="filters", aria_label="math", value="math", hx_post="/section_filter", hx_target="#section-filter")



@rt('/domain_filter')
def post(filters: str, session):
    session["filter_domain"] = filters
    # Reuse questions_list generation logic
    section = session.get("filter_section")
    domain  = session.get("filter_domain")
    questions = question_objects(section)  # Get questions for the section

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

@rt('/questions_list')
def post(session):
    section = session.get("filter_section")
    domain  = session.get("filter_domain")
    print(domain)

    # Fetch updated questions based on both filters
    questions = question_objects(section)  # Get questions for the section

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

@rt('/filters_switch')
def post(session):
        # Generate filters based on the current section
        section = session.get("filter_section")
        if section == "english":
            return Form(
                Input(cls="btn btn-error btn-square m-1", type="reset",name="filters",value="×", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Information and Ideas", value="Information and Ideas", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Craft and Structure", value="Craft and Structure", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Expression of Ideas", value="Expression of Ideas", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Standard English Conventions", value="Standard English Conventions", hx_post="domain_filter", hx_target="#question-container"),
                cls="filter"
            )
        else:
            return Form(
                Input(cls="btn btn-error btn-square m-1", type="reset",name="filters", value="×", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Algebra", value="algebra", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Advanced Math", value="advanced math", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Problem-Solving and Data Analysis", value="problem-solving and data analysis", hx_post="domain_filter", hx_target="#question-container"),
                Input(cls="btn btn-active m-1", type="radio", name="filters", aria_label="Geometry and Trigonometry", value="geometry and trigonometry", hx_post="domain_filter", hx_target="#question-container"),
                cls="filter mt-2"
            )

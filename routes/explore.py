from main import *

# Add global variable for storing checked questions
checked_questions = []

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
                                        Option('English'),
                                        Option('Math'),
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
                                        Option('Any'),
                                        Option('Algebra'),
                                        Option('Advanced Math'),
                                        Option('Problem-Solving and Data Analysis'),
                                        Option('Geometry and Trigonometry'),
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
                                    Button(I(cls="ti ti-search text-warning-content text-lg"),"Search", type="submit", cls="btn btn-warning w-3/4"),
                                    # Updated: set type="button", add hx attributes to trigger /printable_checkbox on click
                                    Button(
                                        I(cls="ti ti-printer text-warning-content text-xl"),
                                        "Print Selected Questions", 
                                        type="button",
                                        id="checkbox_button",
                                        cls="btn btn-warning mt-5",
                                        hx_post="/printable_checkbox",
                                        hx_trigger="click",
                                        hx_swap="none",
                                        hx_include="[name=question_id]"
                                    )
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
def post(session,section: str = "english", domain: str = "any", page: int = 1):
    section = section.lower()
    session["checked_questions"] = []
    session["print_section"] = section
    domain = domain.lower()
    questions = question_objects(section)
    start = (page - 1) * 30
    end = page * 30
    return Div(
        *[
            Div(
                Input(type="checkbox"),
                # Collapse title: now without inner A element
                Div(
                    Div(
                        Div(Div(cls="ti ti-books text-4xl"), cls="flex-shrink-0 p-2"),
                        Div(
                            H2(f"Question #{start + i + 1}", cls="font-bold text-lg"),
                            P(x["domain"], cls="text-sm"),
                            Div(
                                Div(f"Difficulty: {x.get('difficulty', 'N/A')}", cls="text-xs"),
                                cls="flex space-x-4 mt-1"
                            ),
                            cls="flex-grow"
                        ),
                        cls="flex items-center"
                    ),
                    A(
                    # transparent overlay
                    href=f"/questions?{urlencode({'section': section, 'num': start + i})}",
                    cls="absolute inset-0 z-50 w-3/4"),
                    cls="collapse-title collapse-title-lg"
                ),
                # Collapse content remains unchanged
                Div(
                    # Preview at the very top
                    Div("Select Question",
                        Input(
                        type='checkbox', 
                        name="question_id", 
                        value=f"{start + i}", 
                        cls='checkbox checkbox-sm checkbox-error mb-1'),
                        cls="text-lg"),
                    P(
                        "Question Preview..",
                        cls="text-xs italic mb-2 mt-5"
                    ),
                    Div(
                        # Full content details
                        P(x["question"].get("paragraph", " ").strip(), cls="text-sm") if x["question"].get("paragraph", " ").strip() else " ",
                        Br(),
                        P(
                            Span(x["question"]["question"], cls="mathjax"),
                            cls="text-sm font-bold"
                        ),
                        Div(
                            Div(B("A. "), x["question"]["choices"]["A"], cls="py-1"),
                            Div(B("B. "), x["question"]["choices"]["B"], cls="py-1"),
                            Div(B("C. "), x["question"]["choices"]["C"], cls="py-1"),
                            Div(B("D. "), x["question"]["choices"]["D"], cls="py-1"),
                            cls="text-sm"
                        )
                    ),
                    cls="collapse-content",
                    style="max-width: 130vh; overflow-y: auto;"
                ),
                # Overlay card with the same size to capture clicks
                cls="collapse collapse-plus bg-base-300 hover:bg-warning hover:text-warning-content rounded-lg shadow-md p-1 mb-3 relative"
            ) if str(domain).lower() == "any" or str(x['domain']).lower() == str(domain).lower() else Div("", hidden=True)
            for i, x in enumerate(questions[start:end])
        ],
        Div(
            # Pagination controls
            (Button("«", type="button", cls="join-item btn btn-warning", 
                    hx_post=f"/questions_list?section={section}&domain={domain}&page={page - 1}",
                    hx_trigger="click", hx_target="#question-container")
             if page > 1 else ""),

            Button(f"Page {page}", type="button", cls="join-item btn btn-warning disabled"),
            # Updated: use hx_post to load next page
            (Button("»", type="button", cls="join-item btn btn-warning", 
                    hx_post=f"/questions_list?section={section}&domain={domain}&page={page + 1}",
                    hx_trigger="click", hx_target="#question-container")
             if len(questions) > end else ""),
            cls="join"
        ),
        id="question-container"
    )


@rt('/printable_checkbox')
def post(session, question_id: list[str] = None):
    if session["checked_questions"]:
     del session["checked_questions"]
    session["checked_questions"] = question_id
    print("Received question IDs:", session["checked_questions"])  # Print the received question IDs for debugging
    # Print the received question IDs for debugging
    return Redirect("/print")



@rt('/print')
def get(session):
    checked = session.get("checked_questions", [])
    questions = question_objects(session["print_section"])
    heroes = []
    for i, x in enumerate(checked):
        try:
            q = questions[int(x)]
            heroes.append(
                Div(
                    # ...existing hero content header...
                    P(B(f"{i + 1}. "), q["question"].get("paragraph", "No preview available").strip() or "No preview available", cls="mb-2"),
                    H2(q["question"]["question"], cls="text font-bold"),
                    Div(
                        Div(B("A. "), q["question"]["choices"]["A"], cls="py-0.5"),
                        Div(B("B. "), q["question"]["choices"]["B"], cls="py-0.5"),
                        Div(B("C. "), q["question"]["choices"]["C"], cls="py-0.5"),
                        Div(B("D. "), q["question"]["choices"]["D"], cls="py-0.5"),
                        cls="text"
                    ),
                    Div(cls="divider"),
                    cls="m-4 p-1",
                )
            )
        except (ValueError, IndexError):
            continue

    navbar = Div(
        # ...existing navbar code...
        Div(
            Div(
                I(cls="ti ti-school text-base-content text-4xl"),
                P("opensat", cls="puff text-xl text-base-content"),
                cls="btn btn-disabled rounded-full btn-ghost normal-case text-lg",
                href="/"
            ),
            cls="navbar-start"
        ),
        Div(
        Button(
         I(cls="ti ti-printer text-netural-content text-xl"),
         "Print",
         cls="btn btn-active no-print",
         onclick="window.print()"),
         cls="navbar-end"
        ),
        cls="navbar bg-ghost"
    )
    return (
        site_title,
        Head(
            Defaults,
            Style(
                """
                @media print {
                    .no-print, .navbar { display: none !important; }
                }
                """,
                type="text/css"
            )
        ),
        navbar,
        Body(
            Main(*heroes),
            data_theme="silk",
            cls="bg-base-300"
        )
    )
# ...existing code...

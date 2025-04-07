from asyncio import sleep
import firebase_admin
from firebase_admin import firestore
from main import *

# Initialize Firestore (if not already done)
if not firebase_admin._apps:
    firebase_admin.initialize_app()
db = firestore.client()


def check_subscription_expired(email: str):
    """Remove subscription details if subscription_date is older than 1 month."""
    doc_ref = db.collection("users").document(email)
    doc = doc_ref.get()
    if not doc.exists:
        return
    data = doc.to_dict()
    sub_date = data.get("subscription_date")
    if sub_date and isinstance(sub_date, datetime):
        # Convert sub_date to naive datetime by removing tzinfo
        naive_sub_date = sub_date.replace(tzinfo=None)
        if datetime.utcnow() - naive_sub_date > timedelta(days=30):
            doc_ref.update({
                "subscribed": firestore.DELETE_FIELD,
                "subscription_date": firestore.DELETE_FIELD
            })

@rt("/practice/explore")
def get(request, session):

    # reset tests
    if 'page' not in session or session['page'] is None:
        session['page'] = 0
    del session['page']    

    # Load modules from JSON file
    modules = question_objects('practice_test')

    navigation = mobile_menu if is_mobile(request) else Navbar()

    # Check if the user is subscribed.
    email = session.get("user", {}).get("email")
    check_subscription_expired(email)
    subscribed = False
    if email:
        doc = db.collection("users").document(email).get()
        subscribed = doc.exists and doc.to_dict().get("subscribed", False)
    # Limit results for unsubscribed users.
    if not subscribed:
        modules = modules[:2]
    def subscribe_overlay():
        if not subscribed:
            return Div(
                Div(
                    P("Unlock all practice tests and more!", cls="text-lg font-bold text-center"),
                    A("Subscribe", href="/subscription", cls="btn btn-warning btn-active w-full mt-4"),
                    cls="card bg-base-300 text-warning-content shadow-lg w-96 mx-auto p-8"
                ),
                cls="fixed inset-x-0 bottom-0 h-1/2 bg-soft bg-opacity-50 flex items-center justify-center z-50"
            )    

    return (
            site_title,
            Head(
                Defaults
            ),
            Body(
                Header(
                    navigation,
                    cls="sticky top-0 bg-gray-800 z-50"
                ),
                Main(
                    subscribe_overlay(),
                    Div(
                        # Loop through modules and create a card for each one
                        *[
                            Div(
                                A(
                                    Div(Div(cls="ti ti-highlight text-4xl"), cls="text-3xl"),  # Icon for each module
                                    H2(module['name'], cls="card-title text-xl font-bold mt-1"),  # Module name
                                    P("Practice Test", cls=" font-bold"),
                                    cls="card bg-base-300 shadow-lg w-96 mx-auto hover:bg-warning hover:text-warning-content transition-all rounded-lg p-8",
                                    href=f"/practice/{i}/select_timer" 
                                )
                            )
                            for i, module in enumerate(modules)
                        ],
                        cls="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"  # Responsive grid layout
                    ),
                    cls="container mx-auto py-8"
                )
             ,data_theme="silk",cls="bg-base-200 w-full"
            )
        
    )


# New route to store timer selection in session
@rt("/practice/{practice_num}/set_timer")
def set_timer(request, session, practice_num: int):
    timer_value = request.query_params.get("timer", "false")
    session["timer_choice"] = timer_value
    return Redirect(f"/practice/{practice_num}/module/1")

@rt("/practice/{practice_num}/select_timer")
def select_timer(request, session, practice_num: int):
    return (
        Html(
            Head(Defaults),
            Body(
                Main(
                    Div(
                        H2("Select Mode", cls="text-2xl font-bold text-center"),
                        P("Choose a mode to take the test:", cls="text-center mb-4"),
                        Div(
                            # Updated links to store timer choice in session
                            A("With Timer", href=f"/practice/{practice_num}/set_timer?timer=true", cls="btn btn-success mx-2"),
                            A("Without Timer", href=f"/practice/{practice_num}/set_timer?timer=false", cls="btn btn-warning mx-2"),
                            cls="flex justify-center"
                        ),
                        cls="card bg-base-300 shadow-xl w-96 mx-auto py-8"
                    ),
                    cls="flex items-center justify-center min-h-screen"
                )
            ),
            data_theme="silk", cls="bg-base-200 w-full"
        )
    )


@rt("/practice/{practice_num}/module/{module_number}")
def get(request, session, practice_num: int, module_number: int):
    #del session['page']

    # Load the current module and initialize session state
    module = f'module_{module_number}'

    # Check if the user is subscribed.
    email = session.get("user", {}).get("email")
    subscribed = False
    if email:
        doc = db.collection("users").document(email).get()
        subscribed = doc.exists and doc.to_dict().get("subscribed", False)

    # Limit results for unsubscribed users.
    if not subscribed and practice_num > 2:
        return Redirect("/practice/explore")
    
    if 'page' not in session or session['page'] is None:
        session['page'] = 0
    if module not in session or session[module] is None:
        session[module] = []

    # Load practice questions
    practice_en_questions = question_objects('practice_test')
    
    # Get the current question object
    question_obj = question_objects('english' if module_number < 3 else 'math')[practice_en_questions[practice_num][module][session['page']]]

    # Helper to retrieve answers from session
    def answers_session(count):
        for answer in session[module]:
            if str(count) in answer:
                return answer[str(count)]
            
    def module_title():
        if module == "module_1" or module == "module_2":
            return "Reading & Writing"
        if module == "module_3" or module == "module_4":
            return "Math"           

    # Button for navigating to the next page/module
    def module_switcher():
        #checking different states of module
        if session['page'] < len(practice_en_questions[practice_num][module]) - 1:
            return A("Next", hx_post=f'/switch_page/{practice_num}/{module_number}/{session["page"]+1}', hx_swap="innerHTML", hx_target='#practice_html', cls="btn btn-warning rounded-full")
        elif module == "module_2":
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/break', cls="btn btn-warning rounded-full")
        elif module == "module_4":
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/check', cls="btn btn-warning rounded-full")
        else:
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/module/{module_number + 1}', cls="btn btn-warning rounded-full")

    # Timer check: read timer setting from session instead of query_params
    timer_check = session.get("timer_choice", "false")

    #Timer Div
    def timer_div():
        if timer_check == "true":
            return Div(
                Div(id="countdown-display", hx_trigger='every 1s'),
                hx_ext='sse',
                sse_connect=f"/sse_timer?practice_num={practice_num}&module_number={module_number}",
                hx_swap="innerHTML",
                sse_swap="message",
                hx_target="#countdown-display"
            )
        else:
            return Div("No Timer", cls="text-xl font-bold text-center")
    


    # Function for radio options (answer selection)
    def practice_options(value: str):
        if answers_session(session['page']) == value:
            return Input(type="radio", name="answer", value=value, checked=True, cls="radio radio-warning")
        else:
            return Input(type="radio", name="answer", value=value, cls="radio radio-warning")


    return (
        Html(
            Head(Defaults),
            Body(
                Header(
                    Div(
                        # Header container with three sections: left, center, right
                        Div(  # Left section: logo/text
                            Div(
                                H1(module_title(),cls="text-2xl font-bold")
                            ),
                            cls="navbar-start"
                        ),
                        Div(  # Center section: timer
                            H1(
                                timer_div(),
                                cls="text-xl font-extrabold text-center"
                            ),
                            cls="navbar-center"
                        ),
                        Div(  # Right section: menu button
                            menu_button(),
                            cls="navbar-end"
                        ),
                        cls="navbar bg-warning sticky top-0 z-50",
                        hx_swap_oob="true"
                    ),
                    cls="sticky top-0 bg-gray-800 z-50 text-warning-content"
                ),
                Main(
                  Div(
                      # Dropdown for page selection
                         
                 
                        # Question content inside a DaisyUI card
                        Div(
    
                            Div(
                                P(question_obj['question'].get('paragraph', "").replace('null',''), cls="text-base mb-4"),
                                B(question_obj['question']['question'], cls="text-lg font-bold"),
                                Form(
                                    Div(
                                        Label(
                                            practice_options('A'),
                                            Span("A. " + question_obj['question']['choices']['A'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        Br(),
                                        Label(
                                            practice_options('B'),
                                            Span("B. " + question_obj['question']['choices']['B'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        Br(),
                                        Label(
                                            practice_options('C'),
                                            Span("C. " + question_obj['question']['choices']['C'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        Br(),
                                        Label(
                                            practice_options('D'),
                                            Span("D. " + question_obj['question']['choices']['D'], cls="ml-2"),
                                            cls="flex items-center space-x-2"
                                        ),
                                        cls="mt-4"
                                    ),
                                    cls="form-control",
                                    hx_post=f"/page/{module}/{session['page']}",
                                    hx_trigger="change",
                                    hx_swap="none"
                                ),
                                cls="card-body"
                            ),
                            Div(
                                A("Back", hx_post=[f'/switch_page/{practice_num}/{module_number}/{session["page"]-1}' if session['page'] > 0 else None], hx_swap="innerHTML", hx_target='#practice_html', cls="btn btn-active rounded-full bg-base-300"),
                                Div(
        Div(f"Question {session['page'] + 1}", cls="btn btn-warning m-1", tabindex="0", role="button"),
        Div(
            Div(
                H3(f"Select a Question", cls="card-title text-lg font-semibold mb-4"),
                Div(
                    # Grid layout for page buttons
                    *[
                        A(
                            f"{i + 1}", 
                            hx_post=f"/switch_page/{practice_num}/{module_number}/{i}",
                            hx_swap="innerHTML",
                            hx_target='#practice_html', 
                            cls="btn btn-outline btn-warning w-12 h-10 m-1 text-lg font-semibold shadow"
                        ) 
                        for i, _ in enumerate(practice_en_questions[practice_num][module])
                    ],
                    cls=" gap-3 justify-items-center"  # Ensures buttons align properly
                ),
                cls="card-body"
            ),
            cls="dropdown-content card bg-base-300 z-[1] w-[300px] h-[480px] absolute left-1/2 top-12 transform -translate-x-1/2 z-10 shadow",
            tabindex="0"
        ),
        cls="dropdown dropdown-top dropdown-hover"
    ),
                                module_switcher(),
                                cls="flex justify-between items-center mt-6 p-5"
                            )
                            ,
                            cls="card bg-base-300 shadow-xl w-full max-w-3xl mx-auto mt-8"
                        ),
                        # Navigation: Back, Page Number, Next/Finish
                       
                    ),
                    cls="container mx-auto py-8 px-4",
                    id="practice_html"
                )
                
            ),
            data_theme="silk",cls="bg-base-200 w-full"  # silk theme enabled
        )
    )


@rt('/switch_page/{practice}/{module_number}/{value}')
def post(session,practice:str,module_number:str,value:int):
 # Initialize module in the session if it doesn't exist or if it's None
    session.setdefault('page', 0)
    session['page'] = value
    return RedirectResponse(f'/practice/{practice}/module/{module_number}', status_code=303)


@rt('/sse_timer')
async def sse_timer(request):
    query_params = request.query_params
    practice_num = query_params.get("practice_num")
    module_number = int(query_params.get("module_number", 1))
    module_times = {
        1: (32, 0),
        2: (32, 0),
        3: (35, 0),
        4: (35, 0)
    }
    default_minutes, default_seconds = module_times.get(module_number, (1, 0))
    minutes = int(query_params.get("minutes", default_minutes))
    seconds = int(query_params.get("seconds", default_seconds))
    total_seconds = (minutes * 60) + seconds

    async def timer_generator():
        for i in range(total_seconds, -1, -1):
            mins, secs = divmod(i, 60)
            yield sse_message(Span(
                Span(style=f"--value:{mins};"), "m",
                Span(style=f"--value:{secs};", **{"data-countdown": "true"}), "s",
                id='countdown-display',
                cls='countdown font-mono text-2xl'
            ))
            await sleep(1)
        if module_number == 1:
            next_route = f"/practice/{practice_num}/module/2"
        elif module_number == 2:
            next_route = f"/practice/{practice_num}/break"
        elif module_number == 3:
            next_route = f"/practice/{practice_num}/module/4"
        elif module_number == 4:
            next_route = f"/practice/{practice_num}/check"
        else:
            next_route = f"/practice/{practice_num}/module/1"
        # Updated the final yield to redirect directly with a script.
        yield sse_message(Div(
            Script(f"setTimeout(() => window.location.href='{next_route}', 80)"),
            "⏳ Countdown Complete! Moving to Next...",
            id='countdown-display',
            style="color: green; font-weight: bold;"
        ))
    
    return EventStream(timer_generator())

@rt("/practice/{practice_num}/break")
def get(practice_num:int):
    return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Main(
                    Div(
                        H2("Break Time!",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("click continue to start the next module",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("Continue", href=f"/practice/{practice_num}/module/3", cls="btn btn-primary"),
                            style="display:flex; justify-content:center;"
                            
                        ),
                        cls="card bg-base-300 w-96 shadow-xl mx-auto py-8"
                    )
                ),cls="flex items-center justify-center"
            ),data_theme="silk",cls="bg-base-200"
        )
    )

@rt("/practice/{practice_num}/check")
def get(practice_num: int, session):
    practice_en_questions = question_objects('practice_test')

    def checker():
        correct_answers = []
        results = []
        mistakes = []

        def answer_collecter(module_num):
            section = 'english' if module_num < 3 else 'math'
            for question_num in practice_en_questions[practice_num][f'module_{module_num}']:
                answer = question_objects(section)[question_num]['question']['correct_answer']
                correct_answers.append((answer, section, question_num))

        for num in [1, 2, 3, 4]:
            correct_answers.clear()
            user_answers = session[f'module_{num}']
            answer_collecter(num)

            for d in user_answers:
                index_str, user_answer = list(d.items())[0]
                index = int(index_str)

                if 0 <= index < len(correct_answers):
                    correct_answer, section, question_num = correct_answers[index]
                    if correct_answer == user_answer:
                        results.append(1)
                    else:
                        results.append(0)
                        mistakes.append((question_num, user_answer, correct_answer, section))
                else:
                    results.append(0)
                    mistakes.append((index + 1, user_answer, "Out of bounds", "N/A"))

            del session[f'module_{num}']
            session['page'] = 0
        return sum(results), mistakes

    # Calculate score and gather mistakes
    score, mistakes = checker()

    # HTML structure with score and mistakes table inside cards using DaisyUI classes
    return (
    Html(
        Head(
            Defaults
        ),
        Body(
            Main(
                # Card for score display
                Div(
                    H2("Your Score", style="font-size: 2.25rem; font-weight: 700; text-align: center; color: #333;"),
                    P(f"{score}/96", style="font-size: 1.5rem; text-align: center; color: #333; margin-top: 10px; font-weight: 600;"),
                    Br(),
                    Div(
                            A("Finish", href=f"/practice/{practice_num}/module/3", cls="btn btn-primary"),
                            style="display:flex; justify-content:center;"
                       ),

                    cls="card bg-base-300 w-96 shadow-xl mx-auto py-8 mb-6"
                ),
                
                # Card for mistakes table
                Div(
                    H2("Mistakes", style="font-size: 1.5rem; font-weight: 600; text-align: center; color: #333; margin-bottom: 20px;"),
                    Div(
                        Table(
                            Thead(
                                Tr(
                                    Th("Questions", cls="px-8 py-2"),
                                    Th("Your Answer", cls="px-8 py-2"),
                                    Th("Correct Answer", cls="px-8 py-2"),
                                    Th("Action", cls="px-8 py-2")
                                )
                            ),
                            Tbody(
                                *[
                                    Tr(
                                        Td(str(question_num), cls="border border-neutral px-8 py-2"),
                                        Td(user_answer, cls="border border-neutral px-8 py-2"),
                                        Td(correct_answer, cls="border border-neutral px-8 py-2"),
                                        Td(
                                            A("Go to question", href=f"/questions?section={section}&num={question_num}", cls="text-info underline"),
                                            cls="border border-neutral px-8 py-2"
                                        )
                                    )
                                    for question_num, user_answer, correct_answer, section in mistakes
                                ]
                            ),
                            cls="table w-full border-collapse border border-neutral"
                        ),
                        cls="overflow-x-auto px-4"  # Responsive container for table
                    ),
                    cls="card bg-base-300 shadow-xl mx-auto w-full max-w-3xl py-8"
                )
            ),
            cls="flex items-center justify-center min-h-screen"
        ),
        data_theme="silk",cls="bg-base-200 w-full"
    )
)
    


@rt('/page/{module}/{count}')
def post(session, count: int, module: str, answer: str):
 # Initialize module in the session if it doesn't exist or if it's None
    if module not in session or session[module] is None:
        session[module] = []
    practice_answers = session[module]

    # Ensure count is an integer, but we need it as a string to use as a key in the dictionary
    count_str = str(count)

    # Update or append the new item
    for item in practice_answers:
        if count_str in item:
            # If the count already exists, update the answer
            item[count_str] = answer
            break
    else:
        # If the count doesn't exist, append a new item
        practice_answers.append({count_str: answer})

    # Sort the practice_answers list by the integer value of the 'count' key in each dictionary
    practice_answers.sort(key=lambda item: int(list(item.keys())[0]))

    # Update the session with the modified and sorted practice_answers
    session[module] = practice_answers


    # Update the session
    session[module] = practice_answers


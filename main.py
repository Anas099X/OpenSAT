from fasthtml.common import *
from settings import *
from datetime import *
import asyncio
import random, json, time
from starlette.responses import StreamingResponse

app,rt = fast_app(debug=True,live=True)

Defaults = (Meta(name="viewport", content="width=device-width"),
            Meta(property="og:title" ,content="OpenSAT: Question Bank with Endless Possibilities"),
            Meta(property="og:description" ,content="OpenSAT, a free and open-source SAT question bank. Dive into a massive pool of SAT practice problems, constantly growing thanks to a dedicated community of contributors."),
            Meta(property="og:image" ,content="https://github.com/Anas099X/OpenSAT/blob/main/public/banner.png?raw=true"),
            Meta(property="og:url" ,content="https://opensat.fun/"),
            Meta(property="og:type" ,content="website"),
            Title("OpenSAT"),
            Link(rel="icon",href="public/graduation-cap-solid.svg", sizes="any", type="image/svg+xml"),
            Script('''MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};'''),
            Script(src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"),
            Script(src="https://unpkg.com/htmx.org@2.0.2"),
            Script(src="/_vercel/insights/script.js"),
            Link(href="https://cdn.jsdelivr.net/npm/daisyui@4.12.12/dist/full.min.css",rel="stylesheet",type="text/css"),
            Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
            Script(src="https://cdn.tailwindcss.com"),
                Title("OpenSAT"),
            Style(open('main.css').read())    
                
)




@rt("/")
def get():
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
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar-start"
                        ),
                        Div(
                             A("Practice", href="/practice/explore", cls="btn rounded-full btn-sm btn-primary"),
                            A("Tutors", href="/tutors", cls="btn rounded-full btn-sm btn-primary"),
                            A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn rounded-full btn-sm btn-secondary"),
                            cls="navbar-end space-x-2"
                        ),
                        cls="navbar bg-base-90 shadow bg-ghost"
                    )
                ),
                Main(
                        Div(
                        Span("🎓", style="display: flex; font-size: 5rem; margin-bottom: 20px; justify-content: center;"),
                        H2("Question Bank with ", U("Endless", cls="text-primary"), 
                           " Possibilities",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("OpenSAT, a free and open-source SAT question bank. "
                          "Dive into a massive pool of SAT practice problems, "
                          "constantly growing thanks to a dedicated community of contributors.",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("Explore", href="/explore/english/any", cls="btn rounded-full btn-primary"),
                            A("Contribute", href="https://github.com/Anas099X/OpenSAT", cls="btn rounded-full btn-secondary"),
                            style="display: flex; justify-content: center; gap: 15px;"
                        ),
                        cls="card bg-base-100 shadow-xl mx-auto p-10 mt-10",
                        style="max-width:100vh;"
                    )
                )
            ),data_theme="retro"
        )
    )



@rt("/explore/{section}/{domain}")
def get(section: str, domain: str):

    def domain_lower(input):
        return str(input).lower()

    def filter_switch():
        if section == 'english':
            return (
                A("Information and Ideas", href=f'/explore/{section}/information and ideas', cls="btn btn-secondary btn-sm"),
                A("Craft and Structure", href=f'/explore/{section}/craft and structure', cls="btn btn-secondary btn-sm"),
                A("Expression of Ideas", href=f'/explore/{section}/expression of ideas', cls="btn btn-secondary btn-sm"),
                A("Standard English Conventions", href=f'/explore/{section}/standard english conventions', cls="btn btn-secondary btn-sm")
            )
        else:
            return (
                A("Algebra", href=f'/explore/{section}/algebra', cls="btn btn-secondary btn-sm"),
                A("Advanced Math", href=f'/explore/{section}/advanced math', cls="btn btn-secondary btn-sm"),
                A("Problem-Solving and Data Analysis", href=f'/explore/{section}/problem-solving and data analysis', cls="btn btn-secondary btn-sm"),
                A("Geometry and Trigonometry", href=f'/explore/{section}/geometry and trigonometry', cls="btn btn-secondary btn-sm")
            )

    # Question card generation function
    def generate_question_cards():
        return [
            A(
                Div(
                    Div("📚", cls="text-3xl"),  # Icon
                    Div(f'Question #{i + 1}', cls="font-bold text-xl"),  # Question title
                    Div(x['domain'], cls="font-bold text-primary"),  # Domain badge
                    cls="card-body"
                ),
                cls="card bg-base-100 shadow-xl w-96 mx-auto hover:bg-base-200 transition-all rounded-lg",  # Fixed width and centered
                href=f"/questions/{section}/{i}/True"
            ) if domain.lower().replace('%20', ' ') == 'any' or domain_lower(x['domain']) == domain.lower().replace('%20', ' ') else Div('', hidden=True)
            for i, x in enumerate(question_objects(section))
        ]

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
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar-start"
                        ),
                        Div(
                            A("Tutors", href="/tutors", cls="btn rounded-full btn-sm btn-primary"),
                            A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn rounded-full btn-sm btn-secondary"),
                            cls="navbar-end space-x-2"
                        ),
                        cls="navbar bg-base-90 shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Filters section - centered and styled
                        Div(
                            H1("🔎 Filters", cls="text-2xl font-bold mb-4"),
                            Div(
                                A("English", href=f'/explore/english/any', cls=["btn btn-primary rounded-full" if section == 'english' else "btn rounded-full"]),
                                A("Math", href=f'/explore/math/any', cls=["btn btn-primary rounded-full" if section == 'math' else "btn rounded-full"]),
                                cls="btn-group space-x-2"
                            ),
                            Br(),
                            Div(filter_switch(), cls="flex flex-wrap gap-2 mt-4 justify-center"),  # Centered filter buttons
                            cls="p-4 border rounded-lg shadow-xl mx-auto bg-base-100", style="max-width:100vh;"
                        ),
                        # Questions list section - responsive grid layout with 3 columns max
                        Div(
                            *generate_question_cards(),  # Generates all question cards
                            cls="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"  # Responsive grid with 1, 2, or 3 columns
                        ),
                        cls="flex flex-col space-y-6"
                    ),
                    cls="container mx-auto py-8"
                )
            ), data_theme="retro"  # DaisyUI's retro theme
        )
    )





@rt('/questions/{section}/{num}/{answer}')
def get(section: str, num: int, answer: bool):
    question_obj = question_objects(section)[num]

    def hide_switch(input):
        return not input

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
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar-start"
                        ),
                        Div(
                            A("Tutors", href="/tutors", cls="btn rounded-full btn-sm btn-primary"),
                            A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn rounded-full btn-sm btn-secondary"),
                            cls="navbar-end space-x-2"
                        ),
                        cls="navbar bg-base-90 shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Card component for question display
                        Div(
                            Div(
                                H2(f"Question #{question_obj['id']}", cls="card-title text-2xl font-bold"),
                                P(question_obj['question'].get('paragraph', ""), cls="text-base mt-4"),
                                B(question_obj['question']['question'], cls="text-lg"),
                                Div(
                                    Div(B("A. "), question_obj['question']['choices']['A'], cls="py-2"),
                                    Div(B("B. "), question_obj['question']['choices']['B'], cls="py-2"),
                                    Div(B("C. "), question_obj['question']['choices']['C'], cls="py-2"),
                                    Div(B("D. "), question_obj['question']['choices']['D'], cls="py-2"),
                                    cls="mt-4"
                                ),
                                Div(
                                    A("Reveal Answer", href=f'/questions/{section}/{num}/{hide_switch(answer)}', cls="btn btn-primary text-sm"),
                                    A("Go Back", href=f'/explore/{section}/any', cls="btn btn-secondary text-sm ml-4"),
                                    cls="flex mt-4 space-x-4"
                                ),
                                Div(
                                    Br(),
                                    B(f"Correct Answer is: {question_obj['question']['correct_answer']}"),
                                    P(question_obj['question']['explanation']),
                                    hidden=bool(answer),
                                    cls="mt-4"
                                ),
                                cls="card-body"
                            ),
                            cls="card bg-base-100 shadow-lg mx-auto w-full max-w-2xl"
                        ),
                        cls="container mx-auto py-8 px-4"
                    )
                )
            ), data_theme="retro"
        )
    )


@rt("/tutors")
def get():
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
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar-start"
                        ),
                        Div(
                            A("Tutors", href="/tutors", cls="btn rounded-full btn-sm btn-primary"),
                            A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn rounded-full btn-sm btn-secondary"),
                            cls="navbar-end space-x-2"
                        ),
                        cls="navbar bg-base-90 shadow bg-ghost"
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
                                    cls="card bg-base-100 w-96 shadow-xl p-2"
                                ),
                                cls="max-w-sm mx-auto"
                            ) for doc in firestore_docs],
                        cls="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
                    ),
                    cls="container mx-auto py-6"
                )
            ), data_theme="retro"
        )
    )



@rt("/practice/explore")
def get():
    # Load modules from JSON file
    modules = json.load(open('data.json'))['practice_test']

    return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    Div(
                        A(
                            Span("🎓", style="font-size:1.8rem;"),
                            H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                            cls="btn btn-ghost normal-case text-xl", href="/"
                        ),
                        cls="navbar-start"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="navbar-end space-x-4"
                    ),
                    cls="navbar bg-base-100 shadow-lg w-full flex justify-between items-center px-6 py-4"
                ),
                Main(
                    Div(
                        # Loop through modules and create a card for each one
                        *[
                            Div(
                                A(
                                    Div("📚", cls="text-3xl"),  # Icon for each module
                                    H2(module['name'], cls="card-title text-lg font-bold mt-4"),  # Module name
                                    P("Practice Test", cls="text-primary"),
                                    cls="card bg-base-100 shadow-xl w-96 mx-auto hover:bg-base-200 transition-all rounded-lg p-8",
                                    href=f"/practice/{i}/module/1" 
                                )
                            )
                            for i, module in enumerate(modules)
                        ],
                        cls="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4"  # Responsive grid layout
                    ),
                    cls="container mx-auto py-8"
                )
            ), data_theme="retro"
        )
    )


@rt("/practice/{practice_num}/module/{module_number}")
def get(session, practice_num: int, module_number: int):
    # Load the current module and initialize session state
    module = f'module_{module_number}'
    
    if 'page' not in session or session['page'] is None:
        session['page'] = 0
    if module not in session or session[module] is None:
        session[module] = []

    # Load practice questions
    practice_en_questions = json.load(open('data.json'))['practice_test']
    
    # Get the current question object
    question_obj = question_objects('english' if module_number < 3 else 'english')[practice_en_questions[practice_num][module][session['page']]]

    # Helper to retrieve answers from session
    def answers_session(count):
        for answer in session[module]:
            if str(count) in answer:
                return answer[str(count)]

    # Button for navigating to the next page/module
    def module_switcher():
        if session['page'] < 53:
            return A("Next", hx_post=f'/next_page/{practice_num}/{module_number}', hx_swap="innerHTML", hx_target='#practice_html', cls="btn btn-primary rounded-full")
        elif module == "module_2":
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/break', cls="btn btn-secondary rounded-full")
        elif module == "module_4":
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/check', cls="btn btn-secondary rounded-full")
        else:
            session['page'] = 0
            return A("Finish", href=f'/practice/{practice_num}/module/{module_number + 1}', cls="btn btn-secondary rounded-full")

    # Timer time (optional)
    timer_time = 10

    # Function for radio options (answer selection)
    def practice_options(value: str):
        if answers_session(session['page']) == value:
            return Input(type="radio", name="answer", value=value, checked=True, cls="radio radio-primary")
        else:
            return Input(type="radio", name="answer", value=value, cls="radio radio-primary")

    return (
        Html(
            Head(Defaults),
            Body(
                Header(
                    Div(
                        Div(
                            A(
                                Span("🎓", style="font-size:1.8rem;"),
                                H1("OpenSAT", cls="text-primary"),
                                cls="btn rounded-full btn-ghost normal-case text-xl", href="/"
                            ),
                            cls="navbar-start"
                        ),
                        Div(
                            A("Tutors", href="/tutors", cls="btn rounded-full btn-sm btn-primary"),
                            A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn rounded-full btn-sm btn-secondary"),
                            cls="navbar-end space-x-2"
                        ),
                        cls="navbar bg-base-90 shadow bg-ghost"
                    )
                ),
                Main(
                    Div(
                        # Dropdown for page selection
                        Div(
                            Select(
                                *[Option(f"Page {i + 1}") for i, _ in enumerate(practice_en_questions[practice_num][module])],
                                cls="select select-bordered w-full max-w-xs mt-4 mx-auto"
                            ),
                            cls="mb-6"
                        ),
                        # Question content inside a DaisyUI card
                        Div(
                            Div(
                                P(question_obj['question'].get('paragraph', ""), cls="text-base mb-4"),
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
                                A("Back", hx_post=[f'/previous_page/{practice_num}/{module_number}' if session['page'] > 0 else None], hx_swap="innerHTML", hx_target='#practice_html', cls="btn btn-secondary rounded-full"),
                                H4(f"Page {session['page'] + 1}", cls="text-lg font-bold"),
                                module_switcher(),
                                cls="flex justify-between items-center mt-6 p-5"
                            )
                            ,
                            cls="card bg-base-100 shadow-xl w-full max-w-3xl mx-auto mt-8"
                        ),
                        # Navigation: Back, Page Number, Next/Finish
                       
                    ),
                    cls="container mx-auto py-8 px-4"
                ),
                id="practice_html"
            ),
            data_theme="retro"  # Retro theme enabled
        )
    )




@rt('/next_page/{practice}/{module_number}')
def post(session,practice:str,module_number:str):
 # Initialize module in the session if it doesn't exist or if it's None
    session.setdefault('page', 0)
    session['page'] = session.get('page') + 1
    return RedirectResponse(f'/practice/{practice}/module/{module_number}', status_code=303)

@rt('/previous_page/{practice}/{module_number}')
def post(session,practice:str,module_number:str):
 # Initialize module in the session if it doesn't exist or if it's None
    session.setdefault('page', 0)
    session['page'] = session.get('page') - 1
    return RedirectResponse(f'/practice/{practice}/module/{module_number}', status_code=303)


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
                        cls="card bg-base-100 w-96 shadow-xl mx-auto py-8"
                    )
                ),cls="flex items-center justify-center"
            ),data_theme="retro"
        )
    )


@rt("/practice/{practice_num}/check")
def get(practice_num:int,session):
 

 practice_en_questions = json.load(open('data.json'))['practice_test']

 
 def checker():
    correct_answers = []
    results = []
    def answer_collecter(num):
     for question_num in practice_en_questions[practice_num][f'module_{num}']:
      answer =  question_objects('english')[question_num]['question']['correct_answer']
      correct_answers.append(answer)

    for num in [1,2,3,4]:
     correct_answers.clear()
     user_answers = session[f'module_{num}']
     answer_collecter(num)
     # Comparison result list
     # Loop through each dictionary in the list
     for d in user_answers:
     # Extract the number (as string) and the expected string
      index_str, expected_value = list(d.items())[0]
      index = int(index_str)  # Convert index to integer

     # Check if the index is within the bounds of the list_of_values
      if 0 <= index < len(correct_answers):
        # Compare the value in list_of_values at index with expected_value
        if correct_answers[index] == expected_value:
            results.append(1)
        else:
            results.append(0)
      else:
        # If index is out of bounds, consider it a mismatch
        results.append(0)
     del session[f'module_{num}']
     session['page'] = 0       
    return sum(results)

    

 return (
        Html(
            Head(
                Defaults
            ),
            Body(
                Main(
                    Div(
                       
                        H2(f"Your Score is {checker()}/92",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("click continue to start the next module",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("End", href=f"/", cls="btn btn-primary"),
                            style="display:flex; justify-content:center;"
                            
                        ),
                        cls="card bg-base-100 w-96 shadow-xl mx-auto py-8"
                    )
                ),cls="flex items-center justify-center"
            ),data_theme="retro"
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



@rt("/time-sender/{time}")
async def get(session,time:int):
    # Total duration of the countdown (54 minutes)
    total_duration = timedelta(minutes=int(time))

    # Ensure the start time is in the session
    if 'start_time' not in session:
        session['start_time'] = datetime.now().isoformat()

    async def time_generator():
        while True:
            # Retrieve the start time from the session at the start of each iteration
            start_time = datetime.fromisoformat(session['start_time'])

            # Calculate the elapsed time
            elapsed_time = datetime.now() - start_time
            
            # Calculate the remaining time
            remaining_time = total_duration - elapsed_time
            
            if remaining_time.total_seconds() > 0:
                # Calculate minutes and seconds left
                minutes, seconds = divmod(remaining_time.total_seconds(), 60)
                time_str = f"{int(minutes):02d}:{int(seconds):02d}"
            else:
                # If time is up, reset the timer
                session['start_time'] = datetime.now().isoformat()
                start_time = datetime.fromisoformat(session['start_time'])
                time_str = "00:00"

            # Send the remaining time to all connected clients
            yield f"""event: TimeUpdateEvent\ndata: {to_xml(P(time_str, sse_swap="TimeUpdateEvent"))}\n\n"""

            # Use asyncio.sleep to keep the loop non-blocking
            await asyncio.sleep(1)

    try:
        # Start streaming the countdown timer
        return StreamingResponse(time_generator(), media_type="text/event-stream")
    except asyncio.CancelledError:
        # This block will be executed when the server is shutting down
        print("Timer stream was cancelled")

serve()
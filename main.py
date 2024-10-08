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
            Script(src="https://unpkg.com/htmx-ext-sse@2.2.1/sse.js"),
                Title("OpenSAT"),
                Style(open("main.css").read())
                
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
                    A(
                        Span("🎓", style="font-size:1.8rem;"),
                        H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                        cls="logo", href="/",style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(
                    Div(
                        Span("🎓", style="display: flex; font-size: 5rem; margin-bottom: 20px; justify-content: center;"),
                        H2("Question Bank with ", Span("Endless", cls="text-primary-500 decoration-wavy"), " Possibilities",
                           style="font-size: 2.25rem; font-weight: 700; text-align: center; margin-bottom: 20px; color: #333;"),
                        P("OpenSAT, a free and open-source SAT question bank. "
                          "Dive into a massive pool of SAT practice problems, "
                          "constantly growing thanks to a dedicated community of contributors.",
                          style="text-align: center; max-width: 36rem; margin: 0 auto 20px; color: #555; font-size: 1rem;"),
                        Div(
                            A("Explore", href="/explore/english/any", cls="btn btn-primary"),
                            A("Contribute", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                            style="display: flex; justify-content: center; gap: 15px;"
                            
                        ),
                        cls="container"
                    )
                )
            )
        )
    )


@rt("/explore/{section}/{domain}")
def get(section:str,domain:str):
 
 def domain_lower(input):
  return str(input).lower()
 
 def filter_switch():
   if section == 'english':
     return (  
     A("Information and Ideas", href=f'/explore/{section}/information and ideas',cls="btn btn-filter"),
     A("Craft and Structure", href=f'/explore/{section}/craft and structure',cls="btn btn-filter"),
     A("Expression of Ideas", href=f'/explore/{section}/expression of ideas',cls="btn btn-filter"),
     A("Standard English Conventions", href=f'/explore/{section}/standard english conventions',cls="btn btn-filter")
    )
   else:
     return (
     A("Algebra", href=f'/explore/{section}/algebra',cls="btn btn-filter"),
     A("Advanced Math", href=f'/explore/{section}/advanced math',cls="btn btn-filter"),
     A("Problem-Solving and Data Analysis", href=f'/explore/{section}/problem-solving and data analysis',cls="btn btn-filter"),
     A("Geometry and Trigonometry", href=f'/explore/{section}/geometry and trigonometry',cls="btn btn-filter")
    )
   
 return (
    
       Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    A(
                        Span("🎓", style="font-size:1.8rem;"),
                        H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                        cls="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(
                    Div(
                       Div(
                         H1("🔎 Filters"),
                         A("English", href=f'/explore/english/any',cls=["btn btn-primary" if section == 'english' else "btn btn-secondary"]),
                         A("Math", href=f'/explore/math/any',cls=["btn btn-primary" if section == 'math' else "btn btn-secondary"]),
                         Br(),
                         Br(),
                         Div(filter_switch()),
                        cls="filter-container"),
                        *[ A(Div("📚", cls="icon"), Div(f'Question #{i}', cls="question-number"), Div(x['domain'], cls="category"), cls="card", href=f"/questions/{section}/{i}/True" ) if domain.lower().replace('%20',' ') == 'any' or domain_lower(x['domain']) == domain.lower().replace('%20',' ') else Div('', hidden=True) for i, x in enumerate(question_objects(section)) ]
                        

                        ,cls="list-content"
                   )
                   ,Style="display:flex;"
                )
        )
) 

)



@rt('/questions/{section}/{num}/{answer}')
def get(section:str,num:int,answer:bool):
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
                    A(
                        Span("🎓", style="font-size:1.8rem;"),
                        H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                        cls="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(

                    Div(
                         
                        H2(f"Question #{question_obj['id']}"),
                        P(question_obj['question'].get('paragraph', "")),
                        B(question_obj['question']['question']),
                        
                        Div(B("A."), question_obj['question']['choices']['A']),
                        Div(B("B."), question_obj['question']['choices']['B']),
                        Div(B("C."), question_obj['question']['choices']['C']),
                        Div(B("D."), question_obj['question']['choices']['D']),
                        Br(),
                        A("Reveal Answers", href=f'/questions/{section}/{num}/{hide_switch(answer)}',cls="btn btn-primary", style="font-size:0.9em;"),
                        A("Go Back", href=f'/explore/{section}/any',cls="btn btn-secondary", style="font-size:0.9em;"),
                        Div(
                        Br(),
                        B(f"Correct Answer is: {question_obj['question']['correct_answer']}"),
                        P(question_obj['question']['explanation']), 
                         hidden=bool(answer)
                        )

                        ,cls="container",style="max-width:80vh;"
                   )
                   ,Style="display:flex;"
                )
        )
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
                    A(
                        Span("🎓", style="font-size:1.8rem;"),
                        H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                        cls="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(
                    Div(
                        #*[Div(doc.to_dict()['age'],cls="card") for doc in firestore_docs],

                       *[Div(Img(src=doc.to_dict()['banner'],cls="avatar"),Div(H3(doc.to_dict()['username']),P(doc.to_dict()['description'],cls="description"),P(doc.to_dict()['availability'],cls="status"),P(doc.to_dict()['email'],cls="email"),Div(doc.to_dict()['country'],cls="location"),cls="info"),Button(f"Contact: {doc.to_dict()['contact']}",cls="contact-btn"),cls="profile-card") for doc in firestore_docs]
                        

                        ,cls="list-content"
                   )
                   ,Style="display:flex;"
                )
        )
) 

)

@rt("/practice/explore")
def get():
 
 modules = json.load(open('data.json'))['practice_test']
 

 return (
    
       Html(
            Head(
                Defaults
            ),
            Body(
                Header(
                    A(
                        Span("🎓", style="font-size:1.8rem;"),
                        H1("OpenSAT", style="color: #fc9d9a; font-weight: 700;"),
                        cls="logo",href='/',style="text-decoration: none"
                    ),
                    Nav(
                        A("Tutors", href="/tutors", cls="btn btn-primary"),
                        A("Github", href="https://github.com/Anas099X/OpenSAT", cls="btn btn-secondary"),
                        cls="nav"
                    ),
                    cls="header"
                ),
                Main(
                    Div(

                        *[ A(Div("📚", cls="icon"), Div(module['name'], cls="question-number"), Div("Practice Test", cls="category"), cls="card", href=f"/practice/{i}/module/1") for i, module in enumerate(modules)]
                        

                        ,cls="list-content"
                   )
                   ,Style="display:flex;"
                )
        )
) 

)

@rt("/practice/{practice_num}/module/{module_number}")
def get(session,practice_num:int,module_number:int):
 #del session[module]
 # session['page'] = 50
 module = f'module_{module_number}'
 if 'page' not in session or session['page'] is None:
        session['page'] = 0
 if module not in session or session[module] is None:
        session[module] = []

 practice_en_questions = json.load(open('data.json'))['practice_test']
 
 question_obj = question_objects('english' if module_number < 3 else 'math')[practice_en_questions[practice_num][module][session['page']]]
 def answers_session(count):
  for answer in session[module]:
     if str(count) in answer:
      return answer[str(count)]
     
 def module_switcher():
  if session['page'] < 53:
     return A("Next", hx_post=f'/next_page/{practice_num}/{module_number}',hx_swap="innerHTML",hx_target='#practice_html',cls="btn btn-secondary", style="font-size:0.9em;")
  elif module == "module_2":
     session['page'] = 0
     return A("Finish", href=f'/practice/{practice_num}/break',cls="btn btn-secondary", style="font-size:0.9em;") 
  elif module == "module_4":
     session['page'] = 0
     return A("Finish", href=f'/practice/{practice_num}/check',cls="btn btn-secondary", style="font-size:0.9em;") 
  else:
     session['page'] = 0
     return A("Finish", href=f'/practice/{practice_num}/module/{module_number + 1}',cls="btn btn-secondary", style="font-size:0.9em;")
     
 
   
 timer_time = 10
   
 def practice_options(value:str):
    if answers_session(session['page']) == value:
     return Input(type="radio", name="answer", value=value, checked=True)
    else:
     return Input(type="radio", name="answer", value=value) 
   
 return (
    
   Html(
    Head(
        Defaults  # This would include meta tags, CSS links, etc.
    ),
    Body(
        Header(
            
                H3(session[module]),
                Div(  
                #A('',sse_swap="TimeUpdateEvent", hx_ext="sse", sse_connect=f"/time-sender/{timer_time}",cls="timer btn btn-secondary")
                )        
            ,
            cls="header",style="flex-direction: row; height:12vh;"
        ),
        Main(Select(*[Option(f"Page {i + 1} ") for i, module in enumerate(practice_en_questions[practice_num][module])]),
             Div(
                         
                        
                        P(question_obj['question'].get('paragraph', "")),
                        B(question_obj['question']['question']),
                        
                        Form(Label(
                            practice_options('A'),
                            Span(question_obj['question']['choices']['A']),
                            cls="option"
                        ),
                        Label(
                            practice_options('B'),
                            Span(question_obj['question']['choices']['B']),
                            cls="option"
                        ),
                        Label(
                            practice_options('C'),
                            Span(question_obj['question']['choices']['C']),
                            cls="option"
                        ),
                        Label(
                            practice_options('D'),
                            Span(question_obj['question']['choices']['D']),
                            cls="option"
                        ),
                        cls="options", hx_post=f"/page/{module}/{session['page']}", hx_trigger="change", hx_swap="none"),

                        Br(),
                        Div(
                        A("Back", hx_post=[f'/previous_page/{practice_num}/{module_number}' if session['page'] > 0 else None],hx_swap="innerHTML",hx_target='#practice_html',cls="btn btn-secondary", style="font-size:0.9em;"),
                        H4(session['page'] + 1),
                        module_switcher(),
                        style="display:flex; justify-content:space-between;"
                        ),
                        cls="practice-container"
                   )

                   ,Style="display:flex; margin-top:10vh;"
                )
,id="practice_html")
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
                            A("Continue", href=f"/{practice_num}/module/3", cls="btn btn-primary"),
                            style="display:flex; justify-content:center;"
                            
                        ),
                        cls="container"
                    )
                )
            )
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
                        cls="container"
                    )
                )
            )
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
from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from survey import satisfaction_survey






app=Flask(__name__)
app.config["SECRET_KEY"]="key"

debug=DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"]=False

responses=[]


@app.route("/")
def home_page():

    """Title of the survey and the instructions"""

    title=satisfaction_survey.title
    instructions=satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)

@app.route("/question/<int:num>", methods=["GET", "POST"])
def question_pages(num):

    """Page to dynamically send user to current questions. Keeps the user from trying to access questions out of order"""

    try:
        question=satisfaction_survey.questions[num].question
        answer=satisfaction_survey.questions[num].choices
    except:
        flash("Please answer current question before moving on")
        return redirect("/next_page")
    curr_page=len(responses)
    
    if num !=curr_page:
        flash("Please answer current question before moving on")
        return redirect("/next_page")

    return render_template(f"question_{num}.html", question=question, answer=answer)


@app.route("/set_session", methods=["GET", "POST"])
def set_session_data():
    """Sets session data to empty list when survey is started"""
    responses.clear()
    need_to_clear_session=session["responses"]
    
    need_to_clear_session.clear()
    print("************")
    print(need_to_clear_session)
    print("************")
    session["responses"]=need_to_clear_session
    return redirect("/next_page")


@app.route("/answers", methods=["GET","POST"])
def answers():

    """Page that contains answers. """

    total=len(responses)
    question_total=len(satisfaction_survey.questions)
    return render_template("answers.html", responses=responses, total=total, question_total=question_total)


@app.route("/next_page", methods=["GET", "POST"])
def next_page():
    """Next page in the survey. Dynamically chooses the next question to go to.
    If at the end of the survey, directs user to the thank you page"""
    session["responses"]=responses
    total=len(session["responses"])
    
    first=request.form.get(f"choice_{total}_0")
    second=request.form.get(f"choice_{total}_1")
    choices=[first,second]
    for i in choices:
        if i!= None:
            responses.append(i)
    
   
    question_total=len(satisfaction_survey.questions)
    if total == question_total:
        return redirect("/thank_you")
    
    return redirect(f"/question/{total}")

@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")


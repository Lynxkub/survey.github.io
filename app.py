from flask import Flask, render_template, request, redirect, flash
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


# @app.route("/question/0", methods=["GET", "POST"])
# def question_zero():

#     """First question of survey"""

#     q_zero=satisfaction_survey.questions[0].question
#     a_zero=satisfaction_survey.questions[0].choices
#     return render_template("question_0.html", q_zero=q_zero, a_zero=a_zero)


# @app.route("/question/1",methods=["GET","POST"])
# def question_one():

#     """Second question of survey"""

#     q_one=satisfaction_survey.questions[1].question
#     a_one=satisfaction_survey.questions[1].choices

    
    
#     return render_template("question_1.html", q_one=q_one, a_one=a_one)

# @app.route("/question/2", methods=["GET","POST"])
# def question_two():

#     """Third question of survey"""
   
#     q_two=satisfaction_survey.questions[2].question
#     a_two=satisfaction_survey.questions[2].choices

 

#     return render_template("question_2.html", q_two=q_two, a_two=a_two)

# @app.route("/question/3", methods=["GET","POST"])
# def question_three():

#     """Fourth (last) question of survey"""

#     q_three=satisfaction_survey.questions[3].question
#     a_three=satisfaction_survey.questions[3].choices

   

#     return render_template("question_3.html", q_three=q_three, a_three=a_three)


@app.route("/question/<int:num>", methods=["GET", "POST"])
def question_pages(num):
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

@app.route("/answers", methods=["GET","POST"])
def answers():

    """Page that contains answers. Will remove once I can get answers to be captured successfully
    
    On step 5 in project. Change answers page to be a Thank User page?? But do it dynamically??(Add logic to each page to loop through the origional class to see if there are more questions)(or comparing the number of responses in responses list to the page number. Should be last index of responses +1 for correct page)
    
    
    """
   
  

    total=len(responses)
    question_total=len(satisfaction_survey.questions)
    return render_template("answers.html", responses=responses, total=total, question_total=question_total)


@app.route("/next_page", methods=["GET", "POST"])
def next_page():
    """Next page in the survey. Dynamically chooses the next question to go to.
    If at the end of the survey, directs user to the thank you page"""
    total=len(responses)

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
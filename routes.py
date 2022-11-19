import python_sdk.strike as strike #For timebeing, strike is a private library. Has to be downloaded into the local from https://github.com/Strike-official/python-sdk 
import config
import flask
import requests
from flask import jsonify
from flask import request
import sql

app = flask.Flask(__name__)
app.config["DEBUG"] = True


baseAPI=config.baseAPI

@app.route('/foodTrackBot/get/expense', methods=['POST'])
def get_location_for_booking():
    strikeObj = strike.Create("foodTrackBot",baseAPI+"/foodTrackBot/set/expense")
    quesObj1 = strikeObj.Question("shashank_dish").\
                QuestionText().\
                SetTextToQuestion("What was the order for Shashank?")
    quesObj1.Answer(False).TextInput()

    quesObj2 = strikeObj.Question("shashank_cost").\
                QuestionText().\
                SetTextToQuestion("How much Shashank's order cost in ₹?")
    quesObj2.Answer(False).NumberInput()

    quesObj3 = strikeObj.Question("sayak_dish").\
                QuestionText().\
                SetTextToQuestion("What was the order for Sayak?")
    quesObj3.Answer(False).TextInput()

    quesObj4 = strikeObj.Question("sayak_cost").\
                QuestionText().\
                SetTextToQuestion("How much Sayak's order cost in ₹?")
    quesObj4.Answer(False).NumberInput()

    quesObj5 = strikeObj.Question("who_paid").\
                QuestionText().\
                SetTextToQuestion("Who paid for this?")
    answer_card = quesObj5.Answer(False).AnswerCardArray(strike.HORIZONTAL_ORIENTATION)
    answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"Sayak", "#074d69",True)

    answer_card = answer_card.AnswerCard().\
            SetHeaderToAnswer(1,"WRAP").\
            AddTextRowToAnswer(strike.H4,"Shashank", "#074d69",True)
    
    return jsonify(strikeObj.Data())

@app.route('/foodTrackBot/set/expense', methods=['POST'])
def respondBack():
    data = request.get_json()
    print(data)
    user_id = data["bybrisk_session_variables"]["userId"]
    shashank_dish = data["user_session_variables"]["shashank_dish"]
    shashank_cost = data["user_session_variables"]["shashank_cost"]
    sayak_dish = data["user_session_variables"]["sayak_dish"]
    sayak_cost = data["user_session_variables"]["sayak_cost"]
    who_paid = data["user_session_variables"]["who_paid"][0]


    ## Save to DB
    sql.add_food_expense(user_id,shashank_dish,sayak_dish,shashank_cost,sayak_cost,who_paid)

    strikeObj = strike.Create("foodTrackBot","")
    question_card = strikeObj.Question("").\
            QuestionCard().\
            SetHeaderToQuestion(11,strike.HALF_WIDTH).\
            AddGraphicRowToQuestion(strike.PICTURE_ROW,["https://media.istockphoto.com/id/474551486/photo/3d-white-man-with-green-tick.jpg?s=612x612&w=0&k=20&c=aiPfi5CiH8Ru4jGy29Z4O_X9rDrykS5CanfoWtt0dRI="],[""]).\
            AddTextRowToQuestion(strike.H4,"The expense has been recorded","#074d69",False)

    return jsonify(strikeObj.Data())

app.run(host='0.0.0.0', port=config.port)
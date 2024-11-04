from flask import Flask, render_template, request, redirect
from flask_login import LoginManager,login_user,logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from models import Roster, Cadet, Score, User
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
correct_user = "rotc342"
correct_password = "test2"
app.secret_key = "asdlfjsadfdasfas34252354"



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/", methods=['POST','GET'])
def login():
    users = User()
    db.session.add(users)
    db.session.commit()
    if request.method == 'POST':
        username = request.form['Username']
        password = request.form["Password"]
        ob = db.session.query(User).first()
        if((username == correct_user) and (password==correct_password)):
            login_user(ob)
            return redirect('/dashboard')
        else:
            return redirect('/')
    else:
        return render_template('login.html')
@app.route("/dashboard")
def dash():
    if not current_user.is_authenticated:
        return redirect("/")
    return render_template('Dashboard.html')
@app.route("/rosterlist/<string:flight>")
def rosterlist(flight):
    if not current_user.is_authenticated:
        return redirect("/")
    roster = db.session.query(Roster).filter_by(flight_name = flight).first()

    return render_template("rosterList.html", roster = roster.cadets_last.split(","))
@app.route("/rosters")
def rost():
    if not current_user.is_authenticated:
        return redirect("/")
    rosters = db.session.query(Roster).all()
    return render_template("roster.html", rosters=rosters)
@app.route("/add-flight",methods=["POST","GET"])
def addFlight():
    if not current_user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        firstNames = request.form["firstNames"].split(",")
        firstNames.pop(len(firstNames)-1)
        lastNames = request.form["lastNames"].split(",")
        lastNames.pop(len(lastNames)-1)
        flightName = request.form["flightName"]
        cadets_id = ""
        
        flight_exists = db.session.query(Roster).filter_by(flight_name=flightName).first() is not None
        if(flight_exists):
            return render_template("Error.html", error= "ERROR: flight:"+ flightName + " already exists",dir="/add-flight" )
    
        for i in range(len(firstNames)):
            exists = db.session.query(Cadet).filter_by(name=firstNames[i] + "," + lastNames[i]).first() is not None
            if(exists):
                cadet = db.session.query(Cadet).filter_by(name=firstNames[i] + "," + lastNames[i]).first() 
                if(cadet.flight_name != "N/A"):
                    if(cadets_id != ""):
                        for id in cadets_id[:-1].split(","):
                            cadet_NA = db.session.query(Cadet).filter_by(id = int(id)).first()
                            cadet_NA.flight_name = "N/A"
                            db.session.commit()
                    #make it so when error happens it auto refills cadet list created prior to submission
                    return render_template("Error.html", error="ERROR: Cadet: " + cadet.name + " is already in a flight", dir="/add-flight")
                else:
                    cadet.flight_name = flightName
                    db.session.commit()
                    cadets_id = cadets_id + str(cadet.id) + ","
            else:
                newCadet = Cadet(name = firstNames[i] + "," + lastNames[i], flight_name = flightName)
                db.session.add(newCadet)
                db.session.commit()
                cadets_id = cadets_id + str(db.session.query(Cadet).order_by(Cadet.id.desc()).first().id) + ","
        newFlight = Roster(cadets_id=cadets_id[:-1], flight_name = flightName, cadets_last = request.form["lastNames"][:-1], cadets_first=request.form["firstNames"][:-1] )
        db.session.add(newFlight)
        db.session.commit()
        return redirect("/rosters")

    return render_template("add-flight.html")
@app.route("/edit-flight/<string:flight>", methods=["POST","GET"])
def editFlight(flight):
    if not current_user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        firstNames = request.form["firstNames"].split(",")
        firstNames.pop(len(firstNames)-1)
        lastNames = request.form["lastNames"].split(",")
        lastNames.pop(len(lastNames)-1)
        flightName = request.form["flightName"]
        cadets_id = ""
        flight_ob = db.session.query(Roster).filter_by(flight_name=flightName).first()
        cadets_last_backup =flight_ob.cadets_last
        cadets_first_backup=flight_ob.cadets_first
        cadets_id_backup=flight_ob.cadets_id
        print(flight_ob.cadets_id.split(","))
        for id in flight_ob.cadets_id.split(","):
            if(id != ""):
                cad = db.session.query(Cadet).filter_by(id=int(id)).first()
                print(cad.name)
                cad.flight_name = "N/A"
                db.session.commit()
        db.session.commit()
        for i in range(len(firstNames)):
            exists = db.session.query(Cadet).filter_by(name=firstNames[i] + "," + lastNames[i]).first() is not None
            if(exists):
                cadet = db.session.query(Cadet).filter_by(name=firstNames[i] + "," + lastNames[i]).first() 
                if(cadet.flight_name != "N/A" and cadet.flight_name != flightName):
                    if(cadets_id != ""):
                        for id in cadets_id[:-1].split(","):
                            cadet_NA = db.session.query(Cadet).filter_by(id = int(id)).first()
                            cadet_NA.flight_name = "N/A"
                            db.session.commit()
                    for id in flight_ob.cadets_id.split(","):
                        if(cadets_id != ""):
                            cad = db.session.query(Cadet).filter_by(id=int(id)).first()
                            cad.flight_name = flightName
                            db.session.commit()        
                    return render_template("Error.html", error="ERROR: Cadet: " + cadet.name + " is already in a flight ", dir="/edit-flight/" + flight)
                else:
                    cadet.flight_name = flightName
                    db.session.commit()
                    cadets_id = cadets_id + str(cadet.id) + ","
            else:
                newCadet = Cadet(name = firstNames[i] + "," + lastNames[i], flight_name = flightName)
                db.session.add(newCadet)
                db.session.commit()
                cadets_id = cadets_id + str(db.session.query(Cadet).order_by(Cadet.id.desc()).first().id) + ","
        newFlight = db.session.query(Roster).filter_by(flight_name=flightName).first()
        newFlight.cadets_id=cadets_id[:-1]
        newFlight.cadets_last = request.form["lastNames"][:-1]
        newFlight.cadets_first=request.form["firstNames"][:-1]

        db.session.commit()
        return redirect("/rosters")
    flight = db.session.query(Roster).filter_by(flight_name=flight).first()
    return render_template("edit-flight.html", flight=flight, cadets_first=flight.cadets_first.split(","))
@app.route("/deleteFlight", methods=["GET","POST"])
def delFlight():
    if not current_user.is_authenticated:
        return redirect("/")
    #make everyone in flight 
    if request.method == "POST":
        flightName = request.form["flightName"]
        flight = db.session.query(Roster).filter_by(flight_name=flightName).first()
        for id in flight.cadets_id.split(","):
            cadet = db.session.query(Cadet).filter_by(id = int(id)).first()
            cadet.flight_name = "N/A"
            db.session.commit()
        db.session.delete(flight)
        db.session.commit()
    return redirect("/rosters")
@app.route("/score-input")
def scoring():
    if not current_user.is_authenticated:
        return redirect("/")
    rosters = db.session.query(Roster).all()
    return render_template("flight-direct.html", rosters = rosters)
@app.route("/score-input/<string:flight>", methods=["POST", "GET"])
def scoreInput(flight):
    if not current_user.is_authenticated:
        return redirect("/")
    idIndex = 0
    uniformIndex = 1
    ptIndex = 2
    mbcIndex = 3
    dateIndex = 4
    # what if date given, but no data
    if request.method == "POST":
        data = request.form["data"]
        data = data.split(",")
        #print(data)
        for cadet in range(len(data)):
            cadet_data = data[cadet].split("+")
            if(cadet_data[dateIndex] == "N/A"):
                pass # does nothing
            else:
                date = cadet_data[dateIndex].split("-")
                
                if(date[1][0]=="0"): date[1] = date[1][1:]
                if(date[2][0]=="0"): date[2] = date[2][1:]
                print(date)
                if( cadet_data[uniformIndex] != "N/A"):
                    exists = db.session.query(Score).filter_by(score_type="U",cadet_id = cadet_data[idIndex],date = datetime.datetime(
                        int(date[0]),
                        int(date[1]),
                        int(date[2])
                    )).first() is not None
                    if(exists):
                        print("delete")
                        db.session.delete( db.session.query(Score).filter_by(score_type="U",cadet_id = cadet_data[idIndex],date = datetime.datetime(
                            int(date[0]),
                            int(date[1]),
                            int(date[2])
                        )).first())
                        db.session.commit()
                    new_score = Score(score_type="U",cadet_id = cadet_data[idIndex], score_value= int(cadet_data[uniformIndex]),date = datetime.datetime(
                        int(date[0]),
                        int(date[1]),
                        int(date[2])
                    ))
                    db.session.add(new_score)
                    db.session.commit()
                if( cadet_data[ptIndex] != "N/A"):
                    exists = db.session.query(Score).filter_by(score_type="P",cadet_id = cadet_data[idIndex],date = datetime.datetime(
                        int(date[0]),
                        int(date[1]),
                        int(date[2])
                    )).first() is not None
                    if(exists):
                        db.session.delete( db.session.query(Score).filter_by(score_type="P",cadet_id = cadet_data[idIndex],date = datetime.datetime(
                            int(date[0]),
                            int(date[1]),
                            int(date[2])
                        )).first())
                        db.session.commit()
                    new_score = Score(score_type="P",cadet_id = cadet_data[idIndex], score_value= int(cadet_data[ptIndex]),date = datetime.datetime(
                        int(date[0]),
                        int(date[1]),
                        int(date[2])
                    ))
                    db.session.add(new_score)
                    db.session.commit()
                    
                if( cadet_data[mbcIndex] != "N/A"):
                    exists = db.session.query(Score).filter_by(score_type="M",cadet_id = cadet_data[idIndex],date = datetime.datetime(
                        int(date[0]),
                        int(date[1]),
                        int(date[2])
                    )).first() is not None
                    if(exists):
                        db.session.delete( db.session.query(Score).filter_by(score_type="M",cadet_id = cadet_data[idIndex],date = datetime.datetime(
                            int(date[0]),
                            int(date[1]),
                            int(date[2])
                        )).first())
                        db.session.commit()
                    
                    new_score = Score(score_type="M",cadet_id = cadet_data[idIndex], score_value= int(cadet_data[mbcIndex]),date = datetime.datetime(
                        int(date[0]),
                        int(date[1]),
                        int(date[2])
                    ))
                    db.session.add(new_score)
                    db.session.commit()
        return redirect("/score-input/" + flight)
    flight = db.session.query(Roster).filter_by(flight_name=flight).first()
    length = len(flight.cadets_first.split(","))
    cadets_last = flight.cadets_last.split(",")
    cadets_first = flight.cadets_first.split(",")
    return render_template("score-input.html",flight=flight, length=length, cadets_last=cadets_last, cadets_first=cadets_first )
@app.route("/scoreboard")
def scoreBoard():
    return render_template("Scoreboard.html")

def merge(list1, list2):
 
    merged_list = [[list1[i], list2[i]] for i in range(0, len(list1))]
     
    return merged_list

@app.route("/scoring-system/<string:type>")
def scoreSystem(type):
    flights = None
    type = type.split("+")
    group = type[0] # 2
    score_type = type[1] # 2
    start_date = type[2]
    end_date = type[3]
    if(start_date != "all" and end_date != "all"):
        start_date = type[2].split("-") # 2
        end_date = type[3].split("-")
        if(start_date[1][0]=="0"): start_date[1] = start_date[1][1:]
        if(start_date[2][0]=="0"): start_date[2] = start_date[2][1:]
        if(end_date[1][0]=="0"): end_date[1] = end_date[1][1:]
        if(end_date[2][0]=="0"): end_date[2] = end_date[2][1:]
        start_date = datetime.datetime(int(start_date[0]),int(start_date[1]),int(start_date[2]))
        end_date = datetime.datetime(int(end_date[0]),int(end_date[1]),int(end_date[2]))
    final_data = ""
    flight_names =[]
    cadet_names=[] # have to make system find average of cadets
    filtered_flight_Data = []
    filtered_cadet_Data = []
    data = db.session.query(Score).order_by(Score.score_value.desc()).all()
    for score in data:
        date_verification = False
        score_type_verification = False
        group_type_verification = True
        if(start_date == "all" or end_date == "all"):
            date_verification = True
        elif(start_date <= score.date and end_date >= score.date ):
            date_verification = True
        
        
        if(score_type==score.score_type):
            score_type_verification= True
        elif(score_type=="all"):
            #print("all")
            score_type_verification =True
        if(date_verification and score_type_verification):
            #print("verified")
            if(group=="Cadet"):
                #filtered_cadet_Data.append(score)
                cadet = db.session.query(Cadet).filter_by(id=int(score.cadet_id)).first().name
                flight = db.session.query(Cadet).filter_by(id=int(score.cadet_id)).first().flight_name
                if cadet in cadet_names:
                    #print(filtered_cadet_Data)
                    filtered_cadet_Data[cadet_names.index(cadet)].append(score)
                else:
                    if(flight!="N/A"):
                        cadet_names.append(cadet)
                        filtered_cadet_Data.append([])
                        filtered_cadet_Data[cadet_names.index(cadet)].append(score)
            else:
                flight = db.session.query(Cadet).filter_by(id=int(score.cadet_id)).first().flight_name
                if flight in flight_names:
                    filtered_flight_Data[flight_names.index(flight)].append(score)
                else:
                    if(flight!="N/A"):
                        flight_names.append(flight)
                        filtered_flight_Data.append([])
                        filtered_flight_Data[flight_names.index(flight)].append(score) #untested

    cadet_scores=[]
    flight_scores=[]
    flight_group = False
    merged_list = None
    if group == "Flight":
        flight_group = True
        for i in range(len(filtered_flight_Data)):
            denominator_value = 0
            numerator_value = 0
            for x in range(len(filtered_flight_Data[i])):
                denominator_value+=1
                #print(filtered_flight_Data[i][x].score_value)
                numerator_value+= filtered_flight_Data[i][x].score_value
    
            if denominator_value>0: flight_scores.append(round(numerator_value/denominator_value,2))
        merged_list = merge(flight_scores,flight_names)
        merged_list.sort(key=lambda merged_list: merged_list[0], reverse=True)
    else:
        for i in range(len(filtered_cadet_Data)):
            denominator_value = 0
            numerator_value = 0
            for x in range(len(filtered_cadet_Data[i])):
                denominator_value+=1
                #print(filtered_flight_Data[i][x].score_value)
                numerator_value+= filtered_cadet_Data[i][x].score_value
            #only do if denominator greater than 0

            if denominator_value>0: cadet_scores.append(round(numerator_value/denominator_value,2))
        merged_list = merge(cadet_scores,cadet_names)
        merged_list.sort(key=lambda merged_list: merged_list[0], reverse=True)
            

    
    return render_template("scoringBack.html", flights = flights, cadet_data = merged_list,flight_group=flight_group, flight_data = merged_list,
                           lengthF=len(flight_scores),
                           lengthC=len(cadet_scores))
if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=3000)
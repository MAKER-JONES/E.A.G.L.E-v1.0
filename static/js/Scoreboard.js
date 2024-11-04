function search(){
    board = document.getElementById("board")
    group_type = document.getElementById("group_type").value
    score_type = document.getElementById("score_type").value
    start_date = document.getElementById("start_date").value
    if(start_date==""){ start_date="all"}
    end_date = document.getElementById("end_date").value
    if(end_date==""){ end_date="all"}
    board.src = "/scoring-system/" + group_type + "+" + score_type + "+" + start_date + "+"  + end_date
}
let board;
let bluePlayerLocation = [0,0];
let redPlayerLocation = [0,0];
let csrf_token = $("[name=csrfmiddlewaretoken]")[0].defaultValue;
function drawboard(){
    board = []
    let canevas = document.getElementById("canevas");
    let table = document.createElement("table")
    for(let i = 0; i < 8; i++){
        let row = document.createElement("tr");
        board[i] = []
        for(let j = 0; j < 8; j++){
            let cell = document.createElement("td");
            row.append(cell);
            board[i][j] = cell;
        }
        table.append(row);
    }
    canevas.append(table);
}

function setup(){
    //board[0][0].classList.add("bleu");
    //board[7][7].classList.add("rouge");
    document.addEventListener("keypress", movePlayer)
}

function movePlayer(e){
    switch (e.charCode){
        case 122 :
            bluePlayerLocation[0]--;
            break;
        case 113 :
            bluePlayerLocation[1]--;
            break;
        case 115 :
            bluePlayerLocation[0]++;
            break;
        case 100 :
            bluePlayerLocation[1]++;
            break;
        default :
            console.log("invalid key");
            break;
    }
    board[bluePlayerLocation[0]][bluePlayerLocation[1]].classList.add("bleu");
    if(touchSide(bluePlayerLocation)){
        colorZone()
    }
}


function main(){
    let board_string = $("#board").attr("value")

    console.log(board_string)
    drawboard();
    setup();
    for (let s in board_string) {
        
        i = Math.floor(s/8)
        j = s % 8
        console.log("s : ", s, " i : ", i, " j : ", j)
        if (board_string[s] == "1") {
            board[i][j].classList.add("bleu") 
        } else if (board_string[s] == "2") {
            board[i][j].classList.add("rouge")
        }
    }
}



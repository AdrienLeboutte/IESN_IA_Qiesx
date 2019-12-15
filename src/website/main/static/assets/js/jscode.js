let board;
let bluePlayerLocation = [0,0];
let redPlayerLocation = [0,0];
let csrf_token = $("[name=csrfmiddlewaretoken]")[0].defaultValue;
let game_socket;
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
    switch (e.code){
        case "KeyW" :
            game_socket.send(JSON.stringify({direction:"up"}))
            break;
        case "KeyS" :
            game_socket.send(JSON.stringify({direction:"down"}))
            break;
        case "KeyA" :
            game_socket.send(JSON.stringify({direction:"left"}))
            break;
        case "KeyD" :
            game_socket.send(JSON.stringify({direction:"right"}))
            break;
        default :
            console.log("invalid key");
            break;
    }
}


function main(){
    let board_string = $("#board").attr("value")
    let game_id = $("#game_id").attr("value")
    console.log(board_string)
    console.log(game_id)
    drawboard();
    setup();
    for (let s in board_string) {
        
        i = Math.floor(s/8)
        j = s % 8
        if (board_string[s] == "1") {
            board[i][j].classList.add("bleu") 
        } else if (board_string[s] == "2") {
            board[i][j].classList.add("rouge")
        }
    }
    game_socket = new WebSocket(`ws://localhost:8000/ws/game/${game_id}/`)
    game_socket.onmessage = function(e) {
        data = JSON.parse(e.data)
        board_string = data["board"]
        console.log(data)
        console.log(data["player_positions"]);
        pos = data["player_positions"];
        $('.bleu_player').removeClass("bleu_player")
        $('.rouge_player').removeClass("rouge_player")
        for (let s in board_string) {
            i = Math.floor(s/8)
            j = s % 8
            if (board_string[s] == "1") {
                board[i][j].classList.add("bleu") 
            } else if (board_string[s] == "2") {
                board[i][j].classList.add("rouge")
            }
        }
        board[pos[0][1]][pos[0][0]].classList.add("bleu_player")
        board[pos[1][1]][pos[1][0]].classList.add("rouge_player")
    }
    
    
}



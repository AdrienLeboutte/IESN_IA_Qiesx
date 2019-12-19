let board;
let bluePlayerLocation = [0,0];
let redPlayerLocation = [0,0];
let csrf_token = $("[name=csrfmiddlewaretoken]")[0].defaultValue;
let game_socket;
const GAME_SIZE = 4;
function drawboard(){
    board = []
    let canevas = document.getElementById("canevas");
    let table = document.createElement("table")
    for(let i = 0; i < GAME_SIZE; i++){
        let row = document.createElement("tr");
        board[i] = []
        for(let j = 0; j < GAME_SIZE; j++){
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
    drawFromString(board_string);
    host_path = `${window.location.hostname}:${window.location.port}`
    game_socket = new WebSocket(`ws://${host_path}/ws/game/${game_id}/`);
    game_socket.onmessage = socketMessage;  
}

function drawFromString(board_string) {
    for (let s in board_string) {
        i = Math.floor(s/GAME_SIZE)
        j = s % GAME_SIZE
        if (board_string[s] == "1") {
            board[i][j].classList.add("bleu");
        } else if (board_string[s] == "2") {
            board[i][j].classList.add("rouge");
        }
    }
}

function socketMessage(e) {
    data = JSON.parse(e.data)
    console.log(data)
    board_string = data["board"];
    pos = data["player_positions"];
    $('.bleu_player').removeClass("bleu_player");
    $('.rouge_player').removeClass("rouge_player");
    drawFromString(board_string)
    board[pos[0][1]][pos[0][0]].classList.add("bleu_player");
    board[pos[1][1]][pos[1][0]].classList.add("rouge_player");
    if (data["status"] == "2") {
        console.log("Winner test")
        $('#infos').html(`
            <div class="alert alert-success" role="alert">
                <p>GAME IS OVER!</p>
            </div>
        `);
    }   
}



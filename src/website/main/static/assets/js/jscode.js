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
    board[0][0].classList.add("bleu");
    board[7][7].classList.add("rouge");
    document.addEventListener("keypress", movePlayer)
}

function movePlayer(e){
    switch (e.charCode){
        case 122 :
            send_direction("up");
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

function touchSide(coord){
    return coord[0] === 0 || coord[0] === 7 || coord[1] === 0 || coord[1] === 7;
}

function send_direction(direction) {
    $.post('/send_direction/', {"game_id":game_id, 
                                "direction": direction,
                                "csrfmiddlewaretoken":csrf_token
                            }, 
    (response) =>{
        console.log(response);
    });
}

function main(){
    drawboard();
    setup();
    $.getJSON("/get_game_state/" + game_id, (data) => {
        console.log(data);
        console.log($("#game_state"));
        $("#game_state").text(data['game_state']);
    });
}
href_array = window.location.href.split('/');
game_id = href_array[href_array.length - 1];
console.log(game_id);



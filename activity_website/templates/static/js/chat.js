//send message
function sendMessage(message) {
    if (message != "") {
        var row = document.createElement("DIV");
        row.className = "row";
        var box = document.createElement("DIV");
        box.className = "message_send";
        box.innerHTML = message;
        row.appendChild(box);
        $('#chatbox').append(row);
        $('#chatbox').scrollTop = $('#chatbox').scrollHeight;
    }
};

//get message
function getMessage(message) {
    if (message != "") {
        var row = document.createElement("DIV");
        row.className = "row";
        var box = document.createElement("DIV");
        box.className = "message_get";
        box.innerHTML = message;
        row.appendChild(box);
        $('#chatbox').append(row);
        $('#chatbox').scrollTop = $('#chatbox').scrollHeight;
    }
};
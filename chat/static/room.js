console.log("Sanity check from room.js.");


let chatLog = document.querySelector("#chatLog");
let chatMessageInput = document.querySelector("#chatMessageInput");
let chatMessageSend = document.querySelector("#chatMessageSend");
let onlineUsersSelector = document.querySelector("#onlineUsersSelector");

// adds a new option to 'onlineUsersSelector'
function onlineUsersSelectorAdd(value) {
    if (document.querySelector("option[value='" + value + "']")) return;
    let newOption = document.createElement("option");
    newOption.value = value;
    newOption.innerHTML = value;
    onlineUsersSelector.appendChild(newOption);
}

// removes an option from 'onlineUsersSelector'
function onlineUsersSelectorRemove(value) {
    let oldOption = document.querySelector("option[value='" + value + "']");
    if (oldOption !== null) oldOption.remove();
}

// focus 'chatMessageInput' when user opens the page
chatMessageInput.focus();

// submit if the user presses the enter key
chatMessageInput.onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter key
        chatMessageSend.click();
    }
};

// clear the 'chatMessageInput' and forward the message
chatMessageSend.onclick = function() {
    if (chatMessageInput.value.length === 0) return;
    chatSocket.send(JSON.stringify({
        "message": chatMessageInput.value,
    }));
    chatMessageInput.value = "";
};

function changeStatus(){
	document.getElementById("status_form").submit()
	if( chatSocket != null ){
		console.log('Closing Connections')
		chatSocket.close();
	}
}

// initial connect 

function getroom() {
    fetch('get_room/', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({}),
        cache: 'default'
    })
    .then(response => {
        // handle response
        console.log('response:', response);
        return response.json();  // convert response to JSON
    })
    .then(data => {
        // handle data
        console.log('data:', data);
        if( data['valid'] == true  ){
		    // call connect(_
			console.log('connected called')
			// show information 
			const username = data.details.userinfo.username;
			const gender = data.details.userinfo.gender;
			const country = data.details.userinfo.country;
			const userinfoText = `Connected <br> Username: ${username} | Gender: ${gender} | Country: ${country}`;
			document.getElementById('userinfo').innerHTML  = userinfoText;
			
			connect(data['details']['room_name'])
        }
    })
    .catch(error => {
        console.log('error happened:', error);
    });
};

if( 'true' == document.getElementById('statuss').text ){
	getroom();
}


window.addEventListener('unload', function(event) {
    // Set the user status to offline
    var xhr = new XMLHttpRequest();
    xhr.open('POST', 'set_user_offline/', true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhr.send();

    // Note: The XHR request is asynchronous and may not complete before the page is unloaded.
});



let chatSocket = null;
function connect(room) {
	console.log("Room",room);
    chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + room + "/");

    chatSocket.onopen = function(e) {
        console.log("Successfully connected to the WebSocket." );
		// not past 10 msgs if exists 
		
    }

    chatSocket.onclose = function(e) {
        console.log("WebSocket connection closed unexpectedly. Trying to reconnect in 2s...");
        setTimeout(function() {
            console.log("Reconnecting...");
            connect();
        }, 2000);
    };

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        console.log("OnMessage:",data);

        switch (data.type) {
			case "initial_msgs":
				for ( let i = 0 ; i < data.msgs.length ; i++){
					chatLog.value += data.msgs[i].user + ":" + data.msgs[i].msg + "\n";	
				}
				break;
            case "chat_message":
                chatLog.value += data.user + ": " + data.message + "\n";
                break;
            default:
                console.error("Unknown message type!");
                break;
        }

        // scroll 'chatLog' to the bottom
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    chatSocket.onerror = function(err) {
        console.log("WebSocket encountered an error: " + err.message);
        console.log("Closing the socket.");
        chatSocket.close();
    }
}



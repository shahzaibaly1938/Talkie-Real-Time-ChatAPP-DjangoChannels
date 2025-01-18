// Variables

const chatRoom = document.querySelector('#room_uuid').textContent.trim().replace(/"/g, '');

let chatSocket = null;
console.log('chatRoom: ',chatRoom)
// Chat Elements

const chatLogElement = document.querySelector('#chat_log');
const chatInputElement = document.querySelector('#chat_message_input');
const chatSubmitElement = document.querySelector('#chat_message_submit');


// Functions

function onChatMessage(data){
    console.log("OnChatMessage", data);

    if (data.type == 'chat_message'){
        if (!data.agent){

            chatLogElement.innerHTML += `<div class="flex w-full mt-2 space-x-3 max-w-md">

              <div class="flex-shrink-0 h-10 w-10 text-lg rounded-full bg-gray-300 flex items-center justify-center text-gray-800">${data.initials}</div>
            
            <div>
            <div class="bg-gray-300 p-3 rounded-l-lg rounded-br-lg ">
            <p class="text-sm">${data.message}</p>
            </div>
            <span class=" text-gray-500 mt-4 leading-none">${data.created_at} ago</span>
            </div>
          
            </div>`

        } else {
         
            chatLogElement.innerHTML += `<div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
            
            <div>
            <div class="bg-blue-300 p-3 rounded-l-lg rounded-br-lg ">
            <p class="text-sm">${data.message}</p>
            </div>
            <span class=" text-gray-500 mt-4 leading-none">${data.created_at} ago</span>
            </div>
            <div class="flex-shrink-0 h-10 w-10 text-lg rounded-full bg-gray-300 flex items-center justify-center text-gray-800">${data.initials}</div>
            </div>`
        }
    }

}


function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message' : chatInputElement.value,
        'name' : document.querySelector('#user_name').textContent.replaceAll('"',''),
        'agent' : document.querySelector('#user_id').textContent.replaceAll('"',''),
    }))

    chatInputElement.value = '';
}





// WebSocket
const room = encodeURIComponent(chatRoom)
chatSocket = new WebSocket(`ws://${window.location.host}/ws/${room}/`);

chatSocket.onmessage = function(e){
    console.log('on message')

    onChatMessage(JSON.parse(e.data))
}

chatSocket.onopen = function(e){
    console.log('on open')
}

chatSocket.onclose = function(e){
    console.log('chatSocket closed unexpectedly')
}


// Event Listener

chatSubmitElement.onclick = function(e){
    e.preventDefault();

    sendMessage();

    return false
}
$(document).ready(function() {
    $('#action_menu_btn').click(function () {
        $('.action_menu').toggle();
    });

    var messenger = {};
    console.log(JSON.parse(localStorage.getItem('messenger')));

    if(localStorage.getItem('messenger') !== null){
        messenger = JSON.parse(localStorage.getItem('messenger'));
        addMessageToCurrentSelectedPerson()
    }


    // appending all user to messenger array
    $('.user').each(function () {
        let id = $(this).attr('user-id');

        console.log(messenger[id]);

        if (messenger[id] === undefined){
            messenger[id] = []
        }
        // else messenger[id] = []
    });

    console.log(messenger);

    var chatSocket = new WebSocket('ws://' + window.location.host + '/messenger/');
    // console.log(chatSocket);

    $('.chat-select').on('click', function () {

        selectedUserId = parseInt($(this).attr('user-id'));
        var selectedUserName = $(this).attr('name');
        var selectedImageURL = $(this).attr('image-path');

        receiverData = {
            'id': selectedUserId,
            'name': selectedUserName,
            'image': selectedImageURL
        };

        $('#chat-with-name').text(selectedUserName);
        $('#chat-with-image').attr('src',selectedImageURL);

        chatBody.empty();
        addMessageToCurrentSelectedPerson();
    });


    // this "on message" method will receive tha all messages
    chatSocket.onmessage = function (e) {
        var data = JSON.parse(e.data);

        if (data.sender.id === selfId || data.receiver.id === selfId) {

            appendToMessenger(data);
            localStorage.setItem('messenger', JSON.stringify(messenger))
        }
    };


    function appendToMessenger(data){
        let senderId = data.sender.id;
        let receiverId = data.receiver.id;

        if (receiverId === selfId){
            messenger[senderId].push(data)
        }
        else messenger[receiverId].push(data);

        if (selectedUserId === receiverId || selectedUserId === senderId){
            chatBody.append(getMessageDiv(data))
        }
    }


    chatSocket.onclose = function (e) {
        console.error('Chat socket closed unexpectedly');
    };

    // document.querySelector('#chat-message-input').focus();

    $('#chat-textarea').on('keyup', function(e) {
        if (e.keyCode === 13) {  // enter, return
            $('#chat-message-submit').click();
        }
    });


    $('#chat-message-submit').on('click', function () {
        let chatInput = $('#chat-textarea');
        let message = chatInput.val();

        chatSocket.send(JSON.stringify({
            'sender': selfData,
            'receiver': receiverData,
            'message': message
        }));

        // chatBody.append(getMessageDiv(message))
        chatInput.val('')
    });



    function addMessageToCurrentSelectedPerson() {
        let messages = messenger[selectedUserId];

        messages.forEach(function (message) {
            chatBody.append(getMessageDiv(message))
        });
    }


    function getMessageDiv(data) {
        let sender = data['sender'];
        let receiver = data['receiver'];
        let message = data['message'];

        scrollToBottom();

        if(sender['id'] === selfId){
            return `<div class="d-flex justify-content-end mb-4">
                        <div class="msg_cotainer_send">
                            ${message}
                            <div class="row">
                                <span class="msg_time_send">Today</span>

                            </div>
                        </div>
                        <div class="img_cont_msg">
                            <img src="${sender['image']}" class="rounded-circle user_img_msg">
                        </div>
                    </div>`
        }
        else {
            return `<div class="d-flex justify-content-start mb-4">
                        <div class="img_cont_msg">
                            <img src="${sender['image']}" class="rounded-circle user_img_msg">
                        </div>
                        <div class="msg_cotainer">
                            ${message}
                            <div class="row">
                                <span class="msg_time_send">Today</span>

                            </div>
                        </div>
                    </div>`
        }
    }

    function scrollToBottom() {
        chatBody.animate({ scrollTop: chatBody.prop('scrollHeight')}, 10)
    }

    scrollToBottom();

});
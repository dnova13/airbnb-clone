let receive_data;

const msg_input = document.querySelector("input[name=message]")
const btn_send = document.querySelector("#send_msg")
const _pk = document.querySelector(".conv").id

const url = `${window.location.host}/ws/conversation/${_pk}/`
const noti_url = `${window.location.host}/ws/noti/${_id_op}/`

const chatSocket = socket_connect(url)
const sendNotiSocket = socket_connect(noti_url)


// 요청 후 다시 소켓에서 온 데이터 받아서 처리
chatSocket.onmessage = (e) => {
    let data = JSON.parse(e.data);
    receive_data = data["message"];

    if (receive_data.type == "conversation" && receive_data.user.id != _id) {
        addMessage(receive_data)
    }
};

chatSocket.onclose = (e) => {
    alert(gettext("Failed to send"))
};

btn_send.addEventListener("click", e => {

    // e.preventDefault()

    if (!msg_input.value) return

    let send_data = {
        "type": "conversation",
        "user": { "id": _id, "name": _name },
        "pk": _pk,
        "msg": msg_input.value
    }

    sendNotiSocket.send(JSON.stringify({ "type": "conversation", "conv_id": _pk, "noti": true }))
    chatSocket.send(JSON.stringify(send_data));
});

function addMessage(_data) {

    let div = document.createElement("div");
    div.className = "mb-10"

    let user_name = _data.user.name.length > 12 ? _data.user.name.slice(0, 12) + "..." : _data.user.name.slice(0, 12)

    let _created = loc == "en" ? moment(_data.created).format("MMM. D YYYY, h:mm a") : moment(_data.created).format("lll")
    _created = _created.replace("am", "a.m.").replace("pm", "p.m.")

    tags = `<span class="text-sm font-medium  w-56 text-gray-600 truncate">
                    ${user_name}
                    </span>
                    <div class="mt-px p-5 w-56 rounded break-words text-left bg-gray-300">
                        ${_data.msg}
                    </div>
                    <p class="text-xs">${_created}</p>`

    div.innerHTML = tags

    let read_arr = document.querySelectorAll(".is-read")

    if (read_arr)
        read_arr.forEach((elem) => elem.remove());

    scrDiv.appendChild(div)
    scrDiv.scrollTop = scrDiv.scrollHeight;
}
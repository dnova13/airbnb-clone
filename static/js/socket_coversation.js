let receive_data;

const msg_input = document.querySelector("input[name=message]")
const btn_send = document.querySelector("#send_msg")
const _pk = document.querySelector(".conv").id

const url = `${window.location.host}/ws/conversation/${_pk}/`
const noti_url = `${window.location.host}/ws/noti/${_id_op}/`

const chatSocket = socket_connect(url)
const sendNotiSocket = socket_connect(noti_url)
const scrDiv = document.querySelector(".chat-scroll");

let bt_scrCnt = false;

scrDiv.scrollTop = scrDiv.scrollHeight;

// 요청 후 다시 소켓에서 온 데이터 받아서 처리
chatSocket.onmessage = e => {
    let data = JSON.parse(e.data);
    receive_data = data["message"];

    // console.log(receive_data)

    if (receive_data.type == "conversation" && receive_data.user.id != _id) {
        bt_scrCnt = false;
        addMessage(receive_data, "opponent")

    }
};

chatSocket.onclose = (e) => {
    alert(gettext("Failed to send"))
};

btn_send.addEventListener("click", async e => {

    e.preventDefault()

    if (!msg_input.value) return

    let _message = msg_input.value
    let url = `/conversations/${_pk}/send/`
    let _data = { "msg": _message }
    let _tk = document.querySelector("input[name=csrfmiddlewaretoken]").value;

    let _h = {
        "X-CSRFToken": _tk,
    }

    let result = await ajaxCall(url, "POST", _data, _h)
    result = await result.json()

    msg_input.value = ""


    let msg_data = {
        "msg": _message,
        "created": undefined,
        "user": {
            "name": _name
        },
    }

    if (result["success"]) {

        msg_data["created"] = result["created"]

        addMessage(msg_data, "success")

        let send_data = {
            "type": "conversation",
            "user": { "id": _id, "name": _name },
            "pk": _pk,
            "msg": _message
        }

        sendNotiSocket.send(JSON.stringify({ "type": "conversation", "conv_id": _pk, "noti": true }))
        chatSocket.send(JSON.stringify(send_data));

        return
    }

    addMessage(msg_data, "fail")
});

function addMessage(_data, status) {

    let addClassName = ""
    let bgColoer = ""
    let stSpan = ""
    let stText = gettext("failed")

    if (status == "success") {
        addClassName = "conv-msg self-end text-right"
        bgColoer = "bg-teal-500 text-white"
        stSpan = !_data.is_read ? `<p class="is-read text-xs">1</p>` : ""
    }
    else if (status == "fail") {
        addClassName = "self-end text-right"
        bgColoer = "bg-red-500 text-white"
        stSpan = `<p class="failed text-xs text-red-500">${stText}</p>`
    }
    else if (status == "opponent") {
        addClassName = "conv-msg"
        bgColoer = "bg-gray-300"

        let read_arr = document.querySelectorAll(".is-read")

        if (read_arr)
            read_arr.forEach((elem) => elem.remove());
    }

    let div = document.createElement("div");
    div.className = "mb-10 " + addClassName

    let user_name = _data.user.name.length > 12 ? _data.user.name.slice(0, 12) + "..." : _data.user.name.slice(0, 12)

    let _created = loc == "en" ? moment(_data.created).format("MMM. D YYYY, h:mm a") : moment(_data.created).format("lll")
    _created = _created.replace("am", "a.m.").replace("pm", "p.m.")

    tags = `<span class="text-sm font-medium w-56 text-gray-600 truncate">
            ${user_name}
            </span>
            <div class="mt-px p-5 w-56 rounded break-words text-left ${bgColoer}">
                ${_data.msg}
            </div>
            <p class="text-xs">${_created}</p>
            `

    div.innerHTML = tags + stSpan

    let _div = document.querySelector(".chat-scroll")
    _div.appendChild(div)
    _div.scrollTop = _div.scrollHeight;
}

async function read_msg() {
    let url = `/conversations/${_pk}/read/`
    let _tk = document.querySelector("input[name=csrfmiddlewaretoken]").value;

    let _h = {
        "X-CSRFToken": _tk,
    }

    let result = await ajaxCall(url, "POST", null, _h)
    return result
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



// 스크롤 페이징 이벤트
scrDiv.addEventListener("scroll", async e => {

    e.preventDefault();

    if (Math.abs(scrDiv.scrollHeight - scrDiv.scrollTop - scrDiv.offsetHeight) <= 2) {

        if (!bt_scrCnt) {

            bt_scrCnt = true

            let __msgs = document.querySelectorAll(".conv-msg")

            if (__msgs[__msgs.length - 1].classList.contains('self-end'))
                return

            await read_msg()
            const opp_noti_url = `${window.location.host}/ws/noti/${_id_op}/`
            const opp_notiSocket = socket_connect(opp_noti_url)

            opp_notiSocket.onopen = () => opp_notiSocket.send(JSON.stringify({ "type": "read", "op_id": _id_op, "conv_id": _pk, "noti": true }))
        }
    }
});
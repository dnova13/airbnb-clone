let _total_reservs = 100;
let loc = gettext("en")
let _btnControl = false;
let __t = getParam("t")

moment.locale(loc)

function getParam(key) {
    return new URLSearchParams(location.search).get(key);
};

document.addEventListener("DOMContentLoaded", async function (event) {

    if (!__t) __t = "reserved"

    let _st = sessionStorage.getItem(__t)
    _st = _st ? _st : "all"

    document.querySelector(".reserv-forcus").classList.remove("reserv-forcus")
    document.querySelector(".reserv-op-forcus").classList.remove("reserv-op-forcus")

    document.querySelector(`#${__t}`).classList.add("reserv-forcus")
    document.querySelector(`#${_st}`).classList.add("reserv-op-forcus")

    await addReservations(1, __t)
});

async function addReservations(page, _type) {

    let _status = document.querySelector(".reserv-op-forcus").id
    let url = `/reservations/api/list/${_type}/?status=${_status}&page=${page}`;
    let img = document.createElement('img')

    _btnControl = false
    img.setAttribute("class", "mx-auto ");
    img.setAttribute("src", '/static/img/loading.gif');

    document.querySelector(".rev-section").appendChild(img)

    await ajaxCall(url, "GET").then(async res => {
        let data = await res.json()
        img.remove()

        if (data["success"]) {
            _total_reservs = data["total_reservs"]
            appendReservations(data["data"])
            _btnControl = true
        }
    })
}

function appendReservations(items) {

    for (item of items) {

        let div = document.createElement("div");

        div.className = "rev-card w-1/4 mb-10 px-2 overflow-hidden"

        // let _all = gettext("All")
        let _confirm = gettext("Confirmed")
        let _cancel = gettext("Canceled")
        let _pending = gettext("Pending")
        let __status
        let _created = loc == "en" ? moment(item.created).format("MMM. D YYYY, h:mm a") : moment(item.created).format("lll")
        _created = _created.replace("am", "a.m.").replace("pm", "p.m.")

        switch (item.status) {
            case 'pending':
                __status = _pending
                break;
            case "canceled":
                __status = _cancel
                break;
            case "confirmed":
                __status = _confirm
                break;
            default:
                break;
        }

        let tags = `
        <a href=/reservations/${item.id}/>
            <div class="w-full h-64 bg-full bg-center rounded-lg mb-2 " style="background-image: url(${item.room.first_photo});"></div>
            <span class="text-black w-11/12 block truncate">${item.room.name}</span>
            <div class="flex justify-between mb-2 truncate">
                <div class="w-4/5 overflow-hidden flex font-bold">
                    <span class="${item.status == 'pending' ? 'text-yellow-500' : item.status == 'canceled' ? 'text-red-600' : 'text-teal-500'}">
                    ${__status}
                    </span>
                </div >
            </div >
            <div class="w-4/5 overflow-hidden flex">
                <span class="text-sm text-gray-600 block truncate">${_created}</span>
            </div>
        </a>`

        div.innerHTML = tags

        document.getElementById("rev-cards").appendChild(div)
    }
}


let scrCnt = 0;
let _page = 1;

// 스크롤 페이징 이벤트
window.addEventListener("scroll", async e => {

    e.preventDefault();

    // console.log("cn", scrCnt)
    // console.log(Math.abs(document.body.scrollHeight - window.innerHeight - window.scrollY))

    if (Math.abs(document.body.scrollHeight - window.innerHeight - window.scrollY) <= 250) {

        let _cnt = document.querySelectorAll('.rev-card').length
        scrCnt++;

        // console.log("aa", _total_reservs > _cnt)
        // console.log(_total_reservs)
        // console.log(_cnt)

        if (scrCnt === 1 && _total_reservs > _cnt) {

            // console.log("!!!!!!!!!!!!!!!!!!!!")
            let type = document.querySelector(".reserv-forcus").id
            _page++
            await addReservations(_page, type)

            scrCnt = 0;
        }
    }
});

// 예약 최하위 옵션 4개 선택
document.querySelectorAll(".rev-op-link > li").forEach(li => {

    li.addEventListener("click", async e => {

        resetList()

        document.querySelector(".reserv-op-forcus").classList.remove("reserv-op-forcus")
        li.classList.add("reserv-op-forcus")

        let type = document.querySelector(".reserv-forcus").id
        sessionStorage.setItem(__t, li.id)

        await addReservations(1, type)
    })
})

// 예약 옵션 2개 보기
document.querySelectorAll(".reserv_link").forEach(li => {

    li.addEventListener("click", async e => {

        e.preventDefault()

        if (_btnControl) {

            if (li.id === "requested") {
                location.href = location.pathname + "?t=requested"
            }

            else {
                location.href = location.pathname + "?t=reserved"
            }
        }
    })
})

function resetOptionFocus() {
    document.querySelector(".reserv-op-forcus").classList.remove("reserv-op-forcus")
    document.querySelector("#all").classList.add("reserv-op-forcus")
}

function resetList() {
    scrCnt = 0
    _page = 1
    document.querySelector("#rev-cards").innerHTML = ""
}
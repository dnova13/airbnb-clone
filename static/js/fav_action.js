let favTag = document.querySelector(".fav")
let cntTag = document.querySelector(".fav-count")

let save = gettext("Save")
let saved = gettext("Saved")

favTag.addEventListener("click", async e => {

    e.preventDefault()

    let url = favTag.getAttribute("href")

    await ajaxCall(url, "GET").then(async res => {

        let ok = await res.ok

        if (ok) {
            let room_pk = document.querySelector(".room").id

            if (url.includes("remove")) {
                favTag.setAttribute('href', `/lists/toggle/${room_pk}?action=add`)
                favTag.innerHTML = `♡ ${save}`
                cntTag.innerText = Number(cntTag.innerText) - 1
            }

            else {
                favTag.setAttribute('href', `/lists/toggle/${room_pk}?action=remove`)
                favTag.innerHTML = `<span class="text-red-600">♥ </span>${saved}`
                cntTag.innerText = Number(cntTag.innerText) + 1
            }
        }
    })
});
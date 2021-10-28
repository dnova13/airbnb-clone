
document.addEventListener("DOMContentLoaded", async function (event) {

    // event.preventDefault();
    await addReviews(1)
});

async function addReviews(page) {


    let room_pk = window.location.pathname.replace('/rooms/', "")
    let url = `/api/v1/reviews/list/${room_pk}?page=${page ? page : 1}`;

    const response = await ajaxCall(url, "GET")
    const data = await response.json();

    if (data["success"]) {
        appendReviews(data["data"])
    }
}

function appendReviews(reviews) {

    for (review of reviews) {

        let div = document.createElement("div");
        let avatarTag = '';
        let created = moment(review.created).format("DD MMM YYYY")

        div.setAttribute("id", "review");
        div.setAttribute("class", "border-section");

        if (review.user.avatar)
            avatarTag = `<div class="w-10 h-10 rounded-full bg-cover" style="background-image: url(${review.user.avatar});"></div>`

        else
            avatarTag = `
            <div class="w-10 h-10 bg-gray-700 rounded-full text-white flex justify-center items-center overflow-hidden" >
                <span class="text-xl">${review.user.first_name.charAt(0)}</span>
            </div>`

        let tags = `
        <div class="mb-3 flex">
            <div>
                ${avatarTag}
            </div>
            <div class="flex flex-col ml-5">
                <span class="font-medium">${review.user.first_name}</span>
                <span class="text-sm text-gray-500">${created}</span>
            </div>
        </div>
        <p>${review.review}</p>`

        div.innerHTML = tags

        document.getElementById("review-section").appendChild(div)
    }
}


let scrCnt = 0;
let pageSize = 10;

// 스크롤 페이징 이벤트
window.addEventListener("scroll", async e => {

    e.preventDefault();

    if (Math.abs(document.querySelector("body > div.container.mx-auto.flex.justify-around.pb-56").scrollHeight - window.innerHeight - window.scrollY) <= 300) {

        scrCnt++;

        if (scrCnt === 1) {

            let revieCnt = document.querySelectorAll('#review').length
            page = Math.ceil(revieCnt / pageSize) + 1

            await addReviews(page)

            scrCnt = 0;
        }
    }
});
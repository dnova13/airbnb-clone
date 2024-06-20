let reviewTotal = 100;

document.addEventListener('DOMContentLoaded', async function (event) {
    // event.preventDefault();
    await addReviews(1);
});

async function addReviews(page) {
    let room_pk = document.querySelector('.room').id;
    let url = `/api/v1/reviews/list/${room_pk}/?page=${page ? page : 1}`;
    // let s_url = `https://airbnb-clone-dnova12222.s3.amazonaws.com`
    // let s_url = `http://localhost`;
    let s_url = `${window.location.protocol}//${window.location.host}`;

    let img = document.createElement('img');

    img.setAttribute('class', 'mx-auto mt-3');
    img.setAttribute('src', s_url + '/static/img/loading.gif');

    document.querySelector('#review-section').appendChild(img);

    await ajaxCall(url, 'GET').then(async (res) => {
        img.remove();
        if (res.status === 204) return;

        let data = await res.json();

        if (data['success']) {
            reviewTotal = data['total_reviews'];
            appendReviews(data['data']);
            scrCnt = 0;
        }
    });
}

function appendReviews(reviews) {
    for (review of reviews) {
        let div = document.createElement('div');

        let avatarTag = '';
        let created = moment(review.created).format('DD MMM YYYY');

        div.setAttribute('id', 'review');
        div.setAttribute('class', 'border-section');

        if (review.user.avatar) avatarTag = `<div class="w-10 h-10 rounded-full bg-cover" style="background-image: url(${review.user.avatar});"></div>`;
        else
            avatarTag = `
            <div class="w-10 h-10 bg-gray-700 rounded-full text-white flex justify-center items-center overflow-hidden" >
                <span class="text-xl">${review.user.first_name.charAt(0)}</span>
            </div>`;

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
        <p>${review.review}</p>
        `;

        div.innerHTML = tags;

        document.getElementById('review-section').appendChild(div);
    }
}

let scrCnt = 0;
let pageSize = 10;

// 스크롤 페이징 이벤트
window.addEventListener('scroll', async (e) => {
    e.preventDefault();

    if (Math.abs(document.querySelector('body > div.container.mx-auto.flex.justify-around.pb-56').scrollHeight - window.innerHeight - window.scrollY) <= 250) {
        let reviewCnt = document.querySelectorAll('#review').length;
        scrCnt++;

        if (scrCnt === 1 && reviewTotal > reviewCnt) {
            page = Math.ceil(reviewCnt / pageSize) + 1;

            await addReviews(page);
        }
    }
});

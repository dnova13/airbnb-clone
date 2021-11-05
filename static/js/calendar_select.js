let a;
let b;
let diff;
let cnt = 0;
let lastIdx = 0;
let isBook = false;


const cal_days = document.querySelectorAll(".sel-number")

cal_days.forEach((day, idx) => {
    day.addEventListener("click", e => {

        if (cnt == 0)
            a = { tag: e.target, idx: idx }

        else
            b = { tag: e.target, idx: idx }


        selDay(a.tag)

        aDate = a.tag.getAttribute('value')
        bDate = b ? b.tag.getAttribute('value') : 0

        diff = b ? diffDate(bDate, aDate) : undefined

        cnt++;

        if (diff === 0) {
            clearAll();
        }

        else if (diff > 0) {

            if (diff > 9) {
                alert("Available for less than 10 days");
                return;
            }

            clearDays();

            for (let i = a.idx; i <= b.idx; i++) {

                if (cal_days[i].className.includes("is_booked")) {
                    alert("invalid select");
                    clearAll();
                    return;
                }


                selDay(cal_days[i])
            }

            setTimeout(function () {
                isBook = confirm("Do you want the reservation?")

                let room_pk = window.location.pathname.replace('/rooms/', "")

                if (isBook)
                    location.href = `/reservations/create/${room_pk}/${aDate}/${diff}`
            }, 100);
        }

        else if (cnt > 1 && diff < 0)
            alert("Don't select");
    })
})

function selDay(day) {
    day.classList.replace("bg-white", "bg-red-600")
    day.classList.replace("text-gray-700", "text-white")
}

function clearDay(day) {
    day.classList.replace("bg-red-600", "bg-white")
    day.classList.replace("text-white", "text-gray-700")
}

function clearDays() {
    cal_days.forEach(day => {
        clearDay(day)
    })
}

function clearAll() {

    clearDays();

    a = null
    b = null
    diff = ""

    cnt = 0;
}

function diffDate(end_value, start_value) {

    let start_Array = start_value.split("-");
    let end_Array = end_value.split("-");

    let start_date = new Date(start_Array[0], Number(start_Array[1]) - 1, start_Array[2]);
    let end_date = new Date(end_Array[0], Number(end_Array[1]) - 1, end_Array[2]);


    return (end_date.getTime() - start_date.getTime()) / 1000 / 60 / 60 / 24;
}
card_num = window.location.search.split('=')[1]

$(document).ready(function () {
    show_reply()
});

function save_reply() {

    let reply = $('#reply').val()

    if (reply == "") {
        alert("다시 입력해주세요.")
    } else {
        $.ajax({
            type: 'POST',
            url: '/reply',
            data: {
                reply_give: reply,
                card_give: card_num

            },
            success: function (response) {
                alert(response['msg'])
                window.location.reload()
            }
        })
    }
}

function show_reply() {
    $.ajax({
        type: "GET",
        url: "/reply",
        data: {},
        success: function (response) {

            let rows = response["list"]

            for (let i = 0; i < rows.length; i++) {

                let userId = rows[i]['id']
                let reply = rows[i]['reply']
                let card = rows[i]['card_num']
                if (card == card_num) {
                    let temp_html = `<div class="card">
                                                    <div class="card-body">
                                                        <blockquote class="blockquote mb-0">
                                                            <p>${reply}</p>
                                                            <footer class="blockquote-footer">${userId}</footer>
                                                        </blockquote>
                                                    </div>
                                                </div>`
                    $('#reply-list').append(temp_html)
                }
            }
        }
    })
}

const imageElement = document.querySelector('.dp_top');
imageElement.addEventListener('click', () => {
    console.log('click');
    window.location.href = '/'
})
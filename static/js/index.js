   $(document).ready(function(){
            listing()
        });

        function listing() {
            $('#cards-box').empty()
            $.ajax({
                type: 'GET',
                url: '/podcast',
                data: {},
                success: function (response) {
                    let rows = response['all_podcast']
                    for (let i = 0; i< rows.length; i++){
                        let comment = rows[i]['comment']
                        let epi_title = rows[i]['epi_title']
                        let image = rows[i]['image']
                        let chan_title = rows[i]['chan_title']
                        let num = rows[i]['card_num']

                        let temp_html = `<div class="col">
                                            <div class="card h-100">
                                                <img src="${image}" class="card-img-top">
                                                <div class="card-body">
                                                    <a href="/detail?card_num=${num}"> <h5 class="card-title">${epi_title}</h5></a>
                                                    <p class="card-text">${chan_title}</p>
                                                    <p class="mycomment">"${comment}"</p>
                                                    <p><button type="button" class="btn btn-outline-dark" onclick="deleteRow(${num})">삭제</button></p>
                                               </div>
                                            </div>
                                        </div>`
                        $('#cards-box').append(temp_html)
                    }
                }
            })
        }
        function deleteRow(num) {
                $.ajax({
                    type: 'POST',
                    url: '/api/delete',
                    data: {'num_give':num},
                    success: function (response) {
                        alert(response['msg']);
                        window.location.reload()
                    }
                });
            }

        function posting() {
            let url = $('#url').val()
            let comment = $('#comment').val()

            $.ajax({
                type: 'POST',
                url: '/podcast',
                data: {'url_give':url,'comment_give':comment},
                success: function (response) {
                    alert(response['msg'])
                    window.location.reload()
                }
            });
        }

        function open_box(){
            $('#post-box').show()
        }
        function close_box(){
            $('#post-box').hide()
        }
        function logout(){
            $.removeCookie("mytoken", { path: '/'});
            alert('로그아웃!')
            window.location.reload()
        }
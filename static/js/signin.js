 function loginBtn(){

            let userId = $('#userId').val()
            let userPw = $('#userPw').val()
             if (userId == "" | userPw == "") {
                 alert('다시 입력해주세요.')
             } else {
                $.ajax({
                    type: "POST",
                    url: "/signin/login",
                    data: {userId_give: userId , userPw_give: userPw},
                    success: function (response) {
                        if (response['result'] == 'success') {
                            // 로그인이 정상적으로 되면, 토큰을 받아옵니다.
                            // 이 토큰을 mytoken이라는 키 값으로 쿠키에 저장합니다.
                             $.cookie('mytoken', response['token']);
                            alert('로그인 완료!')
                            window.location.href = '/'
                        } else {
                            // 로그인이 안되면 에러메시지를 띄웁니다.
                            alert(response['msg'])
                        }
                    }
                });
             }
        }

        function signUpBtn(){
            window.location.href = '/signup'
        }
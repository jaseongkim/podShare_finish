const regexpPhone = /\d/;
const regexpEmail = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/

const submitElement = document.querySelector('#submit-button');
const deleteElement = document.querySelector('#delete-button');
const backElement = document.querySelector('.back');

submitElement.addEventListener('click', modifyAccount)
deleteElement.addEventListener('click', deleteAccount)
backElement.addEventListener('click', () => {
  window.location.href = '/';
})

function modifyAccount() {
  let password = $('#password-value').val();
  let repassword = $('#re-password-value').val();
  let email = $('#email-value').val();
  let phone = $('#phone-value').val();

  let passwordLabel = $('.password-span');
  let repasswordLabel = $('.re-password-span');
  let emailLabel = $('.email-span');
  let phoneLabel = $('.phone-span');

  let passSign = {
    password: false,
    email: false,
    phone: false,
  };

  console.log()

  if (password === ''
      && email === ''
      && phone === ''
  ) {
    alert('변경할 내용이 없습니다.');
    return;
  }
  if (password !== '') {
    if (password.length < 10) {
      passwordLabel.text('비밀번호를 확인해주세요.').removeClass('text-grey text-green').addClass('text-red');
    } else {
      passwordLabel.text('사용 가능합니다.').removeClass('text-grey text-red').addClass('text-green');
      if (password !== repassword) {
        repasswordLabel.text('비밀번호가 일치하지 않습니다.').removeClass('text-grey text-green').addClass('text-red');
      } else {
        repasswordLabel.text('').removeClass('text-grey text-green text-red')
        passSign.password = true;
      }
    }
  } else {
    passwordLabel.text('비밀번호는 10자 이상의 문자만 입력 가능합니다.').removeClass('text-green text-red').addClass('text-grey');
  }

  if (email !== '') {
    if (regexpEmail.test(email) === false) {
      emailLabel.text('올바른 이메일 형식으로 입력해주세요.').removeClass('text-grey text-green').addClass('text-red');
    } else {
      emailLabel.text('사용 가능합니다.').removeClass('text-grey text-red').addClass('text-green');
      passSign.email = true;
    }
  } else {
    emailLabel.text('이메일 형식에 맞춰 입력 해주세요.').removeClass('text-green text-red').addClass('text-grey');
  }

  if (phone !== '') {
    if (regexpPhone.test($('#phone-value').val()) === false
        || phone.length < 9
        || phone.length > 11
    ) {
      phoneLabel.text('올바른 번호를 입력해주세요.').removeClass('text-grey text-green').addClass('text-red');
    } else {
      phoneLabel.text('사용 가능합니다.').removeClass('text-grey text-red').addClass('text-green');
      passSign.phone = true;
    }
  } else {
    phoneLabel.text('숫자만 입력 가능합니다.').removeClass('text-green text-red').addClass('text-grey');
  }
  console.log(passSign);

  if (!confirm('변경 하시겠습니까?')) {
    return true;
  } else {
    if (passSign.password
        || passSign.email
        || passSign.phone
    ) {
      if (passSign.password === false) {
        password = ''
      }
      if (passSign.email === false) {
        email = ''
      }
      if (passSign.phone === false) {
        phone = ''
      }
      console.log(passSign.password, passSign.email, passSign.phone);
      console.log(password, email, phone);

      $.ajax({
        type: 'POST',
        url: '/signchange/modify',
        data: {
          password: password,
          email: email,
          phone: phone,
        },
        success: function (response) {
          if (response['msg'] === '1') {
            passwordLabel.text('기존 패스워드와 동일합니다.').removeClass('text-grey text-green').addClass('text-red');
          } else if (response['msg'] === '2') {
            emailLabel.text('기존 이메일과 동일합니다.').removeClass('text-grey text-green').addClass('text-red');
          } else if (response['msg'] === '3') {
            phoneLabel.text('기존 전화번호와 동일합니다.').removeClass('text-grey text-green').addClass('text-red');
          } else {
            alert(response['msg'])
            window.location.href = '/';
          }
        }
      })
    }
  }
}

function deleteAccount() {
  if (!confirm('탈퇴 하시겠습니까?')) {
    return true;
  } else {
    $.ajax({
      type: 'POST',
      url: '/signchange/delete',
      data: {
        id: $('#id-value').val()
      },
      success: function (response) {
        alert(response['msg'])
        document.cookie = 'mytoken' + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
        window.location.href = '/';
      }
    })
  }
}
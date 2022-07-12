let dupCheckFinish = false;

const regexpPhone = /\d/;
const regexpEmail = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/


const checkElement = document.querySelector('#dup-check');
const submitElement = document.querySelector('#submit-button');

checkElement.addEventListener('click', dupCheck);
submitElement.addEventListener('click', submitValue);

function dupCheck() {
  const id = $('#id-value').val();
  let label = $('.id-span');

  if (id === '' || id.length > 10 || id.length < 4) {
    label.text('아이디를 확인해주세요.').removeClass('text-grey').addClass('text-red');
  } else {
    $.ajax({
      type: 'POST',
      url: '/signup/dupcheck',
      data: {
        id: id
      },
      success: function (response) {
        if (response['msg'] === '1') {
          label.text('중복되는 아이디입니다.').removeClass('text-grey text-green').addClass('text-red');
        } else {
          label.text('사용 가능합니다.').removeClass('text-grey text-red').addClass('text-green');
          dupCheckFinish = true;
        }
      }
    })
  }
}

function submitValue() {
  const id = $('#id-value').val();
  const password = $('#password-value').val();
  const repassword = $('#re-password-value').val();
  const email = $('#email-value').val();
  const phone = $('#phone-value').val();
  let gender = '';

  let idLabel = $('.id-span');
  let passwordLabel = $('.password-span');
  let repasswordLabel = $('.re-password-span');
  let emailLabel = $('.email-span');
  let phoneLabel = $('.phone-span');
  let genderLabel = $('.gender-span');

  let count = 0;

  if (id === '' || dupCheckFinish === false) {
    idLabel.text('아이디 중복 검사를 먼저 진행 해주세요.').removeClass('text-grey text-green').addClass('text-red');
  } else {
    if (dupCheckFinish === true) {
      if (password === '' || password.length < 10) {
        passwordLabel.text('비밀번호를 확인해주세요.').removeClass('text-grey text-green').addClass('text-red');
      } else {
        passwordLabel.text('사용 가능합니다.').removeClass('text-grey text-red').addClass('text-green');
        count++;
        if (password !== repassword) {
          repasswordLabel.text('비밀번호가 일치하지 않습니다.').removeClass('text-grey text-green').addClass('text-red');
        } else {
          repasswordLabel.text('').removeClass('text-grey text-green text-red')
          count++;
        }
      }

      if (email === '') {
        emailLabel.text('이메일을 입력해주세요.').removeClass('text-grey text-green').addClass('text-red');
      } else if (regexpEmail.test(email) === false) {
        emailLabel.text('올바른 이메일 형식으로 입력해주세요.').removeClass('text-grey text-green').addClass('text-red');
      } else {
        emailLabel.text('사용 가능합니다.').removeClass('text-grey text-red').addClass('text-green');
        count++;
      }

      if (phone === '') {
        phoneLabel.text('번호를 입력해주세요.').removeClass('text-grey').addClass('text-red');
      } else if (regexpPhone.test($('#phone-value').val()) === false
          || phone.length < 9
          || phone.length > 11
      ) {
        phoneLabel.text('올바른 번호를 입력해주세요.').removeClass('text-grey text-green').addClass('text-red');
      } else {
        phoneLabel.text('사용 가능합니다.').removeClass('text-grey text-red').addClass('text-green');
        count++;
      }

      if (document.querySelector('#man').checked === false
          && document.querySelector('#woman').checked === false) {
        genderLabel.text('성별을 선택해주세요.').removeClass('text-grey text-green').addClass('text-red');
      } else {
        genderLabel.text('').removeClass('text-grey text-red text-green');
        document.getElementsByName('gender').forEach((element) => {
          if (element.checked) {
            gender = element.id;
          }
        })
        count++;
      }

      if (count === 5) {
        $.ajax({
          type: 'POST',
          url: '/signup',
          data: {
            id: id,
            password: password,
            email: email,
            phone: phone,
            gender: gender,
          },
          success: function (response) {
            window.location.href = '/signin';
          }
        })
      }
    }
  }
}
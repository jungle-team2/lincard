// // CSR..!

// function getDOM() {
//   const signupDOM = document.querySelector(".signup");
//   const emailDoM = signupDOM.querySelector("#email");
//   const pwdDOM = signupDOM.querySelector("#password");
//   const pwdChkDOM = signupDOM.querySelector("#password-chk");
//   const email = emailDoM.value;
//   const password = pwdDOM.value;
//   const pwdChk = pwdChkDOM.value;

//   return { signupDOM, emailDoM, pwdDOM, email, password, pwdChk };
// }

// function signup() {
//   const { email, password, pwdChk } = getDOM();

//   const { success } = validationSignup({ email, password, pwdChk });
//   //  alert 처리
//   if (!success) return;

//   const user = { email, password };

//   fetch("/api/auth/sign-up", {
//     method: "post",
//     body: JSON.stringify(user),
//   });
// }

// function validationSignup({ email, password, pwdChk }) {
//   return { success: true };
// }

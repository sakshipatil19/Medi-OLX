const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
function matchPassword() {
  var pw1 = document.getElementById("pwd1").value;
  var pw2 = document.getElementById("pwd2").value;
  if(pw1 != pw2)
  {	
      alert("Passwords did not match");
  }
  else if(pw1 = null){
    alert("Enter valid Password");
  }
  else{
      // container.classList.remove("sign-up-mode");
  }
}
sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

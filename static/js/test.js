function Success(type,text='You clicked the button!'){
    Swal.fire(
        type,
        text,
        'success'
        )
}

function Checksubmit(){
    let acconut = document.getElementById("account").value.length;
    let password = document.getElementById("password").value.length;
    if (acconut == 0 && password == 0){
      alert("請輸入資料");
      return false
    }
    else if (acconut == 0){
      alert("請輸入帳號");
      return false
    }
    else if (password == 0){
      alert("請輸入密碼");
      return false
    }
    else{
      return true
    }
    }
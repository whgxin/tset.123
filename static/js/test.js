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





    function Checksubmit2(){
      let number = document.getElementById("number").value.length;
      let date = document.getElementById("date").value.length;
      let money = document.getElementById("money").value.length;
      let hours= document.getElementById("hours").value.length;
      //let note = document.getElementById("note").value.length;
      
      if (number == 0 && date == 0 && money == 0 && hours == 0){
        alert("請輸入資料");
        return false
      }
      else if (number == 0){
        alert("請輸入學號");
        return false 
      }
      else if (date == 0){
        alert("請輸入學期");
        return false
      }
      else if (hours == 0){
        alert("請輸入科目");
        return false
      }
      else if (money == 0){
        alert("請輸入成績");
        return false
      }
      else{
        return true
      }
      }





  
  function turn(){
      var number = parseInt(document.getElementById("val").value);
      if(!number)
        number = 1
      if(number < 0){
        number = Math.abs(number);
      }
      else {
        number = number * -1
      }
      var calculatedNumber = ((number) + 70);

      if(calculatedNumber > 80)
        calculatedNumber = 80;

      if(calculatedNumber < 61)
        calculatedNumber = 61;

      $.ajax({
          contentType: "application/json;charset=UTF-8",
          url : "/getnumber",
          type: "POST",
          data: JSON.stringify({val: calculatedNumber})
      });
  };

  setInterval(turn, 100);

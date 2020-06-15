$(document).ready(function(){

  $("form").submit(function(event){
    //this line disable the action inside of form
    event.preventDefault();
    //.val() to get the actual value of the id
    var formName;
    var url = $(" #form-url").val();
    var submit = $("#form-submit").val();
    
    // set up the form name
    theForms = document.getElementsByTagName("form");
    for(i=0;i<theForms.length;i++){
      formName = theForms[i].name;
    }

    $("#content").getJSON("backend.py",url, function(result, textStatus){
      if (textStatus == "success") {
        document.getElementsByTagName("main-page").style = "display:none;";
        document.getElementsByTagName("content").style = "display:flex;";
      }else if (textStatus == "error") {
        alert("Error: " + xhr.status + ": " + xhr.statusText);
      }
    });

    var profileInfo, views, comments, likes, date, comments_emo;

    function dataSeperation(data){
      // to deal with data

    }

    function profileDisplay(profileInfo){
      // profileInfo =[pic_link, ]
      document.getElementsbyId("profile_pic")[0].src = profileInfo[0]
    }

    function views(views, date){

    }

    function comments(comments,date){

    }

    function likes(comments,date){

    }

    function comments_emo(emo){

    }
    
        
        

  });
})

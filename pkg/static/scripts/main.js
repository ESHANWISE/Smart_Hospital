



$(document).ready(function(){

    // login form validation
    var email = $('#email').val();
    const pass = $('#pass').val();
    const form = $('#loginForm');
    const errorMessage = $('#errors');
    

    $(form).submit(function(e){
     
        let message = []
        if(pass == '' ){
            alert('password empty')
           //message.append('Invalid password or Password too long or too short')
           e.preventDefault();
        }else{
            return true;
        }

        if(message.length > 0){
            e.preventDefault();
            errorMessage.test = message.join(', ')
        }
        
    })


// create botton

// $('#createaccount').click(function(){
//     $('#createForm').show(800)
//    $('#loginForm').hide(800)
    
// })

// $('#create').click(function(){
//     $('#loginForm').show(800)
//     $('#createForm').hide(800)
   
// })


function validate(){
    var user = $("#uname1").val();
    var pass = $("#pass1").val()

    if(user==""){
         document.getElementById("errorMessage").innerHTML='<span class="text-danger"> *fill out all information</span>'
         return false;
     
    }else if(pass==""){
         document.getElementById("errorMessage1").innerHTML='<span class="text-danger"> *fill out all information</span>'
         return false;
     }
    else  {
     document.getElementById("errorMessage").innerHTML=''
     return true;
    }
    
         
    

 }
$(document).ready(function(){
     $("#change").click(function(){
         $("#formMain").hide();
         $("#logForm").show(700);
     })
     $("#login").click(function(){
         $("#logForm").hide(1000);
         $("#formMain").show(700)
     })
 })


 
})
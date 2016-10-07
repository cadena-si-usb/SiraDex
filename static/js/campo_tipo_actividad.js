$(document).ready(function(){
  $("#campos table tbody td").each(function(){

    // Se cambia True por si y False por no en la tabla de los campos.
    if ($(this).html() == "True"){$(this).html("Si");}
    else if ($(this).html() == "False"){$(this).html("No");}
  })
});

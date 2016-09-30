$(document).ready(function(){
  var maxLongNombre  = 128;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;  // Longitud máxima que tendrá el campo descripción.

  // Se elimina el div de "error_wrapper" en nombre, si existe, porque repite la información.
  if ($("#no_table_Nombre").siblings(".error_wrapper").length > 0){
    $("#no_table_Nombre").siblings(".error_wrapper").remove();
  }

  // Se elimina el div de "error_wrapper" en descripción, si existe, porque repite la información.
  if ($("#no_table_Descripcion").siblings(".error_wrapper").length > 0){
    $("#no_table_Descripcion").siblings(".error_wrapper").remove();
  }

  // Selecciono el div que es "hermano" del textfield de nombre.
  var longitudTextoAct = $("#no_table_Nombre").val().length;
  if (longitudTextoAct == 0){
    $("#no_table_Nombre").siblings(".help-block").html(maxLongNombre + " caracteres (No puede estar vacío)");
  }else{
    $("#no_table_Nombre").siblings(".help-block").html((maxLongNombre - longitudTextoAct) + " caracteres");
  }

  // Selecciono el div que es "hermano" del textarea de descripción.
  longitudTextoAct = $("#no_table_Nombre").val().length;
  if (longitudTextoAct == 0){
    $("#no_table_Descripcion").siblings(".help-block").html(maxLongDescrip + " caracteres. (No puede estar vacío)");
  }else{
    $("#no_table_Descripcion").siblings(".help-block").html((maxLongDescrip - longitudTextoAct) + " caracteres.");
  }

  // Si estoy escribiendo en el textfield de nombre, entonces...
  $("#no_table_Nombre").keyup(function(){
    var longitudTexto = $("#no_table_Nombre").val().length;
    var textoRestante = maxLongNombre - longitudTexto;

    if (textoRestante == maxLongNombre){
      $("#no_table_Nombre").siblings(".help-block").html(textoRestante + " caracteres (No puede estar vacío)");
    }else{
      $("#no_table_Nombre").siblings(".help-block").html(textoRestante + " caracteres");
    }

    if (textoRestante < 0){
      $(".btn-primary").prop('disabled',true);
    }else if(textoRestante >= 0 && $(".btn-primary").is(":disabled")){
      $(".btn-primary").prop('disabled',false);
    }
  });

  // Si estoy escribiendo en el textarea de descripción, entonces...
  $("#no_table_Descripcion").keyup(function(){
    var longitudTexto = $("#no_table_Descripcion").val().length;
    var textoRestante = maxLongDescrip - longitudTexto;

    if (textoRestante == maxLongDescrip){
      $("#no_table_Descripcion").siblings(".help-block").html(textoRestante + " caracteres. (No puede estar vacío)");
    }else{
      $("#no_table_Descripcion").siblings(".help-block").html(textoRestante + " caracteres.");
    }

    if (textoRestante < 0){
      $(".btn-primary").prop('disabled',true);
    }else if(textoRestante >= 0 && $(".btn-primary").is(":disabled")){
      $(".btn-primary").prop('disabled',false);
    }
  });
});

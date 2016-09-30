$(document).ready(function(){
  var maxLongNombre  = 128;    // Longitud máxima que tendrá el campo nombre.
  var maxLongDescrip = 2048;  // Longitud máxima que tendrá el campo descripción.

  textoRestante(maxLongNombre,  "#no_table_Nombre");
  textoRestante(maxLongDescrip, "#no_table_Descripcion");
});

/*
  - Descripción:
        permite mostrar, y calcular, cuantos caracteres quedan disponible en un
        textfield/textarea.

  - Parámetros:
        @param maxLong  : número máximo de caracteres a utilizar.
        @param idDivUsar: identificador del div donde se mostrára el texto.
*/
function textoRestante(maxLong, idDivUsar){
  var longitudTexto = $(idDivUsar).val().length;
  var textoRestante = maxLong - longitudTexto;

  // Se elimina el div de "error_wrapper", si existe, porque repite la información.
  if ($(idDivUsar).siblings(".error_wrapper").length > 0){
    $(idDivUsar).siblings(".error_wrapper").remove();
  }

  // Selecciono el div que es "hermano" del textfield de nombre.
  var longitudTextoAct = $(idDivUsar).val().length;
  if (longitudTextoAct == 0){
    $(idDivUsar).siblings(".help-block").html(maxLong + " caracteres (No puede estar vacío)");
  }else{
    $(idDivUsar).siblings(".help-block").html((maxLong - longitudTextoAct) + " caracteres");
  }

  // Si estoy escribiendo en el textfield de nombre, entonces...
  $(idDivUsar).keyup(function(){
    var longitudTexto = $(idDivUsar).val().length;
    var textoRestante = maxLong - longitudTexto;

    if (textoRestante == maxLong){
      $(idDivUsar).siblings(".help-block").html(textoRestante + " caracteres. (No puede estar vacío)");
    }else{
      $(idDivUsar).siblings(".help-block").html(textoRestante + " caracteres.");
    }

    if (textoRestante < 0){
      $(".btn-primary").prop('disabled',true);
      $(idDivUsar).siblings(".help-block").css("color","red");
    }else if (textoRestante >= 0 && $(".btn-primary").is(":disabled")){
      $(".btn-primary").prop('disabled',false);
      $(idDivUsar).siblings(".help-block").css("color","");
    }
  });
}

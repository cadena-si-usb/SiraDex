$(document).ready(function(){
  // Pasamos los argumentos para eliminar el programa.
  $('#modalEliminarUsuario').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar');
      $("#BotonEliminar").attr("href", linkEliminar);
  });
});
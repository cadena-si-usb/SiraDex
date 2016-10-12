$(document).ready(function(){

 $('#ModalModificarUsuario').on('show.bs.modal', function(e){
      var tipo = $(e.relatedTarget).data('tipo');

      $(e.currentTarget).find('input[name="tipo"]').val(tipo);
  });

  // Pasamos los argumentos para eliminar el programa.
  $('#modalEliminarUsuario').on('show.bs.modal', function(e){
      var linkEliminar = $(e.relatedTarget).data('link-eliminar');
      $("#BotonEliminar").attr("href", linkEliminar);
  });
});
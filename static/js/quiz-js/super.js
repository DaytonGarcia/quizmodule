function submitLoad(controlador,funcion,params)
{
  alert("Si llego");
  var retorno ="";
  pageload="https://"+document.domain+"/cpfecys/"+controlador+"/"+funcion+params;
  $.ajax({
  	url: pageload, 
  	async: true,
  	success: function(result)
  	{
  		//jsonResult = JSON.parse(result);
  		retorno=(result); 

   }});

 return(retorno);
  
}

function LlamarControlador(controlador,funcion,params)
{
  var retorno ="";
  pageload="https://"+document.domain+"/cpfecys/"+controlador+"/"+funcion+params;
  alert(pageload);
  $.ajax({
    url: pageload, 
    async: true,
    success: function(result)
    {
      //jsonResult = JSON.parse(result);
      retorno=(result); 

   }});

 //return(retorno);
  
}

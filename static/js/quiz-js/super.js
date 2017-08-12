function submitLoad(controlador,funcion,params)
{
  var retorno ="";
  pageload="https://"+document.domain+"/"+controlador+"/"+funcion+params;
  $.ajax({
  	url: pageload, 
  	async: false,
  	success: function(result)
  	{
      //jsonResult = JSON.parse(result);
      //return (result);
      retorno=(result); 
   }});
 return(retorno);
  
}

function LlamarControlador(controlador,funcion,params)
{
  var retorno ="";
  pageload="https://"+document.domain+"/"+controlador+"/"+funcion+params;
  alert(pageload);
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

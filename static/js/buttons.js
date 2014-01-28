var buttonsScript = function(){
    
    var width, height;
    
    document.getElementById("create").addEventListener("click", moveToCanvas); 
    
    var moveToCanvas = function(){
	width = document.getElementById("width").value;
	height = document.getElementById("height").value;
	window.location="/canvas";
   }

    document.getElementById("delete").addEventListener("click", deleteCanvas);

    var deleteCanvas = function(){
	window.alert("Are you sure you wanna delete this?")
}();


buttonScript();

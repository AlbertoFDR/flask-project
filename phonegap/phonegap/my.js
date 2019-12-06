
$(document).ready(function() {
	//GET JSON OF THE HEROKU SERVER
	$.getJSON('https://desarrollophonegap.herokuapp.com/getbooks', function(data) { 
		var html = "";
		for(let i = 0; i < data.length ; i++){
			
			//RELLENAR EL HTML DE TODOS LOS LIBROS
			//JSON FORMAT (IMG, TITLE, AUTHOR, CREATED.... IMG, TITLE...)
			let ret = i%4;
			if(ret==0){
				//Img
				html += "<div class='col-sm-6 col-md-4'>"
				html += "<div class='thumbnail'>"
				html += "<img class='img-thumbnail' src='data:image/png;base64," + data[i] + "' alt='...'>";
			}else if(ret==1) {
				//Title
				html += "<div class='caption'><h3> " + data[i] + " </h3>";
			}else if(ret==2){
				//Auth0r
				html += "<p>" + data[i] + "</p>";
			}else if(ret==3){
				//Created
				html += "<p>" + data[i] + "</p><p><a href='' class='btn btn-primary' role='button'>Descargar</a></p></div>";
				html += "</div></div>"
			}

		}
		//INCLUIRLO AL DOM
		document.getElementById("rellenar").innerHTML = html;

	}); 
});


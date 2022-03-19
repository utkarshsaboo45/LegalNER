function insert_result(response) {
	var maintext = document.getElementById("maintext");
	maintext.innerHTML = response;
}


function insert_result_container(response) {
	var maintext = document.getElementById("container");
	maintext.innerHTML = response;
}


function update_page() {
	var form = document.getElementById("form");
	var formData = new FormData(form);
	var searchParams = new URLSearchParams(formData);
	keys = searchParams.getAll("keyword")
	entities = searchParams.getAll("entity")
	var queryString = "entity=" + entities.toString() + "&keyword=" + keys.toString()
	// var queryString = searchParams.toString();
	xmlHttpRqst = new XMLHttpRequest();
	xmlHttpRqst.onload = function (e) { insert_result(xmlHttpRqst.response); }
	xmlHttpRqst.open("GET", "/corpus/?" + queryString);
	xmlHttpRqst.send();

}

function update_about_form() {                         
	var form = document.getElementById("about-form");
	var formData = new FormData(form);
	var searchParams = new URLSearchParams(formData);
	var queryString = searchParams.toString();
	xmlHttpRqst = new XMLHttpRequest();
	xmlHttpRqst.onload = function (e) { insert_result_container(xmlHttpRqst.response); }
	xmlHttpRqst.open("GET", "/about/?" + queryString);
	xmlHttpRqst.send();
}


function update_usage_form() {
	var form = document.getElementById("usage-form");
	var formData = new FormData(form);
	var searchParams = new URLSearchParams(formData);
	var queryString = searchParams.toString();
	xmlHttpRqst = new XMLHttpRequest();
	xmlHttpRqst.onload = function (e) { insert_result_container(xmlHttpRqst.response); }
	xmlHttpRqst.open("GET", "/usage/?" + queryString);
	xmlHttpRqst.send();
}
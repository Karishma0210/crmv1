$(document).ready(function () {
	$("#dummy").attr("disabled", true);
	$("#task-status").val("");
	$("#task-status").change(function () {
		console.log($(this).val());

		let formData = new FormData();
		formData.set("selected-task", $(this).val());
		const csrftoken = getCookie("csrftoken");
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
		}
		$.ajaxSetup({
			beforeSend: function (xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			},
		});
		$.ajax({
			type: "POST",
			url: "",
			data: formData, // serializes the form's elements.
			processData: false,
			contentType: false,
			success: function (data) {
				// console.log(data); // show response from the Django script.

				$("#task-type").text($("#task-status option:selected").html());
				$("#tt-space").html(data);
			},
			error: function () {
				alert("error in loading the task list");
			},
		});
	});
});

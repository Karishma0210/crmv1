$(document).ready(function () {
	$(".delete-form").submit(function (e) {
		// console.log("delete event submitting");
		e.preventDefault(); // avoid to execute the actual submit of the form.

		let form = $(this);

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

		let url = form.attr("action");
		$.ajax({
			type: "POST",
			url: url,
			data: form.serialize(), // serializes the form's elements.
			// processData: false,
			// contentType: false,
			success: function (response_product_id) {
				alert(
					"Successfully deleted product with id " +
						response_product_id +
						" from the task"
				);
				let dummy = "#" + response_product_id + "_btn";
				$(dummy).attr("disabled", true);
			},
			error: function () {
				alert("error deleting product");
			},
		});
	});
});

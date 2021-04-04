$(document).ready(function () {
	$(".review-form").submit(function (e) {
		// console.log($(e.originalEvent.submitter).attr("name"));
		e.preventDefault(); // avoid to execute the actual submit of the form.

		let form = $(this);
		let newForm = new FormData($(form)[0]);
		let submitter_btn = $(e.originalEvent.submitter);

		if (submitter_btn.attr("name") == "approve_btn") {
			newForm.set("action_for", submitter_btn.attr("name"));
		} else if (submitter_btn.attr("name") == "reject_btn") {
			newForm.set("action_for", submitter_btn.attr("name"));
		} else {
			console.log("there is some error!");
			return;
		}
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
			data: newForm, // serializes the form's elements.
			processData: false,
			contentType: false,
			success: function (response_product_id) {
				alert(
					"Successfully approved product id - " +
						response_product_id +
						" for the task"
				);
			},
			error: function () {
				alert("error approving product");
			},
		});
		// $(this).children("button").attr("disabled", true);
		$(this).children("button").hide();
		if (submitter_btn.attr("name") == "approve_btn") {
			$(this).html(
				'<i class="fa fa-check" style="color: rgb(10, 240, 10);"></i>'
			);
		} else if (submitter_btn.attr("name") == "reject_btn") {
			$(this).html('<i class="fa fa-times" style="color: red;"></i>');
		}
	});
});

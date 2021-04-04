$(document).ready(function () {
	//for approve or disapproval
	$(".review-form").submit(function (e) {
		// console.log($(e.originalEvent.submitter).attr("name"));
		e.preventDefault(); // avoid to execute the actual submit of the form.

		let form = $(this);
		let newForm = new FormData($(form)[0]);
		let submitter_btn = $(e.originalEvent.submitter);

		if (submitter_btn.attr("name") == "approve_btn") {
			newForm.set("submitter_btn", submitter_btn.attr("name"));
		} else if (submitter_btn.attr("name") == "reject_btn") {
			newForm.set("submitter_btn", submitter_btn.attr("name"));
		} else {
			alert("there is some error!");
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
			success: function (resp) {
				alert(resp);
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

	$(".change-status-form").submit(function (e) {
		// console.log($(e.originalEvent.submitter).attr("name"));
		e.preventDefault(); // avoid to execute the actual submit of the form.

		let form = $(this);
		let newForm = new FormData($(form)[0]);
		let submitter_btn = $(e.originalEvent.submitter);
		console.log(submitter_btn);
		if (submitter_btn.attr("name") == "task_ready_to_upload_btn") {
			newForm.set("submitter_btn", submitter_btn.attr("name"));
		} else if (submitter_btn.attr("name") == "task_cancelled_btn") {
			newForm.set("submitter_btn", submitter_btn.attr("name"));
		} else {
			console.log(submitter_btn.attr("name"));
			alert("there is some error!");
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

		for (let v of newForm.entries()) {
			console.log(v[0] + " - " + v[1]);
		}

		let url = form.attr("action");
		$.ajax({
			type: "POST",
			url: url,
			data: newForm, // serializes the form's elements.
			processData: false,
			contentType: false,
			success: function (resp) {
				alert(resp);
				window.location = "/tasks/";
			},
			error: function () {
				alert("error changing state of the task");
			},
		});
		// $(this).children("button").attr("disabled", true);
		console.log(
			$(this).children("div").children("button").attr("disabled", true)
		);
	});
});

function toggle(source, childClassName) {
	//Getting all child elements
	checkboxes = document.getElementsByClassName(childClassName);
	for (var i = 0, n = checkboxes.length; i < n; i++) {
		checkboxes[i].checked = source.checked;
	}
}
let searchParams = new URLSearchParams(window.location.search);
if (!searchParams.has("category")) {
	$("#add-prod-btn").attr("hidden", true);
	$("#no-cat-msg").html(
		'<div class="alert alert-warning" role="alert">Please select category first!</div>'
	);
} else {
	$("#add-prod-btn").attr("hidden", false);
}
$("#assign-prod-form").submit(function (e) {
	e.preventDefault(); // avoid to execute the actual submit of the form.

	let form = $(this);
	let formData = new FormData(form[0]);
	product_ids = formData.getAll("checkBox");
	// console.log(product_ids);
	// console.log("length - " + product_ids.length);
	if (product_ids.length < 1) {
		alert("no products selected");
		return;
	} else {
		var newFD = new FormData();

		for (let i = 0; i < product_ids.length; i++) {
			newFD.append("product_ids", product_ids[i]);
			newFD.set(
				"name_" + product_ids[i],
				formData.get("name_" + product_ids[i])
			);
			newFD.set(
				"regular_price_" + product_ids[i],
				formData.get("regular_price_" + product_ids[i])
			);
			// newFD.set(
			// 	"curr_price_" + product_ids[i],
			// 	formData.get("curr_price_" + product_ids[i])
			// );
			newFD.set(
				"sale_price_" + product_ids[i],
				formData.get("sale_price_" + product_ids[i])
			);
			newFD.set(
				"last_mod_onsite_" + product_ids[i],
				formData.get("last_mod_onsite_" + product_ids[i])
			);
			newFD.set(
				"parent_" + product_ids[i],
				formData.get("parent_" + product_ids[i])
			);
			newFD.set(
				"permalink_" + product_ids[i],
				formData.get("permalink_" + product_ids[i])
			);
			$("#cb_" + product_ids[i]).attr("disabled", true);
			$("#cb_" + product_ids[i]).attr("readonly", true);
		}
	}
	// for (let [n, v] of newFD) {
	// 	console.log(n + " - " + v);
	// }

	// console.log("Here submit");

	const csrftoken = getCookie("csrftoken");
	function csrfSafeMethod(method) {
		// these HTTP methods do not require CSRF protection
		return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
	}
	// console.log(csrftoken);
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
		data: newFD, // serializes the form's elements.
		processData: false,
		contentType: false,
		success: function (data) {
			alert(data); // show response from the Django script.
		},
		error: function () {
			alert("error adding in data");
		},
	});
});

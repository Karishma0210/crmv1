function toggle(source, childClassName) {
	//Getting all child elements
	checkboxes = document.getElementsByClassName(childClassName);
	for (var i = 0, n = checkboxes.length; i < n; i++) {
		checkboxes[i].checked = source.checked;
	}
}

$("#assign-prod-form").submit(function (e) {
	e.preventDefault(); // avoid to execute the actual submit of the form.

	let form = $(this);
	let url = form.attr("action");
	// console.log("Here submit");
	$.ajax({
		type: "POST",
		url: url,
		data: form.serialize(), // serializes the form's elements.
		success: function (data) {
			alert(data); // show response from the Django script.
		},
	});
});

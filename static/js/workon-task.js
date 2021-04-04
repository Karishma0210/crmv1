$(document).ready(function () {
	let newForm = new FormData();

	$("input[type='number']").attr("min", 0.0);

	//add listeners to new_reg_price_{{}} for updating form
	$("input[name^='new_reg_price']").on("input", function () {
		// console.log("new reg price value changed");
		current_row_id = parseInt($(this).attr("class"));
		console.log(current_row_id);
		current_row_data = $("input[name$=" + current_row_id + "]");
		console.log($(current_row_data));
		for (let i = 0; i < current_row_data.length; i++) {
			console.log($(current_row_data[i]));
			newForm.set(
				$(current_row_data[i]).attr("name"),
				$(current_row_data[i]).val()
			);
		}
		console.log("added to form");
	});

	$("input[name^='suggested_price']").on("input", function () {
		// console.log("new reg price value changed");
		current_row_id = parseInt($(this).attr("class"));
		console.log(current_row_id);
		current_row_data = $("input[name$=" + current_row_id + "]");
		console.log($(current_row_data));
		for (let i = 0; i < current_row_data.length; i++) {
			console.log($(current_row_data[i]));
			newForm.set(
				$(current_row_data[i]).attr("name"),
				$(current_row_data[i]).val()
			);
		}
		console.log("added to form");
	});

	$(".competitor").on("input", function () {
		current_row_id = $(this).attr("class").split(" ")[1];
		//get all competitors of same row
		curr_row_comp = $(".competitor").filter("." + current_row_id);
		// console.log(curr_row_comp);

		//get suggested price cell for dynamic suggested value change
		suggested_price_cell = $("." + current_row_id).filter(
			"input[name^='suggested_price_']"
		);
		// console.log(suggested_price_cell);

		assume_from_array = curr_row_comp
			.filter(function () {
				return $(this).val() > 0.1;
			})
			.map(function () {
				if ($(this).val() - 20 < 0) {
					return $(this).val();
				}
				return $(this).val() - 20;
			})
			.get();

		// console.log(assume_from_array);
		//get assumed value
		assumed_suggest_price = Math.min.apply(Math, assume_from_array);
		// console.log(assumed_suggest_price);
		suggested_price_cell.attr("value", assumed_suggest_price);
		suggested_price_cell.attr("value", assumed_suggest_price).trigger("input");
	});

	$("#mark-as-comp-btn").click(function (e) {
		e.preventDefault();
		// console.log($(this) + "im pressed");
		let dummyForm = new FormData();
		dummyForm.set("dummyKey", "dummyValue");

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
			url: window.location.pathname + "mark-as-complete",
			data: dummyForm, // serializes the form's elements.
			processData: false,
			contentType: false,
			success: function (data) {
				alert(data);
				window.location = "/tasks/";
			},
			error: function () {
				alert("error in saving products");
			},
		});
	});
	// as form is submitted run this
	$("#workon-task-form").submit(function (e) {
		// console.log("event submitting");
		e.preventDefault(); // avoid to execute the actual submit of the form.

		let form = $(this);

		//check values set
		for (let v of newForm.entries()) {
			console.log(v[0] + " - " + v[1]);
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
			success: function (num_of_prod_saved) {
				alert("Successfully saved " + num_of_prod_saved + " products");
			},
			error: function () {
				alert("error in saving products");
			},
		});
	});
});

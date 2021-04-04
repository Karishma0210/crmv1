$(document).ready(function () {
	let searchParams = new URLSearchParams(window.location.search);
	// console.log(searchParams.has("category"));
	if (searchParams.has("category")) {
		$("#cat-selector").val(searchParams.get("category").toString()).change();
		$("#products-btn").show();
	}
	// console.log(searchParams.get("category"));
	else {
		$("#products-btn").hide();
	}

	$(".competitor_value").change(function () {
		// console.log($(this).parents("tr").attr("id"));
		current_row = $(this).parents("tr");
		current_row
			.find('[name="minimum"]')
			.val(
				Math.min(
					current_row.find('[name="jumbo_virgin"]').val(),
					current_row.find('[name="sharafdg"]').val(),
					current_row.find('[name="carr_lulu"]').val(),
					current_row.find('[name="eros_axiom"]').val()
				)
			);
	});
});

function getCookie(name) {
	let cookieValue = null;
	if (document.cookie && document.cookie !== "") {
		const cookies = document.cookie.split(";");
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === name + "=") {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	// console.log("MY COOKIE" + cookieValue);
	return cookieValue;
}

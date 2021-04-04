let today = new Date();
document.getElementById("task-date").value = today.toISOString().slice(0, 10);
let minDate = new Date();
minDate.setDate(today.getDate());
document.getElementById("task-date").min = minDate.toISOString().slice(0, 10);

// let dum_deadline = new Date();
// dum_deadline.setDate(today.getDate());
// document.getElementById(
// 	"task-deadline"
// ).value = dum_deadline.toISOString().slice(0, 10);
document.getElementById("task-deadline").min = minDate
	.toISOString()
	.slice(0, 10);

function saveFile(absolute_path) {
    $.ajax({
	async: false,
	type : "POST",
	url : '/mde/save',
	dataType: "json",
	data: JSON.stringify({"saved_value": s.value(), "absolute_path": absolute_path}),
	contentType: 'application/json;charset=UTF-8',
	success: function (data) {
		console.log(data);
		}
	});
}
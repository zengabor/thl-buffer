var queue = []

var defer = function(queue) {
    if (! queue.length)
        return
    queue.shift()()
    setTimeout(defer, 250, queue)
}

function add_to_queue(href) {
	queue.unshift(function (){location.replace(href)})
}

function import_all() {
  ul = document.getElementById('tasks')
	if (ul && ul.tagName == 'UL') {
		var ils = ul.children
		for (var i = 0; i < ils.length; i++) {
			var li = ul.children[i]
			var a = li.children[2]
			add_to_queue(a.href)
		}
		defer(queue)
	}
}


function archive_task(anchor) {
	if (anchor && anchor.href && window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest()
		xmlhttp.open("PUT", anchor.href, false)
		xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded")
		xmlhttp.send("is_archived=1")
		anchor.parentNode.style.display = "none"
	}
}

function archive_all() {
  ul = document.getElementById('tasks')
	if (ul && ul.tagName == 'UL') {
		var ils = ul.children
		for (var i = 0; i < ils.length; i++) {
			var li = ul.children[i]
			var anchor = li.children[0]
			archive_task(anchor)
		}
		window.location.reload()
	} else {
	}
}


function delete_task(anchor) {
	if (anchor && anchor.href && window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest()
		xmlhttp.open("DELETE", anchor.href, false)
		xmlhttp.send()
		anchor.parentNode.style.display = "none"
	}
}


function delete_all() {
  ul = document.getElementById('tasks')
	if (ul && ul.tagName == 'UL') {
		var ils = ul.children
		for (var i = 0; i < ils.length; i++) {
			var li = ul.children[i]
			var anchor = li.children[0]
			delete_task(anchor)
		}
		window.location.reload()
	}
}


function grow(textarea) {
	var newHeight = textarea.scrollHeight;
	var currentHeight = textarea.clientHeight;
	if (newHeight > currentHeight && newHeight < 500) {
		textarea.style.height = newHeight + 50 + 'px';
	}
}

/*jslint browser: true*/
/*global $*/

function add_content(req) {
    var elem = document.getElementById("content");
    elem.innerHTML += req;
}

function replace_content(id, data) {
    var elem = document.getElementById(id);
    elem.outerHTML = data;
}

function get_rows(rows) {
    var fragment = "";
    rows.forEach(function (row) {
        var css_class = "hasNoProject";
        var task = row.title;
        var context = row.context;
        var uuid = 0;

        if (row.uuid !== null) {
            task = `<a draggable='false' href='things:///show?id=${row.uuid}' target='_blank'>${row.title}</a>`;
        }
        if (row.context_uuid !== null) {
            context = `<a draggable='false' href='things:///show?id=${row.context_uuid}' target='_blank'>` +
            `${row.context}</a>`;
        }
        if (row.context !== null) {
            css_class = "hasProject";
        } else {
            row.context = "No Context";
        }
        if (row.due !== null) {
            css_class = "hasDeadline";
        } else {
            row.due = "";
        }

        fragment += `<div class='box' draggable='false' ondragstart='onDragStart(event);' id='${row.uuid}'>` + task +
                    "<div class='deadline'>" + row.due + "</div>" +
                    "<div class='area " + css_class + "'>" +
                    context + "</div>" +
                    "</div>";
        });
    return fragment;
}

function setup_html_column(cssclass, header, number, query, help) {
    return "<div class='column' ondrop='onDrop(event);' ondragleave='onDragLeave(event);' ondragover='onDragOver(event);' id='"+header+"' title='"+help+"'>" +
               "  <div class=''>" +
               "     <a draggable='false' href='things:///show?" + query + "' target='_blank'><h2 class='" + cssclass + "'>" + header +
               "         <span class='size'>" + number + "</span>" +
               "     </h2></a>";
}

function add(color, title, data, query, help) {
    var rows = JSON.parse(data.response);
    var fragment = setup_html_column(color, title, rows.length, query, help);
    fragment += get_rows(rows);
    fragment += "</div></div>";
    if (document.getElementById(title) !== null) {
        replace_content(title, fragment);
    } else {
        document.getElementById('loading').style.display = "none";
        add_content(fragment);
    }
}

var makeRequest = function (url, method) {
    var request = new XMLHttpRequest();
    return new Promise(function (resolve, reject) {
        request.onreadystatechange = function () {
            if (request.readyState !== 4) {return;}
            if (request.status >= 200 && request.status < 300) {
                resolve(request);
            } else {
                reject({
                    status: request.status,
                    statusText: request.statusText
                });
            }
        };
        request.open(method || "GET", url, true);
        request.send();
    });
};

async function refresh() {
    await makeRequest("api/backlog").then(function (data) {add("color1", "Backlog", data, "id=someday", "tasks in someday projects");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
    await makeRequest("api/cleanup").then(function (data) {add("color8", "Grooming", data, "id=empty", "empty projects, tasks with no parent, items with tag 'Cleanup'");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
    await makeRequest("api/upcoming").then(function (data) {add("color5", "Upcoming", data, "id=upcoming", "scheduled tasks");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
    await makeRequest("api/waiting").then(function (data) {add("color3", "Waiting", data, "query=Waiting", "tasks with the tag 'Waiting'");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
    await makeRequest("api/inbox").then(function (data) {add("color4", "Inbox", data, "id=inbox", "tasks in the inbox");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
    await makeRequest("api/mit").then(function (data) {add("color2", "MIT", data, "query=MIT", "most important tasks with the tag 'MIT'");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
    await makeRequest("api/today").then(function (data) {add("color6", "Today", data, "id=today", "tasks for today");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
    await makeRequest("api/next").then(function (data) {add("color7", "Next", data, "id=anytime", "anytime tasks that are not in today");}).catch(function (result) { document.getElementById('loading').innerHTML = 'Error: ' + (result.statusText || 'no reply from database');})
}

function onDragStart(event) {
  event
    .dataTransfer
    .setData('text/plain', event.target.id);

    event
    .currentTarget
    .style
    .border = '2px solid green';
}

function onDragOver(event) {
  event.preventDefault();
  event
    .currentTarget
    .style
    .border = '2px solid red';
}

function onDragLeave(event) {
    event.preventDefault();
    event
    .currentTarget
    .style
    .border = '0';
}

function onDrop(event) {
    event.preventDefault();
    event
    .currentTarget
    .style
    .border = '0';
    
    const id = event
    .dataTransfer
    .getData('text');

  const draggableElement = document.getElementById(id);
  const dropzone = event.target;
  
  draggableElement
    .style
    .border = '0';

  dropzone.appendChild(draggableElement);

  event
    .dataTransfer
    .clearData();
    
    console.log(dropzone.id)
    //refresh();
}

window.onfocus = refresh;
window.onload = refresh;

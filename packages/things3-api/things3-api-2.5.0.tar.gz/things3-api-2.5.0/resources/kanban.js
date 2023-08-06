/* global XMLHttpRequest, Chart */

'use strict'

var view = null
var idxUUID = 'None'
var canvas = document.getElementById('canvas')
var mode = 'task'

function kanbanHide () { document.getElementById('content').style.display = 'none' }
function kanbanShow () { document.getElementById('content').style.display = '' }

const arrSum = arr => arr.reduce((a, b) => a + b, 0)

function kanbanUpdate () {
  console.log('Updating kanban...')
  view = kanbanUpdate
  statsHide()
  kanbanShow()
  if (canvas == null) {
    console.log('Requesting data...')
    requestParallel('api/areas', function (data) { contentReset('areas'); optionsAdd(data, 'areas') })
    requestParallel('api/projects', function (data) { contentReset('projects'); optionsAdd(data, 'projects') })
    requestParallel('api/inbox', function (data) { rowsAdd('color4', 'Inbox', data, 'id=inbox', 'tasks in the inbox', 'i') })
    requestParallel('api/today', function (data) { rowsAdd('color6', 'Today', data, 'id=today', 'tasks for today', 't') })
    requestParallel('api/waiting', function (data) { rowsAdd('color3', 'Waiting', data, 'query=Waiting', 'tasks with the tag "Waiting"', 'w') })
    requestParallel('api/mit', function (data) { rowsAdd('color2', 'MIT', data, 'query=MIT', 'most important tasks with the tag "MIT"', 'm') })
    requestParallel('api/upcoming', function (data) { rowsAdd('color5', 'Upcoming', data, 'id=upcoming', 'scheduled tasks', 'u') })
    requestParallel('api/cleanup', function (data) { rowsAdd('color8', 'Grooming', data, 'id=empty', 'empty projects, tasks with no parent, items with tag "Cleanup"', '') })
    requestParallel('api/next', function (data) { rowsAdd('color7', 'Next', data, 'id=anytime', 'anytime tasks that are not in today', 'n') })
    requestParallel('api/backlog', function (data) { rowsAdd('color1', 'Backlog', data, 'id=someday', 'tasks in someday projects', 'b') })
  }
}

function contentReset (id) {
  var filter = document.getElementById(id)
  filter.innerHTML = ''
}

function optionAdd (list, title, uuid) {
  var entry = document.createElement('option')
  entry.setAttribute('value', uuid)
  if (idxUUID === uuid) { entry.setAttribute('selected', 'selected') }
  entry.innerHTML = title
  list.appendChild(entry)
}

function optionsAdd (data, id) {
  var filter = document.getElementById(id)
  var items = JSON.parse(data.response)
  items.forEach(function (item) {
    optionAdd(filter, '&nbsp;&nbsp;&nbsp;○ ' + item.title, item.uuid)
  })
}

function contentAdd (req) {
  var elem = document.getElementById('content')
  elem.innerHTML += req
}

function contentReplace (id, data) {
  var elem = document.getElementById(id)
  elem.outerHTML = data
}

function rowsGet (rows) {
  var fragment = ''
  rows.forEach(function (row) {
    var cssClass = 'hasNoProject'
    var task = row.title
    var context = row.context

    if (row.type === 'project') {
      task = `${task} (${row.size})`
    }

    if (row.uuid !== null) {
      task = `<a draggable='false' href='things:///show?id=${row.uuid}'
                       target='_blank'>${task}
                    </a>`
    }
    if (row.context_uuid !== null) {
      context = `<a draggable='false' 
                          href='things:///show?id=${row.context_uuid}' 
                          target='_blank'>
                          ${row.context}
                        </a>`
    }
    if (row.context !== null) {
      cssClass = 'hasProject'
    } else {
      row.context = 'No Context'
    }
    if (row.due !== null) {
      cssClass = 'hasDeadline'
    } else {
      row.due = ''
    }

    fragment += `<div class='box' draggable='false' 
                          ondragstart='onDragStart(event);' 
                          id='${row.uuid}'>${task}
                        <div class='deadline'>${row.due}</div>
                        <div class='area ${cssClass}'>${context}</div>
                    </div>`
  })
  return fragment
}

function columnAddPreview (cssclass, header) {
  return `<div class='column' id='${header}'>
                <div class='inner-column'>
                    <h2 class='h2 ${cssclass}'>
                        ${header}<span class='size'></span>
                    </h2>
                </div>
            </div>`
}

function rowsAdd (color, title, data, query, help, shortcut) {
  var rows = JSON.parse(data.response)
  var rowHTML = rowsGet(rows)
  var fragment = `
        <div class='column' 
            ondrop='onDrop(event);'
            ondragleave='onDragLeave(event);'
            ondragover='onDragOver(event);'
            id='${title}' title='${help}'>
            <div class='inner-column'>
                <a draggable='false' 
                    href='things:///show?${query}'
                    target='_blank'
                    accesskey='${shortcut}'
                    title='⌃+⎇+${shortcut}'>
                    <h2 class='h2 ${color}'>${title}
                        <span class='size'>${rows.length}</span>
                    </h2>
                </a>
                ${rowHTML}
            </div>
        </div>`

  if (document.getElementById(title) !== null) {
    contentReplace(title, fragment)
  } else {
    document.getElementById('loading').style.display = 'none'
    contentAdd(fragment)
  }
}

var requestParallel = function (url, method) {
  var request = new XMLHttpRequest()
  request.onreadystatechange = function () {
    if (request.readyState !== 4) { return }
    if (request.status >= 200 && request.status < 300) {
      method(request)
    } else {
      console.log('Error: ' + request.status)
    }
  }
  request.open('GET', `${url}?mode=${mode}`, true)
  request.send()
}

var requestSequencial = function (url, method) {
  var request = new XMLHttpRequest()
  return new Promise(function (resolve, reject) {
    request.onreadystatechange = function () {
      if (request.readyState !== 4) { return }
      if (request.status >= 200 && request.status < 300) {
        resolve(request)
      } else {
        reject(new Error(request.statusText))
      }
    }
    request.open(method || 'GET', `${url}?mode=${mode}`, true)
    request.send()
  })
}

function refresh () {
  var idx = document.getElementById('filter').selectedIndex
  console.log('Refresh: ', idx)
  if (idx >= 0) {
    var func = document.getElementById('filter').options[idx].dataset.function
    if (func != null) {
      return eval(func).call() // eslint-disable-line no-eval
    }
  }
  console.log('View is null: ', view == null)
  if (view != null) {
    view()
  } else {
    kanbanUpdate()
  }
}

function onDragStart (event) { // eslint-disable-line no-unused-vars
  event
    .dataTransfer
    .setData('text/plain', event.target.id)

  event
    .currentTarget
    .style
    .border = '2px solid green'
}

function onDragOver (event) { // eslint-disable-line no-unused-vars
  event.preventDefault()
  event
    .currentTarget
    .style
    .border = '2px solid red'
}

function onDragLeave (event) { // eslint-disable-line no-unused-vars
  event.preventDefault()
  event
    .currentTarget
    .style
    .border = '0'
}

function onDrop (event) { // eslint-disable-line no-unused-vars
  // not completely implemented yet
  event.preventDefault()
  event
    .currentTarget
    .style
    .border = '0'

  const id = event
    .dataTransfer
    .getData('text')

  const draggableElement = document.getElementById(id)
  const dropzone = event.target

  draggableElement
    .style
    .border = '0'

  dropzone.appendChild(draggableElement)

  event
    .dataTransfer
    .clearData()

  console.log(dropzone.id)
  // refresh();
}

function switchMode (event) { // eslint-disable-line no-unused-vars
  var taskMode = document.getElementById('mode').checked
  if (taskMode === true) {
    mode = 'task'
  } else {
    mode = 'project'
  }
  refresh()
}

function kanbanFilterChange (event) { // eslint-disable-line no-unused-vars
  var idx = document.getElementById('filter').selectedIndex
  if (idx >= 0) {
    var option = document.getElementById('filter').options[idx]
    var uuid = option.value
    var filterType = option.parentNode.dataset.ctx
    if (uuid != null) {
      idxUUID = uuid
      console.log('Index: ', idx, idxUUID, filterType)

      if (idxUUID !== 'None' && filterType != null) {
        requestParallel('api/filter/' + filterType + '/' + idxUUID, refresh)
      } else {
        idxUUID = 'None'
        kanbanFilterReset()
      }
      kanbanUpdate()
    }
  }
}

function kanbanFilterReset () {
  requestParallel('api/filter/reset', refresh)
}

function statsHide () {
  document.getElementById('stats').style.display = 'none'
}
function statsShow () {
  document.getElementById('stats').style.display = ''
}
function statsReplace (canv) {
  contentReset('stats')
  document.getElementById('stats').appendChild(canv)
}
function canvasCreate () {
  var canvas = document.createElement('canvas')
  canvas.id = 'canvas'
  canvas.className = 'canvas'
  return canvas
}

async function statsShowDistribution () { // eslint-disable-line no-unused-vars
  view = statsShowDistribution
  kanbanHide()
  statsShow()
  var canv = canvasCreate()
  statsReplace(canv)

  var ctx = canv.getContext('2d')
  var backlog = 0
  await requestSequencial('api/backlog').then(function (data) {
    backlog = JSON.parse(data.response).length
  })
  var upcoming = 0
  await requestSequencial('api/upcoming').then(function (data) {
    upcoming = JSON.parse(data.response).length
  })
  var inbox = 0
  await requestSequencial('api/inbox').then(function (data) {
    inbox = JSON.parse(data.response).length
  })
  var today = 0
  await requestSequencial('api/today').then(function (data) {
    today = JSON.parse(data.response).length
  })
  var next = 0
  await requestSequencial('api/next').then(function (data) {
    next = JSON.parse(data.response).length
  })
  new Chart(ctx, { // eslint-disable-line no-new
    type: 'doughnut',
    options: {
      plugins: {
        labels: {
          render: 'percentage',
          precision: 0,
          position: 'outside',
          arc: true
        }
      }
    },
    data: {
      labels: [`Backlog (${backlog})`, `Upcoming (${upcoming})`, `Inbox  (${inbox})`, `Today (${today})`, `Next  (${next})`],
      datasets: [
        {
          label: '# of tasks',
          data: [backlog, upcoming, inbox, today, next],
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 1
        }
      ]
    }
  })
}

async function statsShowMinutes () { // eslint-disable-line no-unused-vars
  view = statsShowMinutes
  kanbanHide()
  statsShow()

  var canv = document.createElement('div')
  canv.id = 'canvas'
  canv.className = 'canvas big-text container'
  statsReplace(canv)

  await requestSequencial('api/stats-min-today').then(function (data) {
    var jsonfile = JSON.parse(data.response)
    var minutes = jsonfile[0].minutes
    if (minutes == null) {
      canv.innerHTML = 'no time estimations'
    } else if (minutes === '1') {
      canv.innerHTML = minutes + ' minute'
    } else {
      canv.innerHTML = minutes + ' minutes'
    }

    canv.title = 'use tags named after plain numbers'
  })
}

async function statsShowUniverse () { // eslint-disable-line no-unused-vars
  view = statsShowUniverse
  kanbanHide()
  statsShow()
  var canv = canvasCreate()
  statsReplace(canv)
  var ctx = canv.getContext('2d')

  await requestSequencial('api/top-proj').then(function (data) {
    var jsonfile = JSON.parse(data.response)

    var labels = jsonfile.map(function (e) {
      return e.title
    })
    var uuids = jsonfile.map(function (e) {
      return e.uuid
    })
    var x = jsonfile.map(function (e) {
      return e.created
    })
    var y = jsonfile.map(function (e) {
      return e.modified
    })
    var r = jsonfile.map(function (e) {
      return e.tasks
    })

    var xMax = Math.max(...x)
    var yMax = Math.max(...y)
    var rMax = Math.max(...r)
    var chartData = []

    for (var i = 0; i < labels.length; i++) {
      var chartDataset = {
        label: labels[i],
        backgroundColor: 'rgba(' + (r[i] / rMax) * 250 + ', 150, 0, 0.5)',
        borderColor: 'rgba(150, 150, 0, 1)',
        borderWidth: 1,
        hoverBorderWidth: 2,
        rotation: uuids[i],
        data: [
          {
            x: (x[i] / xMax) * 10,
            y: (y[i] / yMax) * 10,
            r: (r[i] / rMax) * 50
          }
        ]
      }

      chartData.push(chartDataset)
    }

    var dataset = { datasets: chartData }
    var options = {
      title: { display: true, text: 'project size vs. age' },
      legend: { display: false },
      scales: {
        yAxes: [
          {
            scaleLabel: { display: true, labelString: 'age [modified]' },
            ticks: { display: false, max: 10.1 }
          }
        ],
        xAxes: [
          {
            scaleLabel: { display: true, labelString: 'age [created]' },
            ticks: { display: false, max: 10.5 }
          }
        ]
      }
    }

    const chart = new Chart(ctx, { // eslint-disable-line no-new
      type: 'bubble',
      data: dataset,
      options: options
    })
    document.getElementById('canvas').addEventListener('click', function (evt) {
      var activePoint = chart.getDatasetAtEvent(evt)
      var uuid = activePoint[0]._options.rotation
      const a = document.createElement('a')
      a.target = '_blank'
      a.href = `things:///show?id=${uuid}`
      a.click()
    })
  })
}

async function statsShowHistory () { // eslint-disable-line no-unused-vars
  view = statsShowHistory
  kanbanHide()
  statsShow()
  var canv = canvasCreate()
  statsReplace(canv)

  await requestSequencial('api/stats-day').then(function (data) {
    var jsonfile = JSON.parse(data.response)

    var labels = jsonfile.map(function (e) {
      return e.date
    })
    var created = jsonfile.map(function (e) {
      return e.created
    })
    var cancelled = jsonfile.map(function (e) {
      return e.cancelled
    })
    var completed = jsonfile.map(function (e) {
      return e.completed
    })
    var trashed = jsonfile.map(function (e) {
      return e.trashed
    })

    var ctx = canv.getContext('2d')
    var config = {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'created (' + arrSum(created) + ')',
            data: created,
            backgroundColor: 'rgba(0, 119, 204, 0.5)',
            borderColor: 'rgba(0, 119, 204, 1)',
            borderWidth: 1
          },
          {
            label: 'completed (' + arrSum(completed) + ')',
            data: completed,
            backgroundColor: 'rgba(0, 204, 119, 0.5)',
            borderColor: 'rgba(0, 204, 119, 1)',
            borderWidth: 1
          },
          {
            label: 'cancelled (' + arrSum(cancelled) + ')',
            data: cancelled,
            backgroundColor: 'rgba(204, 119, 0, 0.5)',
            borderColor: 'rgba(204, 119, 0, 1)',
            borderWidth: 1
          },
          {
            label: 'trashed (' + arrSum(trashed) + ')',
            data: trashed,
            backgroundColor: 'rgba(204, 0, 119, 0.5)',
            borderColor: 'rgba(204, 0, 119, 1)',
            borderWidth: 1
          }
        ]
      },
      options: {
        plugins: {
          labels: false
        },
        scales: {
          xAxes: [
            {
              stacked: true
            }
          ],
          yAxes: [
            {
              stacked: true
            }
          ]
        }
      }
    }
    new Chart(ctx, config) // eslint-disable-line no-new
  })
}

window.onload = function () {
  contentAdd(columnAddPreview('color1', 'Backlog'))
  contentAdd(columnAddPreview('color8', 'Grooming'))
  contentAdd(columnAddPreview('color5', 'Upcoming'))
  contentAdd(columnAddPreview('color3', 'Waiting'))
  contentAdd(columnAddPreview('color4', 'Inbox'))
  contentAdd(columnAddPreview('color2', 'MIT'))
  contentAdd(columnAddPreview('color6', 'Today'))
  contentAdd(columnAddPreview('color7', 'Next'))
  document.getElementById('filter').selectedIndex = 0
  document.getElementById('filter').focus()
  document.getElementById('filter').click()
  refresh()
}
window.onfocus = refresh

function deleteTask(taskId) {
  fetch("/delete-task", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/kanban";
  });
}

function moveTask(taskId, newStatus) {
console.log(newStatus)
fetch("/move-task", {
  method: "POST",
  body: JSON.stringify({ taskId: taskId, newStatus: newStatus }),
}).then((_res) => {
  window.location.href = "/kanban";
});
}
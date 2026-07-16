function TaskCard({ task, onUpdateTask, onDeleteTask }) {
  async function handleStatusChange(event) {
    await onUpdateTask(task.id, {
      status: event.target.value,
    });
  }

  async function handlePriorityChange(event) {
    await onUpdateTask(task.id, {
      priority: event.target.value,
    });
  }

  return (
    <article className="task-card">
      <div>
        <h3>{task.title}</h3>
        <p>{task.description || "No description added."}</p>

        <div className="task-controls">
          <label>
            Status
            <select value={task.status} onChange={handleStatusChange}>
              <option value="Not Started">Not Started</option>
              <option value="In Progress">In Progress</option>
              <option value="Complete">Complete</option>
            </select>
          </label>

          <label>
            Priority
            <select value={task.priority} onChange={handlePriorityChange}>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </label>
        </div>
      </div>

      <button className="danger-button" onClick={() => onDeleteTask(task.id)}>
        Delete Task
      </button>
    </article>
  );
}

export default TaskCard;
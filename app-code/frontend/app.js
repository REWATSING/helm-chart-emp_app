fetch('/api/employees')
  .then(res => res.json())
  .then(data => {
    const list = document.getElementById('emp-list');
    data.forEach(emp => {
      const li = document.createElement('li');
      li.innerText = `${emp.id}: ${emp.name}`;
      list.appendChild(li);
    });
  });

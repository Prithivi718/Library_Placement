// script.js - simple DOM + fetch wiring
// Use the FastAPI server if we're not already on it (e.g., Live Server)
const API_BASE =
  window.API_BASE ||
  (window.location.port === '8000' ? '' : 'http://127.0.0.1:8000');
const api = (path, opts) => fetch(`${API_BASE}/api${path}`, opts).then(r => r.json());

async function refreshBooks() {
  const out = document.getElementById('books-list');
  out.innerText = 'Loading...';
  const res = await api('/books');
  if (!res.ok) { out.innerText = 'Failed to load'; return; }
  const books = res.books;
  if (books.length === 0) { out.innerHTML = '<div class="small-muted">No books yet</div>'; return; }
  let html = '<table><thead><tr><th>ID</th><th>Title</th><th>Author</th><th>Avail/Total</th></tr></thead><tbody>';
  books.forEach(b => {
    html += `<tr><td>${b.id}</td><td>${escapeHtml(b.title)}</td><td>${escapeHtml(b.author)}</td><td>${b.available_copies}/${b.total_copies}</td></tr>`;
  });
  html += '</tbody></table>';
  out.innerHTML = html;
  populateBookSelect(books);
}

async function refreshUsers() {
  const sel = document.getElementById('user-select');
  const res = await api('/users');
  if (!res.ok) return;
  const users = res.users;
  sel.innerHTML = '<option value="">Select user</option>';
  users.forEach(u => {
    const opt = document.createElement('option');
    opt.value = u.id; opt.textContent = `${u.name} (${u.email || 'no email'})`;
    sel.appendChild(opt);
  });
}

async function refreshIssued() {
  const out = document.getElementById('issued-list');
  out.innerText = 'Loading...';
  const res = await api('/issued');
  if (!res.ok) { out.innerText = 'Failed to load'; return; }
  const iss = res.issued;
  if (iss.length === 0) { out.innerHTML = '<div class="small-muted">No issued books</div>'; return; }
  let html = '<ul>';
  iss.forEach(i => {
    html += `<li>Issue#${i.id}: <strong>${escapeHtml(i.book_title)}</strong> to ${escapeHtml(i.user_name)} — ${i.returned ? '<span class="small-muted">Returned</span>' : 'Issued'}</li>`;
  });
  html += '</ul>';
  out.innerHTML = html;
}

function populateBookSelect(books) {
  const sel = document.getElementById('book-select');
  sel.innerHTML = '<option value="">Select book</option>';
  books.forEach(b => {
    const opt = document.createElement('option');
    opt.value = b.id;
    opt.textContent = `${b.title} (${b.available_copies} avail)`;
    sel.appendChild(opt);
  });
}

function escapeHtml(s){ return String(s).replace(/[&<>"']/g, (m)=>({ '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;' }[m])); }

// Form handlers
document.getElementById('add-book-form').addEventListener('submit', async e => {
  e.preventDefault();
  const title = document.getElementById('book-title').value.trim();
  const author = document.getElementById('book-author').value.trim();
  const copies = parseInt(document.getElementById('book-copies').value) || 1;
  if (!title || !author) return alert('Fill title & author');
  const res = await api('/books', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({title, author, total_copies: copies})
  });
  if (res.ok) {
    document.getElementById('book-title').value = '';
    document.getElementById('book-author').value = '';
    document.getElementById('book-copies').value = '1';
    refreshBooks();
  } else {
    alert('Failed to add');
  }
});

document.getElementById('add-user-form').addEventListener('submit', async e => {
  e.preventDefault();
  const name = document.getElementById('user-name').value.trim();
  const email = document.getElementById('user-email').value.trim();
  if (!name) return alert('Please enter name');
  const res = await api('/users', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({name, email: email || null})
  });
  if (res.ok) {
    document.getElementById('user-name').value = '';
    document.getElementById('user-email').value = '';
    refreshUsers();
  } else {
    alert('Failed to register');
  }
});

document.getElementById('issue-btn').addEventListener('click', async () => {
  const userId = document.getElementById('user-select').value;
  const bookId = document.getElementById('book-select').value;
  if (!userId || !bookId) return alert('Select user and book');
  const res = await api('/issue', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({user_id: Number(userId), book_id: Number(bookId)})
  });
  if (res.ok) {
    refreshBooks(); refreshIssued();
  } else {
    alert(res.detail || 'Issue failed');
  }
});

document.getElementById('return-btn').addEventListener('click', async () => {
  const id = Number(document.getElementById('return-issue-id').value);
  if (!id) return alert('Enter issue id');
  const res = await api('/return', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({issue_id: id})
  });
  if (res.ok) {
    refreshBooks(); refreshIssued();
  } else {
    alert(res.detail || 'Return failed');
  }
});

// initial load
refreshBooks();
refreshUsers();
refreshIssued();

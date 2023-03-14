const comments = document.querySelectorAll('.comment')

comments.forEach(comment => {
  const depth = comment.getAttribute('data-depth');
  comment.style.setProperty('--indent-level', depth);
});

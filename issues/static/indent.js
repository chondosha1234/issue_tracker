const comments = document.querySelectorAll('.comment')

console.log(comments)

comments.forEach(comment => {
  const depth = comment.getAttribute('data-depth');
  comment.style.setProperty('--indent-level', depth);
});

const edit_links = document.querySelectorAll('[id^="edit-link-"]');

edit_links.forEach(link => {
  link.addEventListener("click", function() {
    this.classList.toggle("active");
    let id = link.id.substring(10);
    let text_name = 'comment-text-' + id;
    let form_name = 'comment-form-' + id;
    let comment_text = document.getElementsByClassName(text_name)[0];
    let comment_form = document.getElementsByClassName(form_name)[0];

    console.log(comment_text);
    console.log(comment_form);
    if (comment_form.style.display === 'none'){
      comment_form.style.display = 'block';
      comment_text.style.display = 'none';
    } else {
      comment_form.style.display = 'none';
      comment_text.style.display = 'block';
    }

  });
});

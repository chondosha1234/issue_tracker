const add_user = document.getElementById('add-user');
const remove_user = document.getElementById('remove-user');
const reply_links = document.querySelectorAll('[id^="reply-link-"]');

add_user.addEventListener("click", function() {
  this.classList.toggle("active");
  let content = document.getElementsByClassName('add-form')[0];
  if (content.style.display === "block"){
    content.style.display = "none";
  } else {
    content.style.display = "block";
  }
});

remove_user.addEventListener("click", function() {
  this.classList.toggle("active");
  let content = document.getElementsByClassName('remove-form')[0];
  if (content.style.display === "block"){
    content.style.display = "none";
  } else {
    content.style.display = "block";
  }
});

reply_links.forEach(link => {
  link.addEventListener("click", function() {
    this.classList.toggle("active");
    //get the id of parent from class name
    let class_name = 'reply-form-' + link.id.substring(11);
    let content = document.getElementsByClassName(class_name)[0];
    console.log(content)
    if (content.style.display === "block"){
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
})

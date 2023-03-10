const add_user = document.getElementById('add-user');
const remove_user = document.getElementById('remove-user');

add_user.addEventListener("click", function() {
  this.classList.toggle("active");
  let content = document.getElementsByClassName('add-form')[0]
  if (content.style.display === "block"){
    content.style.display = "none";
  } else {
    content.style.display = "block";
  }
});

remove_user.addEventListener("click", function() {
  this.classList.toggle("active");
  let content = document.getElementsByClassName('remove-form')[0]
  if (content.style.display === "block"){
    content.style.display = "none";
  } else {
    content.style.display = "block";
  }
});

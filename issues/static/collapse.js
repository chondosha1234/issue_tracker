const add_user = document.getElementById('add-user');
const remove_user = document.getElementById('remove-user');
const reply_links = document.querySelectorAll('[id^="reply-link-"]');
const hide_replies = document.querySelectorAll('[id^="hide-replies-"]')

if(add_user){
  add_user.addEventListener("click", function(element) {
    this.classList.toggle("active");
    element.stopPropagation();
    let content = document.getElementsByClassName('add-form')[0];
    if (content.style.display === "block"){
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

if(remove_user){
  remove_user.addEventListener("click", function(element) {
    this.classList.toggle("active");
    element.stopPropagation();
    let content = document.getElementsByClassName('remove-form')[0];
    if (content.style.display === "block"){
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}

reply_links.forEach(link => {
  link.addEventListener("click", function() {
    this.classList.toggle("active");
    //get the id of parent from class name
    let class_name = 'reply-form-' + link.id.substring(11);
    let content = document.getElementsByClassName(class_name)[0];
    if (content.style.display === "block"){
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
})

hide_replies.forEach(link => {
  link.addEventListener("click", function() {
    console.log("inside click function")
    this.classList.toggle("active");
    let class_name = 'reply-tree-' + link.id.substring(13);
    let content = document.getElementsByClassName(class_name)[0];

    if (content.style.display === "block"){
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }

    let str = link.innerHTML;
    let last_char = str.length - 1;

    if (link.innerHTML[last_char] === "\u2193"){  //unicode for down arrow
      new_str = str.slice(0, -1) + "\u2191";  // unicode for up arrow
      link.innerHTML = new_str;
    } else {
      new_str = str.slice(0, -1) + "\u2193";
      link.innerHTML = new_str;
    }

  });
})

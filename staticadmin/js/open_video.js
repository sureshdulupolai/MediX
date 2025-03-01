function toggleLike() {
    let likeBtn = document.getElementById("likeBtn");
    let dislikeBtn = document.getElementById("dislikeBtn");
    
    if (likeBtn.classList.contains("active")) {
        likeBtn.classList.remove("active");
    } else {
        likeBtn.classList.add("active");
        dislikeBtn.classList.remove("active");
    }
}

function toggleDislike() {
    let likeBtn = document.getElementById("likeBtn");
    let dislikeBtn = document.getElementById("dislikeBtn");
    
    if (dislikeBtn.classList.contains("active")) {
        dislikeBtn.classList.remove("active");
    } else {
        dislikeBtn.classList.add("active");
        likeBtn.classList.remove("active");
    }
}

function toggleSubscribe() {
    let subscribeBtn = document.getElementById("subscribeBtn");
    
    if (subscribeBtn.classList.contains("btn-primary")) {
        subscribeBtn.classList.remove("btn-primary");
        subscribeBtn.classList.add("btn-danger");
        subscribeBtn.textContent = "Unsubscribe";
    } else {
        subscribeBtn.classList.remove("btn-danger");
        subscribeBtn.classList.add("btn-primary");
        subscribeBtn.textContent = "Subscribe";
    }
}

function showShareBox() {
    document.getElementById("overlay").style.display = "flex";
    document.body.classList.add("no-scroll"); // Prevent scrolling
}

function closeShareBox() {
    document.getElementById("overlay").style.display = "none";
    document.body.classList.remove("no-scroll"); // Restore scrolling
}


function addComment() {
    let commentInput = document.getElementById("commentInput");
    let commentText = commentInput.value.trim();

    if (commentText === "") {
        alert("Comment cannot be empty!");
        return;
    }

    let commentList = document.getElementById("commentList");

    // Create new list item
    let newComment = document.createElement("li");
    newComment.className = "list-group-item d-flex justify-content-between align-items-center";
    newComment.innerHTML = `
        ${commentText}
        <div>
            <button class="btn btn-sm btn-warning" onclick="editComment(this)">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="deleteComment(this)">Delete</button>
        </div>
    `;

    // Append new comment
    commentList.appendChild(newComment);
    commentInput.value = ""; // Clear input field
}

function deleteComment(button) {
    let commentItem = button.parentElement.parentElement;
    commentItem.remove();
}

function editComment(button) {
    let commentItem = button.parentElement.parentElement;
    let currentText = commentItem.firstChild.textContent.trim();
    let newText = prompt("Edit your comment:", currentText);

    if (newText !== null && newText.trim() !== "") {
        commentItem.firstChild.textContent = newText;
    }
}




function toggleComments() { 
    let commentSection = document.getElementById("commentSection");
    commentSection.style.display = (commentSection.style.display === "none" || commentSection.style.display === "") ? "block" : "none"; 
} // Highlighted: Toggle Comments Visibility

function addComment() { // Highlighted: Add Comment Function
    let commentInput = document.getElementById("commentInput");
    let commentText = commentInput.value.trim();

    if (commentText === "") {
        alert("Comment cannot be empty!");
        return;
    }

    let commentList = document.getElementById("commentList");

    // Create new list item
    let newComment = document.createElement("li");
    newComment.className = "list-group-item d-flex justify-content-between align-items-center";
    newComment.innerHTML = `
        ${commentText}
        <div>
            <button class="btn btn-sm btn-warning" onclick="editComment(this)">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="deleteComment(this)">Delete</button>
        </div>
    `;

    // Append new comment
    commentList.appendChild(newComment);
    commentInput.value = ""; // Clear input field
}

function deleteComment(button) { // Highlighted: Delete Comment Function
    let commentItem = button.parentElement.parentElement;
    commentItem.remove();
}

function editComment(button) { // Highlighted: Edit Comment Function
    let commentItem = button.parentElement.parentElement;
    let currentText = commentItem.firstChild.textContent.trim();
    let newText = prompt("Edit your comment:", currentText);

    if (newText !== null && newText.trim() !== "") {
        commentItem.firstChild.textContent = newText;
    }
}
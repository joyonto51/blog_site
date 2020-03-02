$(document).ready(function () {
    $('.link-text').css('color', '#05c7f7');
    var token = $('#csrf_token').val();
    var totalComment = parseInt($('#comments_count').text());
    var body = $('body');
    var article_id = $('#article_id').val();
    var commentAddURL = $('#url').val();
    var commentDeleteURL = '/article/comment/delete/';
    var commentUpdateURL = '/article/comment/update/';


    // =============== Comment Generator Function ===============

    function getComment(data){
        return `<div class="comment clearfix">
                    <div class="row">
                        <img src="${data.avatar}"  alt="" class="profile_pic">
                        <strong class="mt-1 ml-2">${data.author}</strong>
                        <div class="comment-text ml-5">
                            <span class="comment-name">${data.text}</span>
                        </div>
                    </div>

                    <div class="comment-details">
                        <span class="comment-date">${data.created_at}</span>
                        <a class="reply-btn text-info" data-id="${data.id}">Reply</a>
                        <a comment-type="comment" class="comment-edit-btn edit-btn" data-id="${data.id}">Edit</a>
                        <a comment-type="comment" class="comment-delete-btn text-danger" data-id="${data.id}">Delete</a>
                    </div>
                    
                    <div class="replies replies_wrapper_${data.id}"></div>
       
                    <!-- reply form --> 
                    <form action="" class="reply_form clearfix" id="comment_reply_form_${data.id}">
                        <label for="reply_text"></label><textarea class="form-control" name="reply_text" id="reply_text" cols="30" rows="2"></textarea>
                        <button class="btn btn-primary btn-xs pull-right submit-reply" parent-id="${data.id}">Submit</button>
                    </form>
                </div>`
    }


    // ================ Comment Add =================

    // When user clicks on submit comment to add comment under post
    body.on('click', '#submit_comment', function(e) {
        e.preventDefault();
        var form = $('#comment_form');
        var comment_box = $('#comment_text');

        var comment_text = comment_box.val();
        var article_id = form.attr('article-id');

        // Stop executing if not value is entered
        if (comment_text !== "" ){
            var data = {
                "text": comment_text,
                "article_id": article_id
            };
            console.log(data)
        }

        $.ajax({
            url: commentAddURL,
            type: "POST",
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", token);
            },
            data: data,

            success: function(data){
                // var response = JSON.parse(data);
                if (data === "error") {
                    alert('There was an error adding comment. Please try again');
                }
                else {
                    totalComment += 1;

                    $('#comments-wrapper').prepend(getComment(data));
                    $('#comments_count').text(totalComment);
                    $('#comment_text').val('');
                }
            }
        });
    });


    // =============== Reply Generator Function =================

    function getReply(data){
        return `<div class="comment reply clearfix mt-2">
                    <div class="row col-md-8 reply-div">
                        <img src="${data.avatar}" alt="" class="profile_pic">
                        <div class="reply-text mt-1 mt-2">
                            <strong>${data.author}</strong>
                            <span class="comment-name reply">${data.text}</span>
                        </div>
                    </div>

                    <div class="comment-details">
                        <span class="comment-date">${data.created_at}</span>
                            <a comment-type="reply" class="comment-edit-btn edit-btn" data-id="${data.id}">Edit</a>
                            <a comment-type="reply" class="comment-delete-btn text-danger" data-id="${data.id}">Delete</a>
                    </div>
                </div>`

    }


    //  =============== Reply Add ====================

    // When user clicks on submit reply to add reply under comment
    body.on('click', '.reply-btn', function(e){
        e.preventDefault();
        // Get the comment id from the reply button's data-id attribute
        let comment_id = $(this).attr('data-id');

        // show/hide the appropriate reply form (from the reply-btn (this), go to the parent element (comment-details)
        // and then its siblings which is a form element with id comment_reply_form_ + comment_id)
        replyDiv = $(this).parent().siblings('div.replies_wrapper_' + comment_id);
        replyDiv.toggle(500);

        $(this).parent().siblings('form#comment_reply_form_' + comment_id).toggle(500);

        $(document).on('click', '.submit-reply', function(e){
            e.preventDefault();
            // elements
            let commentId = $(this).attr('parent-id');
            replyDiv = $(this).parent().siblings('div.replies_wrapper_' + commentId);

            let reply_textarea = $(this).siblings('textarea'); // reply textarea element
            let reply_text = $(this).siblings('textarea').val();

            if (reply_text !==''){
                var data = {
                    "text": reply_text,
                    "article_id": article_id,
                    "parent_id": commentId
                }
            }
            else return;

            $.ajax({
                url: commentAddURL,
                type: "POST",
                async: false,
                beforeSend: function (request) {
                    request.setRequestHeader("X-CSRFToken", token);
                },
                data: data,

                success: function(data){
                    if (data === "error") {
                        alert('There was an error adding reply. Please try again');
                    } else {
                        // console.log(getReply(data));
                        replyDiv.append(getReply(data));
                        reply_textarea.val('');
                    }
                }
            });
        });
    });


    // ================ Comment Delete ================

    body.on('click', '.comment-delete-btn', function (e) {
        e.preventDefault();
        commentDeleteBtn = $(this);

        $('#delete-comment-id').val(commentDeleteBtn.attr('data-id'));
        let type = $(this).attr('comment-type');

        console.log(type);

        // showing the modal
        modal = $("div#comment-delete-modal");
        modal.modal("show");

        // body.on('click', '#comment-delete', function (e) {
        $('#comment-delete').off().on('click', function () {
            commentId = $('#delete-comment-id').val();

            e.preventDefault();

            if (commentId !==''){
                let data = {
                    "comment_id": commentId
                };

                console.log(data);

                $.ajax({
                    url: commentDeleteURL,
                    type: "POST",
                    async: false,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", token);
                    },
                    data: data,

                    complete: function() {
                        if (type === 'comment') {
                            totalComment -= 1;
                            $('#comments_count').text(totalComment);
                        }
                        commentDeleteBtn.parent('div.comment-details').parent('div.comment').remove();

                        // dismiss the modal
                        modal.modal('hide')
                    }
                });
            }
            else alert("Comment not found");
        })

    });

    //  Comment Edit
    body.on('click', '.comment-edit-btn', function (e) {
        e.preventDefault();
        // Comment Data
        let commentEditBtn = $(this);
        let type = commentEditBtn.attr('comment-type');
        let commentId = commentEditBtn.attr('data-id');

        // console.log(type, commentId);

        if(type === "comment"){
            commentText = commentEditBtn.parent().parent().find("div.comment-text").find("span.comment-name");
        }
        else if(type === "reply"){
            commentText = commentEditBtn.parent().siblings('div.reply-div').find("div.reply-text").find("span.reply");
        }

        // console.log(commentText.text());

        // Modal Attributes
        let modal = $("div#comment-edit-modal");
        let modalCommentText = $('#comment-edit-text');

        // showing the modal
        modalCommentText.val(commentText.text());
        modal.modal("show");

        body.on('click', '#comment-edit', function (e) {
            let newCommentText = modalCommentText.val();

            if (commentId !=='' && newCommentText !== '' ){
                let data = {
                    "comment_id": commentId,
                    "text": newCommentText
                };

                $.ajax({
                    url: commentUpdateURL,
                    type: "POST",
                    async: false,
                    beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", token);
                    },
                    data: data,

                    success: function(data, textStatus, xhr){

                        if (xhr.status !== 200) {
                            alert('There was an error.');
                        }
                        else {
                            commentText.text(newCommentText);
                            modal.modal('hide')
                        }
                    }
                });
            }
            else alert("Comment not found");
        })

    });
});
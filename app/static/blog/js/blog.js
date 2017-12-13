$(document).ready(function() {
    blogServices.GetBlogs();
});

var blogServices = (function($) {
    var selected_blog_id = 0;

    function GetBlogs() {
        $.ajax({
            url: '/getBlog',
            type: 'GET',
            success: function(res) {
                setBlogHTML(res)
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    function setBlogHTML(res) {
        var blogObj = JSON.parse(res);
        var blogHtml = '';
        var length = 200;
        for (var i = 0; i < blogObj.length; i++) {
            var blog_description = blogObj[i].description.substring(0, length);

            blogHtml += '<div class="media-blog" id="id-list-' + blogObj[i].id + '"><div class="media" id="blog_' + blogObj[i].id + '"><div class="media-left media-top"><a href="#"><img class="media-object" src="static/blog/images/woods.jpeg" alt="..."></a></div><div class="media-body"><div class="media-left-text"><h4 class="media-heading" id="id-title-' + blogObj[i].id + '">' + blogObj[i].title + '</h4><p class="list-group-item-text" id="id-desc-' + blogObj[i].id + '">' + blog_description + '...<a href="/blog_track/' + blogObj[i].id + '">Read More</a></p></br><p class="list-group-item-date" id="id-createdon"><strong>Created on: </strong>' + blogObj[i].blog_created_on +'</p></div><div class="updateBtn"><a href="javascript:void(0)" data-id=' + blogObj[i].id + ' onclick="blogServices.editBlog(this)"><span class="glyphicon glyphicon-pencil"></span></a><a href="javascript:void(0)" data-id=' + blogObj[i].id + ' onclick="blogServices.confirmDelete(this)"><span class="glyphicon glyphicon-trash"></span></a></div></div></div></div>'
        }

        var mainDiv = '<div id="list-blog"></br>' + blogHtml + '</div>';
        $('.blogList').append(mainDiv);
    }
    
    function editBlog(elm) {
        selected_blog_id = $(elm).attr('data-id');
        $.ajax({
            url: '/getBlogById',
            data: {
                id: selected_blog_id
            },
            type: 'POST',
            success: function(res) {
                // Parse the received JSON string
                var data = JSON.parse(res);
                //Populate the Pop up
                $('#editTitle').val(data[0]['title']);
                $('#editDescription').val(data[0]['description']);
                // Trigger the Pop Up
                $('#editModal').modal('show');
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    function updateBlogdetails(blog_id) {
        var length = 300;
        $('#id-title-' + blog_id).html($('#editTitle').val());
        if ($('#id-desc-' + blog_id).html($('#editDescription').val().substring(0, length > 200))) {
            $('#id-desc-' + blog_id).html($('#editDescription').val().substring(0, length)).append('...<a href="/blog_track/' + blog_id + '">Read More</a>');
        }
        else {
           $('#id-desc-' + blog_id).html($('#editDescription').val().substring(0, length)).append('...<a href="/blog_track/' + blog_id + '">view Details</a>');
        }
        
    }

    $(function() {
        $('#btnUpdate').click(function() {
            // if(!$('#editTitle').val()){
            //     if(!$('#titleId').length){
            //         return $('#titleId').append('<span class="error">Please enter blog title.</span>');
            //     }
            // }
            // if (!$('#editDescription').val()) {
            //    if(!$('#descriptionId').length){
            //         return $('#descriptionId').append('<span class="error">Please enter blog description.</span>');
            //     }
            // }
            $.ajax({
                url: '/updateBlog',
                data: {
                    title: $('#editTitle').val(),
                    description: $('#editDescription').val(),
                    id: selected_blog_id
                },
                type: 'POST',
                success: function(res) {
                    updateBlogdetails(selected_blog_id);
                    selected_blog_id = 0;
                    $('#editModal').modal('hide');
                    // $('#modalError').remove();
                    // $('#modalDescError').remove();
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });
    });

    function confirmDelete(elm) {
        selected_blog_id = $(elm).attr('data-id');
        $('#deleteModal').modal();
    }

    function deleteBlogdetails(blog_id) {
        $('#id-list-' + blog_id).remove();
    }

    function deleteBlog() {
        $.ajax({
            url: '/deleteBlog',
            data: { id: selected_blog_id },
            type: 'POST',
            success: function(res) {
                var result = JSON.parse(res);
                if (result.status == 'OK') {
                    $('#deleteModal').modal('hide');
                    deleteBlogdetails(selected_blog_id);
                    selected_blog_id = 0;
                } else {
                    alert(result.status);
                }
            },
            error: function(error) {
                console.log(error);
            }
        });
    }

    var services = {};
    services.GetBlogs = GetBlogs;
    services.setBlogHTML = setBlogHTML;
    services.editBlog = editBlog;
    services.deleteBlog = deleteBlog;
    services.confirmDelete = confirmDelete;
    services.deleteBlog = deleteBlog;
    return services;

})(jQuery);
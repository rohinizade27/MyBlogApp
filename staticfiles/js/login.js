$(document).ready(function() {
    $('#blog_detail').hide();
    // Retrieve the list of blogs from the server
    var token = localStorage.getItem('accessToken'); // Retrieve the token from local storage
    var user_id = localStorage.getItem('user_id'); // Retrieve the user_id from local storage
    console.log('token-->',token)
    console.log('user_id-->',user_id)
        function isTokenValid(token) {
          if (token) {
            try {
              const decodedToken = JSON.parse(atob(token.split('.')[1]));
              const currentTime = Math.floor(Date.now() / 1000); // Get current time in seconds

              // Check if the token's expiration time is greater than the current time
              if (decodedToken.exp > currentTime) {
                console.log('home page...Token is valid...');
                $('#logout-button').show();
                $('#add-blog-button').on('click', function() {
                    console.log('redirect to add blog page....')
                    window.location.href = '/add_blog/';
                 });
                 $.ajax({
                          type: 'GET',
                          url: '/blogs/api/blog-list-by-use/' + user_id + '/',
                          beforeSend: function(xhr, settings) {
                          xhr.setRequestHeader('Authorization', 'Bearer ' + token);}, // Include the token in the request headers
                          success: function(response) {
                            console.log(response)
                            // Loop through the blogs and create Bootstrap cards
                            for (var i = 0; i < response.length; i++) {
                              var blog = response[i];
                              var blogCard = `
                                <div class="col-lg-4 col-sm-6 mb-4 hover-animate">
                                    <div class="card shadow border-0 h-100">
                                      <a href="">
                                        <img class="img-fluid card-img-top" src="${blog.image}" alt="..."/></a>
                                      <div class="card-body"><a class="text-uppercase text-muted text-sm letter-spacing-2" href="#">
                                        ${blog.user}</a>
                                        <h5 class="my-2"><a class="text-dark" href="/">
                                         ${blog.title}</a></h5>
                                        <p class="text-gray-500 text-sm my-3"><i class="far fa-clock mr-2"></i>
                                          ${blog.created_at}</p>
                                        <a class="btn btn-link pl-0 read-more" data-blog-id="${blog.id}">Read more<i class="fa fa-long-arrow-alt-right ml-2"></i></a>
                                      </div>
                                    </div>
                                  </div>
                              `;
                              $('#blogContainer').append(blogCard); // Append the card to the container
                              $('.read-more').on('click', function() {
                                var blogId = $(this).data('blog-id');
                                console.log("direct to detail blog view page...")

                                 $('#like-button').on('click',function() {
                                  console.log("clicked on like..")
                                  var element = $(this);

                                  // Make an AJAX request to like the post
                                  $.ajax({
                                    url: '/blogs/api/like-list-create/',
                                    type: 'POST',
                                    dataType: 'json',
                                    data: { "blog": blogId, "user": user_id},
                                    beforeSend: function(xhr, settings) {
                                    xhr.setRequestHeader('Authorization', 'Bearer ' + token);},
                                    success: function(response) {
                                      // Handle the success response
                                      console.log('blog liked successfully');
                                      console.log(response);
                                      $('#like-button').hide();
                                      $('#unlike-button').show();
                                      $('.like-count').find('.ml-1').text('( Total like count - ' + response.like_count + ')');
                                    },
                                    error: function(xhr, status, error) {
                                      // Handle the error response
                                      console.error('Error liking post:', error);
                                    }
                                  });
                                });

                                $('#unlike-button').on('click', function() {
                                console.log("clicked on unlike..")
                                  var element = $(this);

                                  // Make an AJAX request to unlike the post
                                  $.ajax({
                                    url: '/blogs/api/like-list-create/',
                                    type: 'PUT',
                                    data: { "blog": blogId, "user": user_id},
                                    beforeSend: function(xhr, settings) {
                                    xhr.setRequestHeader('Authorization', 'Bearer ' + token);},
                                    success: function(response) {
                                      // Handle the success response
                                      console.log('blog unliked successfully');
                                      $('#like-button').show();
                                      $('#unlike-button').hide();
                                      $('.like-count').find('.ml-1').text('( Total like count - ' + response.like_count + ')');
                                    },
                                    error: function(xhr, status, error) {
                                      // Handle the error response
                                      console.error('Error unliking post:', error);
                                    }
                                  });
                                });

                                 $.ajax({
                                    url: '/blogs/api/blog-retrieve-update-destroy/'+blogId+'/',
                                    type: 'GET',
                                    dataType: 'json',
                                    beforeSend: function(xhr, settings) {
                                    xhr.setRequestHeader('Authorization', 'Bearer ' + token);},
                                    success: function(responseData) {
                                       var blogDetails = responseData;
                                       console.log(blogDetails)

                                       // Update the image source
                                        $('#blog_detail img').attr('src', responseData.image);
                                        // Update the text content
                                        $('#blog_detail .text-content').html(`
                                          <h2>${blogDetails.title}</h2>
                                          <p>${blogDetails.content}</p>
                                          <p>Author: ${blogDetails.user}</p>
                                        `);
                                      if (blogDetails.user_has_liked) {
                                        console.log('this blog is already liked by logged in user..')
                                          var likeCount = blogDetails.like_count;
                                           $('#like-button').hide();
                                          $('#unlike-button').show();
                                          $('.like-count').find('.ml-1').text('( Total like count - ' + likeCount + ')');
                                       }
                                      else{
                                          console.log('this blog is not liked by logged in user..')
                                          var likeCount = blogDetails.like_count;
                                          $('#unlike-button').hide();
                                          $('#like-button').show();
                                          $('.like-count').find('.ml-1').text('( Total like count - ' + likeCount + ')');
                                       }
                                      $('#blog_list').hide();
                                      $('#blog_info').hide();
                                      $('#blog_detail').show();
                                    },
                                    error: function(xhr, status, error) {
                                      console.error('Request failed. Status:', status);
                                    }
                                  });

                              });
                            }
                          },
                          error: function(xhr, textStatus, error) {
                            console.log(error);
                          }
                        });
                      }
            } catch (error) {
              console.error('Error decoding JWT token:', error);
            }
          }
          else{
            // Redirect to the login page,Token is missing or expired
            console.log('Token is missing or expired...');
             $.ajax({
              type: 'GET',
              url: '/blogs/api/blog-list-create/',
              success: function(response) {
                // Loop through the blogs and create Bootstrap cards
                for (var i = 0; i < response.length; i++) {
                  var blog = response[i];
                  var blogCard = `
                    <div class="col-lg-4 col-sm-6 mb-4 hover-animate">
                        <div class="card shadow border-0 h-100">
                          <a href="">
                            <img class="img-fluid card-img-top" src="${blog.image}" alt="..."/></a>
                          <div class="card-body"><a class="text-uppercase text-muted text-sm letter-spacing-2" href="#">
                            ${blog.user}</a>
                            <h5 class="my-2"><a class="text-dark" href="/">
                             ${blog.title}</a></h5>
                            <p class="text-gray-500 text-sm my-3"><i class="far fa-clock mr-2"></i>
                              ${blog.created_at}</p>
                            <a class="btn btn-link pl-0 read-more" data-blog-id="${blog.id}">Read more<i class="fa fa-long-arrow-alt-right ml-2"></i></a>
                          </div>
                        </div>
                      </div>
                  `;
                  $('#blogContainer').append(blogCard); // Append the card to the container
                  $('.read-more').on('click', function() {
                                var blogId = $(this).data('blog-id');
                                console.log("direct to detail blog view page...1")
                                 $.ajax({
                                    url: '/blogs/api/blog-retrieve-update-destroy/'+blogId+'/',
                                    type: 'GET',
                                    dataType: 'json',
                                    success: function(responseData) {
                                       console.log(responseData)
                                       var blogDetails = responseData;
                                       // Update the image source
                                        $('#blog_detail img').attr('src', responseData.image);
                                        // Update the text content
                                        $('#blog_detail .text-content').html(`
                                          <h2>${blogDetails.title}</h2>
                                          <p>${blogDetails.content}</p>
                                          <p>Author: ${blogDetails.user}</p>
                                        `);
                                      $('#blog_list').hide();
                                      $('#blog_info').hide();
                                      $('#blog_detail').show();
                                    },
                                    error: function(xhr, status, error) {
                                      console.error('Request failed. Status:', status);
                                    }
                                  });

                              });

                }
              },
              error: function(xhr, textStatus, error) {
                console.log(error);
              }
            });

          }
        }
        const isLoggedIn = isTokenValid(token);

       });




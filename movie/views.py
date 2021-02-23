from django.shortcuts import render, redirect

# def movie(request):
#     return render(request, 'movie_page/movie_page.html')

def movie(request, movie_id):

    # *movie form movie table
    # *is_in_favorite boolean value
    # *is_in_watched boolean value
    # *review from the review table where user is who logged in
    # *lsit of user who are friend with the user, who logged in, and have this movie in favorite list

    context = {
        
    }
    return render(request, 'movie_page/movie_page.html', context)

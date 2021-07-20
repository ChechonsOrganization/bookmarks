(function(){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        document.body.appendChild(document.createElement('script')).src='https://testdjango.com:8000/static/js/bookmarklet.js?r='+Math.floor(Math.random()*99999999999999999999);
    }
})();

/*  The proceding script discovers whether the bookmarklet has
    already been loaded by checking whether the myBookmarklet variable
    is defined. By doing so, you avoid loading it again if the user clicks
    on the bookmarlet repeatedly. If myBookmarlet is not defined, you
    load another JS file by adding a <script> element to the document.
    The script tag loads the bookmarlet.js script using a randmon number
    as a parameter to prevent loading the file from the browser's cache.
    The actual bookmarklet code without requiringg your users to update
    the bookamrk they previously added to their browser 
*/
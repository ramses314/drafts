(function(){
    if (window.myBookmarklet !== undefined) {
        myBookmarklet();
    }
    else {
    documet.body.appendChild(
        documet.createElement('script')
    ).src='http://127.0.0.1:8000/static/jc/bookmarklet.js?r=' + Math.floor(Math.random()*999999999);
    }
})();
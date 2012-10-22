(function(){
	var iframe = document.createElement('iframe'),
		body = document.body,
		domain = 'http://oberlinreview.org/';

	body.appendChild(iframe);
	body.style.paddingTop = '55px';

	iframe.src = domain+'blogs/tumblr_embed';
	iframe.style.border = 0;
	iframe.style.position = 'absolute';
	iframe.style.top = 0;
	iframe.style.left = 0;
	iframe.style.right = 0;
	iframe.style.width = "100%";
	iframe.style.height = '60px';
	iframe.style.webkitBoxShadow = '0 0 8px rgba(0,0,0,.65)';
	iframe.style.MozBoxShadow = '0 0 8px rgba(0,0,0,.65)';
	iframe.style.boxShadow = '0 0 8px rgba(0,0,0,.65)';
	iframe.scrolling = 'no';
	iframe.style.zIndex = 1;
	iframe.style.backgroundColor = '#FFF';
}());

// Add this to your blog above </body>
// <script type="text/javascript" src="http://oberlinreview.org/static/behavior/tumbl.js"></script>
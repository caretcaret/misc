<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>$pagetitle$ - $wikititle$</title>
	$if(feed)$<link href="$base$/_feed/" type="application/atom+xml" rel="alternate" title="$wikititle$ Atom feed">
	<link href="$base$/_feed$pageUrl$" type="application/atom+xml" rel="alternate" title="$wikititle$: $pagetitle$ Atom feed">$endif$
	<link href="$base$/css/normalize.css" rel="stylesheet">
	$if(printable)$<link href="$base$/css/print.css" rel="stylesheet" media="all">
	$else$<link href="$base$/css/screen.css" rel="stylesheet" media="screen, projection">
	<link href="$base$/css/print.css" rel="stylesheet" media="print">$endif$
</head>
<body>
	<header>
		<nav id="site-nav">
			<ul>
				<li class="icon frontpage" title="Home"><a href="$base$/">Home</a></li>
				$if(sitenav)$
				<li class="icon allpages" title="All pages"><a href="$base$/_index">All pages</a></li>
				<li class="icon categories" title="Categories"><a href="$base$/_categories">Categories</a></li>
				<li class="icon randompage" title="Random page"><a href="$base$/_random">Random page</a></li>
				<li class="icon recentactivity" title="Recent activity"><a href="$base$/_activity">Recent activity</a></li>
				$if(wikiupload)$<li class="icon upload" title="Upload"><a href="$base$/_upload">Upload</a></li>$endif$
				<li class="icon help" title="Help"><a href="$base$/Help">Help</a></li>
				<li class="icon feed" title="Atom feed for this site"><a href="$base$/_feed" type="application/atom+xml" rel="alternate">Atom feed</a></li>
				$endif$
				<li class="icon loggedin" title="Logout"><a href="$base$/_logout">Logout</a></li>
				<li class="icon loggedout" title="Login"><a href="$base$/_login">Login</a></li>
			</ul>
			<form action="/_go" method="post" id="goform">
				<input type="text" name="gotopage" id="gotopage">
				<input type="button" name="go" id="go" value="Go">
				<input type="button" name="dupesearch" id="dupesearch" value="Search">
			</form>
			<form action="/_search" method="post" id="searchform">
				<input type="hidden" name="patterns" id="patterns">
				<input type="hidden" name="search" id="search" value="Search">
			</form>
		</nav>
		<nav id="article-nav">
			<h1><a href="$base$$pageUrl$">$pagetitle$</a></h1>
			$tabs$
			$if(pagetools)$
			<ul>
				<li class="icon pagesource" title="Page source"><a href="$base$/_showraw$pageUrl$$if(revision)$?revision=$revision$$endif$">Page source</a></li>
				<li class="icon print" title="Printable version"><a href="$base$$pageUrl$?printable$if(revision)$&amp;revision=$revision$$endif$">Printable version</a></li>
				<li class="icon delete" title="Delete this page"><a href="$base$/_delete$pageUrl$">Delete this page</a></li>
				<li class="icon feed" title="Atom feed for this page"><a href="$base$/_feed$pageUrl$" type="application/atom+xml" rel="alternate">Atom feed</a></li>
				<li>$exportbox$</li>
			</ul>
			$endif$
		</nav>
	</header>
	<article$if(ispage)$ class="ispage"$endif$>
		$if(markuphelp)$<div class="markupHelp"><div>Use pandoc flavored markdown syntax.</div></div>$endif$
		$if(revision)$<h2>Revision $revision$</h2>$endif$
		$if(messages)$<ul class="messages">$messages:listitem()$</ul>$endif$
		$content$
		$if(ispage)$
		<div id="disqus_thread"></div>
	    <script type="text/javascript">
	        var disqus_shortname = 'piesaresquares-wiki';
	        var disqus_developer = 1;
	        var disqus_identifier = '$pageUrl$';
	        var disqus_title = '$pagetitle$';
	        (function() {
	            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
	            dsq.src = 'http://' + disqus_shortname + '.disqus.com/embed.js';
	            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
	        })();
	    </script>
    	<noscript>Please enable JavaScript to view the <a href="http://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>    
		$endif$
	</article>
	<footer>powered by <a href="https://github.com/jgm/gitit/tree/master/">gitit</a> and <a href="http://disqus.com/">disqus</a></footer>
	<div>&nbsp;</div>
	$javascripts$
	<script>
		/* <![CDATA[ */
		  \$('#go').click(function() {
		    \$('#goform').submit();
		  });
		  \$('#dupesearch').click(function() {
		    \$('#patterns').attr('value', \$('#gotopage').attr('value'));
		    \$('#searchform').submit();
		  });
		  \$.get("$base$/_user", {}, function(username, status) {
		     \$(".loggedin").attr('title', 'Logged in as ' + username + ' (click to logout)');
		     \$("#username").text(username);
		     if (username == "") {  // nobody logged in
		        \$(".loggedin").hide();
		        \$(".loggedout").show();
		     } else {
		        \$(".loggedin").show();
		        \$(".loggedout").hide();
		     };
		   });
		/* ]]> */
	</script>
</body>
</html>

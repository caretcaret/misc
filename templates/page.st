<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>$pagetitle$ - $wikititle$</title>
	<link href="$base$/_feed/" type="application/atom+xml" rel="alternate" title="$wikititle$ Atom feed">
	<link href="$base$/_feed$pageUrl$" type="application/atom+xml" rel="alternate" title="$wikititle$: $pagetitle$ Atom feed">
	<link href="$base$/css/normalize.css" rel="stylesheet">
	<link href="$base$/css/screen.css" rel="stylesheet">
</head>
<body>
	<header>
		<nav id="site-nav">
			<ul>
				<li class="icon frontpage" title="Home"><a href="">Home</a></li>
				<li class="icon allpages" title="All pages"><a href="">All pages</a></li>
				<li class="icon categories" title="Categories"><a href="">Categories</a></li>
				<li class="icon randompage" title="Random page"><a href="">Random page</a></li>
				<li class="icon recentactivity" title="Recent activity"><a href="">Recent activity</a></li>
				<li class="icon upload" title="Upload"><a href="">Upload</a></li>
				<li class="icon help" title="Help"><a href="">Help</a></li>
				<li class="icon feed" title="Atom feed for this site"><a href="">Atom feed</a></li>
				<li class="icon loggedin" title="Logged in as _ (Logout)"><a href="">Logout</a></li>
				<li class="icon loggedout" title="Login"><a href="">Login</a></li>
				<li>
					<form action="/_go" method="post" id="goform">
						<input type="text" name="gotopage" id="gotopage">
						<input type="button" name="go" id="go" value="Go">
						<input type="button" name="dupesearch" id="dupesearch" value="Search">
					</form>
					<form action="/_search" method="post" id="searchform">
						<input type="hidden" name="patterns" id="patterns">
						<input type="hidden" name="search" id="search" value="Search">
					</form>
				</li>
			</ul>
		</nav>
		<nav id="article-nav">
			<h1><a href="$base$$pageUrl$">$pagetitle$</a></h1>
			<ul>
				<li class="icon pagesource" title="Page source"><a href="">Page source</a></li>
				<li class="icon print" title="Printable version"><a href="">Printable version</a></li>
				<li class="icon delete" title="Delete this page"><a href="">Delete this page</a></li>
				<li class="icon feed" title="Atom feed for this page"><a href="">Atom feed</a></li>
				<li>$exportbox$</li>
			</ul>	
			<ul class="tabs">
				<li>Tabs<li>
			</ul>
		</nav>
	</header>
	<article$if(ispage)$ class="ispage"$endif$>
		$content$
		<!-- if(ispage) put disqus here -->
	</article>
	<footer>powered by <a href="http://github.com/jgm/gitit/tree/master/">gitit</a></footer>
	<div>&nbsp;</div>
</body>
</html>
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
				<li>Login</li>
				<li>Logout</li>
				<li>Front page</li>
				<li>All pages</li>
				<li>Categories</li>
				<li>Random page</li>
				<li>Recent activity</li>
				<li>Upload a file</li>
				<li>Atom feed</li>
				<li>Help</li>
				<li>Search</li>
				<li>Goto</li>
			</ul>
		</nav>
		<nav id="article-nav">
			<h1><a href="$base$$pageUrl$">$pagetitle$</a></h1>
			<ul>
				<li>Tabs</li>
				<li>Page source</li>
				<li>Printable version</li>
				<li>Delete this page</li>
				<li>Atom feed</li>
				<li>Export</li>
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
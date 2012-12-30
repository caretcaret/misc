<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>$pagetitle$ - $wikititle$</title>
	<link href="$base$/_feed/" type="application/atom+xml" rel="alternate" title="$wikititle$ Atom feed">
	<link href="$base$/_feed$pageUrl$" type="application/atom+xml" rel="alternate" title="$wikititle$: $pagetitle$ Atom feed">
	<link href="$base$/css/normalize.css" rel="stylesheet">
	<link href="$base$/css/screen.css" rel="stylesheet" media="screen, projection">
	<link href="$base$/css/print.css" rel="stylesheet" media="print">
</head>
<body>
	<header>
		<nav id="site-nav">
			<ul>
				<li class="icon frontpage" title="Home"><a href="$base$">Home</a></li>
				<li class="icon allpages" title="All pages"><a href="$base$/_index">All pages</a></li>
				<li class="icon categories" title="Categories"><a href="$base$/_categories">Categories</a></li>
				<li class="icon randompage" title="Random page"><a href="$base$/_random">Random page</a></li>
				<li class="icon recentactivity" title="Recent activity"><a href="$base$/_activity">Recent activity</a></li>
				<li class="icon upload" title="Upload"><a href="$base$/_upload">Upload</a></li>
				<li class="icon help" title="Help"><a href="$base$/Help">Help</a></li>
				<li class="icon feed" title="Atom feed for this site"><a href="$base$/_feed" type="application/atom+xml" rel="alternate">Atom feed</a></li>
				<li class="icon loggedin" title="Logged in as _ (Logout)"><a id="logoutlink" href="$base$/_logout">Logout</a></li>
				<li class="icon loggedout" title="Login"><a id="loginlink" href="$base$/_login">Login</a></li>
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
				<li class="icon pagesource" title="Page source"><a href="$base$/_showraw$pageUrl$$if(revision)$?revision=$revision$$endif$">Page source</a></li>
				<li class="icon print" title="Printable version"><a href="$base$$pageUrl$?printable$if(revision)$&amp;revision=$revision$$endif$">Printable version</a></li>
				<li class="icon delete" title="Delete this page"><a href="$base$/_delete$pageUrl$">Delete this page</a></li>
				<li class="icon feed" title="Atom feed for this page"><a href="$base$/_feed$pageUrl$" type="application/atom+xml" rel="alternate">Atom feed</a></li>
				<li>$exportbox$</li>
			</ul>
			$tabs$
		</nav>
	</header>
	<article$if(ispage)$ class="ispage"$endif$>
		$if(markuphelp)$<div class="markupHelp"><div>Use pandoc flavored markdown syntax.</div></div>$endif$
		$if(revision)$<h2>Revision $revision$</h2>$endif$
		$if(messages)$<ul class="messages">$messages:listitem()$</ul>$endif$
		$content$
		<!-- if(ispage) put disqus here -->
	</article>
	<footer>powered by <a href="http://github.com/jgm/gitit/tree/master/">gitit</a></footer>
	<div>&nbsp;</div>
</body>
</html>

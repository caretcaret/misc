<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>$pagetitle$ - $wikititle$</title>
	<link href="$base$/_feed/" type="application/atom+xml" rel="alternate" title="$wikititle$ Atom feed">
	<link href="$base$/_feed$pageUrl$" type="application/atom+xml" rel="alternate" title="$wikititle$: $pagetitle$ Atom feed">
	<link href="$base$/css/normalize.css" rel="stylesheet">
	<style>
	/* screen.css */
	body { background-color: #077; margin: 0; }
	#site-nav, #article-nav h1, #article-nav ul { border: 1px solid #000; }
	header { background-color: #33f; }
	#site-nav { text-align: center; margin: auto; background-color: #44f; float: right; }
	#article-nav { margin: auto; background-color: #0a0; }
	#article-nav h1 { display: inline; }
	#article-nav ul { float: right; }
	#TOC { position: absolute; height: 100%; background-color: #ffd; right: 0; }
	#TOC ul { margin-top: 15px; }
	article { position: relative; margin: auto; background-color: #fff; }
	article * { margin-top: 0; }
	article:before, article:after { content: " "; display: table; }
	article:after { clear: both; } /* clearfix */
	footer { text-align: center; margin: auto; background-color: #00d; }
	@media only screen and (min-width: 768px) {

	}

	@media only screen and (min-width: 992px) {
		#article-nav { max-width: 992px; padding-left: 55px; padding-right: 55px; height: 55px; border-radius: 50%; border-bottom: 2px solid #aaf; }
		#TOC { width: 270px; padding: 0 15px; top: 0; }
		article { max-width: 692px; padding-left: 55px; padding-right: 355px; padding-top: 15px; }
		footer { max-width: 992px; padding-left: 55px; padding-right: 55px; height: 55px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; margin-bottom: 55px; }
		/* make font size smaller */
	}
	</style>
</head>
<body>
	<header>
		<a href="$base$"><img src="$base$/img/logo.png" alt="lilypad" height="100" width="100"></a>
		<nav id="site-nav">stuff</nav>
		<nav id="article-nav">
			<a href="$base$$pageUrl$"><h1>$pagetitle$</h1></a>
			<ul><!-- icons here --></ul>
		</nav>
	</header>
	<article>
		$content$
		<!-- if(ispage) put disqus here -->
	</article>
	<footer>powered by <a href="http://github.com/jgm/gitit/tree/master/">gitit</a></footer>
</body>
</html>
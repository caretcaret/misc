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
	html, body { height: 100%; padding: 0; margin: 0; background-image: url("img/white_wave.png"), -webkit-linear-gradient(top, #27a2e6, #0e5278); background-image: url("img/white_wave.png"), linear-gradient(top, #27a2e6, #0e5278); background-attachment: fixed, fixed; }
	header { background: #116796 url("img/white_wave.png"); }
	#site-nav { text-align: center; margin: auto; }
	#article-nav { margin: auto; background: #82ca67 url("img/white_wave.png"); }
	#article-nav h1 { display: inline; }
	#article-nav ul { float: right; }
	#TOC { background-color: #e1f3cc; background-image: url("img/bgnoise.png"); }
	article { position: relative; margin: auto; background: #e9f6da url("img/bgnoise.png"); }
	article:before, article:after { content: " "; display: table; }
	article:after { clear: both; } /* clearfix */
	footer { text-align: center; margin: auto; background: #dde2e8 url("img/bgnoise.png"); }
	@media only screen and (min-width: 768px) {

	}

	@media only screen and (min-width: 992px) {
		#site-nav { height: 55px; }
		#article-nav { max-width: 882px; padding: 0 55px; height: 55px; border-radius: 10px 10px 0 0; }
		#TOC { position: absolute; height: 100%; top: 0; right: 0; width: 220px; padding: 0 15px; border-left: 1px solid #d1edb0; }
		#TOC ul { margin-top: 40px; }
		article { max-width: 882px; padding: 40px 55px 0; border-bottom: 1px solid #b4bfcd; }
		article.ispage { max-width: 632px; padding-right: 305px; }
		article * { margin-top: 0; }
		footer { max-width: 992px; height: 55px; border-radius: 0 0 10px 10px; border-top: 1px solid #ffffff; background-image: -webkit-linear-gradient(top, #f1f3f6, #d3dae1); background-image: linear-gradient(top, #f1f3f6, #d3dae1); margin-bottom: 55px; }
		/* make font size smaller */
	}
	</style>
</head>
<body>
	<header>
		<nav id="site-nav">icons here</nav>
		<nav id="article-nav">
			<a href="$base$$pageUrl$"><h1>$pagetitle$</h1></a>
			<ul>icons here</ul>
		</nav>
	</header>
	<article class="$if(ispage)$ispage$endif$">
		$content$
		<!-- if(ispage) put disqus here -->
	</article>
	<footer>powered by <a href="http://github.com/jgm/gitit/tree/master/">gitit</a></footer>
	<div>&nbsp;</div>
</body>
</html>
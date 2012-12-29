<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>$pagetitle$ - $wikititle$</title>
	<link href="$base$/_feed/" type="application/atom+xml" rel="alternate" title="$wikititle$ Atom feed">
	<link href="$base$/_feed$pageUrl$" type="application/atom+xml" rel="alternate" title="$wikititle$: $pagetitle$ Atom feed">
	<link href="$base$/css/normalize.css" rel="stylesheet">
	<style>
	#site-nav, #article-nav h1, #article-nav ul { border: 1px solid #000; }
	/* screen.css */
	html, body { height: 100%; padding: 0; margin: 0; background-image: url("img/white_wave.png"), -webkit-linear-gradient(top, #27a2e6, #0e5278); background-image: url("img/white_wave.png"), linear-gradient(top, #27a2e6, #0e5278); background-attachment: fixed, fixed; }
	header { background-color: #116796; background-image: url("img/white_wave.png"); }
	#site-nav { text-align: center; margin: auto; float: right; }
	#article-nav { margin: auto; background: #82ca67 url("img/white_wave.png"); }
	#article-nav h1 { display: inline; }
	#article-nav ul { float: right; }
	#TOC { background-color: #e1f3cc; background-image: url("img/bgnoise.png"); }
	#container { margin: auto; }
	article { position: relative; background-color: #e9f6da; background-image: url("img/bgnoise.png"); }
	article:before, article:after { content: " "; display: table; }
	article:after { clear: both; } /* clearfix */
	footer { text-align: center; margin: auto; background-color: #dde2e8; background-image: url("img/bgnoise.png"); }
	@media only screen and (min-width: 768px) {

	}

	@media only screen and (min-width: 992px) {
		#article-nav { max-width: 882px; padding-left: 55px; padding-right: 55px; height: 55px; border-top-left-radius: 10px; border-top-right-radius: 10px; }
		#TOC { position: absolute; height: 100%; right: 0; width: 220px; padding: 0 15px; top: 0; border-left: 1px solid #d1edb0; }
		#TOC ul { margin-top: 40px; }
		#container { width: 992px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; }
		article { max-width: 692px; padding-left: 55px; padding-right: 355px; padding-top: 40px; border-bottom: 1px solid #b4bfcd; }
		article * { margin-top: 0; }
		footer { max-width: 992px; height: 55px; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; border-top: 1px solid #ffffff; background-image: -webkit-linear-gradient(top, #f1f3f6, #d3dae1); background-image: linear-gradient(top, #f1f3f6, #d3dae1); }
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
	<div id="container">
		<article>
			$content$
			<!-- if(ispage) put disqus here -->
		</article>
		<footer>powered by <a href="http://github.com/jgm/gitit/tree/master/">gitit</a></footer>
	</div>
</body>
</html>
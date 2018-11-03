



<!DOCTYPE html>
<html lang="en" class="">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>

    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/frameworks-ce3c74f5c71958d8d02d5f36275809f5f6e20e5244cb38e36fd299a3cb49716a.css" media="all" rel="stylesheet" />
    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github-4d8d7740603718bde2c83ff766bf53c39972f4f6f5509c013a08497a75799732.css" media="all" rel="stylesheet" />
    
    
    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/site-c4b4365da282e51c06e107368db8502a2ecf82e64094d29d791b797372212de2.css" media="all" rel="stylesheet" />
    

    <link as="script" href="https://assets-cdn.github.com/assets/frameworks-e76ce42ce77c934586f7cacbe24d556dbe6fefdbe8b53a393644b18199f7c291.js" rel="preload" />
    
    <link as="script" href="https://assets-cdn.github.com/assets/github-3403611476aba5449f7af712dbf7b488bbb552e0a3e93c55d36c058fe7968b46.js" rel="preload" />

    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    <meta name="viewport" content="width=device-width">
    
    
    <title>GitHub - eligrey/FileSaver.js: An HTML5 saveAs() FileSaver implementation</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" href="/apple-touch-icon.png">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="/apple-touch-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="/apple-touch-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="/apple-touch-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="/apple-touch-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon-180x180.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="https://avatars3.githubusercontent.com/u/46995?v=3&amp;s=400" name="twitter:image:src" /><meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="eligrey/FileSaver.js" name="twitter:title" /><meta content="FileSaver.js - An HTML5 saveAs() FileSaver implementation" name="twitter:description" />
      <meta content="https://avatars3.githubusercontent.com/u/46995?v=3&amp;s=400" property="og:image" /><meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="eligrey/FileSaver.js" property="og:title" /><meta content="https://github.com/eligrey/FileSaver.js" property="og:url" /><meta content="FileSaver.js - An HTML5 saveAs() FileSaver implementation" property="og:description" />
      <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">
    <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">
    <link rel="assets" href="https://assets-cdn.github.com/">
    
    <meta name="pjax-timeout" content="1000">
    

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>

    <meta name="google-site-verification" content="KT5gs8h0wvaagLKAVWq8bbeNwnZZK1r1XQysX3xurLU">
<meta name="google-site-verification" content="ZzhVyEFwb7w3e0-uOTltm8Jsck2F5StVihD0exw2fsA">
    <meta name="google-analytics" content="UA-3769691-2">

<meta content="collector.githubapp.com" name="octolytics-host" /><meta content="github" name="octolytics-app-id" /><meta content="4E1578B2:8523:1ED6CD5A:5746C8F8" name="octolytics-dimension-request_id" />
<meta content="/&lt;user-name&gt;/&lt;repo-name&gt;" data-pjax-transient="true" name="analytics-location" />



  <meta class="js-ga-set" name="dimension1" content="Logged Out">



        <meta name="hostname" content="github.com">
    <meta name="user-login" content="">

        <meta name="expected-hostname" content="github.com">
      <meta name="js-proxy-site-detection-payload" content="ZTFjYzM3NTdmMjJmYzM5MDFjMzI0YmFkNjljYjc5NTBhMGI2NjE0NzY0MDM1Mjk3MDE2MTcxMTRlZjRhY2MzNHx7InJlbW90ZV9hZGRyZXNzIjoiNzguMjEuMTIwLjE3OCIsInJlcXVlc3RfaWQiOiI0RTE1NzhCMjo4NTIzOjFFRDZDRDVBOjU3NDZDOEY4IiwidGltZXN0YW1wIjoxNDY0MjU2NzYwfQ==">


      <link rel="mask-icon" href="https://assets-cdn.github.com/pinned-octocat.svg" color="#4078c0">
      <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">

    <meta name="html-safe-nonce" content="b3184383b34671cb61723bcb401c316151b49eb9">
    <meta content="9f111d64e28d2e53430d47f25015bae55cd27c97" name="form-nonce" />

    <meta http-equiv="x-pjax-version" content="28e6c1aea7b458688812e600c223f2e1">
    

      
  <meta name="description" content="FileSaver.js - An HTML5 saveAs() FileSaver implementation">
  <meta name="go-import" content="github.com/eligrey/FileSaver.js git https://github.com/eligrey/FileSaver.js.git">

  <meta content="46995" name="octolytics-dimension-user_id" /><meta content="eligrey" name="octolytics-dimension-user_login" /><meta content="2051226" name="octolytics-dimension-repository_id" /><meta content="eligrey/FileSaver.js" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="2051226" name="octolytics-dimension-repository_network_root_id" /><meta content="eligrey/FileSaver.js" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/eligrey/FileSaver.js/commits/master.atom" rel="alternate" title="Recent Commits to FileSaver.js:master" type="application/atom+xml">


      <link rel="canonical" href="https://github.com/eligrey/FileSaver.js" data-pjax-transient>
  </head>


  <body class="logged-out   env-production  vis-public">
    <div id="js-pjax-loader-bar" class="pjax-loader-bar"></div>
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>

    
    
    



          <header class="site-header js-details-container" role="banner">
  <div class="container-responsive">
    <a class="header-logo-invertocat" href="https://github.com/" aria-label="Homepage" data-ga-click="(Logged out) Header, go to homepage, icon:logo-wordmark">
      <svg aria-hidden="true" class="octicon octicon-mark-github" height="32" version="1.1" viewBox="0 0 16 16" width="32"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59 0.4 0.07 0.55-0.17 0.55-0.38 0-0.19-0.01-0.82-0.01-1.49-2.01 0.37-2.53-0.49-2.69-0.94-0.09-0.23-0.48-0.94-0.82-1.13-0.28-0.15-0.68-0.52-0.01-0.53 0.63-0.01 1.08 0.58 1.23 0.82 0.72 1.21 1.87 0.87 2.33 0.66 0.07-0.52 0.28-0.87 0.51-1.07-1.78-0.2-3.64-0.89-3.64-3.95 0-0.87 0.31-1.59 0.82-2.15-0.08-0.2-0.36-1.02 0.08-2.12 0 0 0.67-0.21 2.2 0.82 0.64-0.18 1.32-0.27 2-0.27 0.68 0 1.36 0.09 2 0.27 1.53-1.04 2.2-0.82 2.2-0.82 0.44 1.1 0.16 1.92 0.08 2.12 0.51 0.56 0.82 1.27 0.82 2.15 0 3.07-1.87 3.75-3.65 3.95 0.29 0.25 0.54 0.73 0.54 1.48 0 1.07-0.01 1.93-0.01 2.2 0 0.21 0.15 0.46 0.55 0.38C13.71 14.53 16 11.53 16 8 16 3.58 12.42 0 8 0z"></path></svg>
    </a>

    <button class="btn-link right site-header-toggle js-details-target" type="button" aria-label="Toggle navigation">
      <svg aria-hidden="true" class="octicon octicon-three-bars" height="24" version="1.1" viewBox="0 0 12 16" width="18"><path d="M11.41 9H0.59c-0.59 0-0.59-0.41-0.59-1s0-1 0.59-1h10.81c0.59 0 0.59 0.41 0.59 1s0 1-0.59 1z m0-4H0.59c-0.59 0-0.59-0.41-0.59-1s0-1 0.59-1h10.81c0.59 0 0.59 0.41 0.59 1s0 1-0.59 1zM0.59 11h10.81c0.59 0 0.59 0.41 0.59 1s0 1-0.59 1H0.59c-0.59 0-0.59-0.41-0.59-1s0-1 0.59-1z"></path></svg>
    </button>

    <div class="site-header-menu">
      <nav class="site-header-nav site-header-nav-main">
        <a href="/personal" class="js-selected-navigation-item nav-item nav-item-personal" data-ga-click="Header, click, Nav menu - item:personal" data-selected-links="/personal /personal">
          Personal
</a>        <a href="/open-source" class="js-selected-navigation-item nav-item nav-item-opensource" data-ga-click="Header, click, Nav menu - item:opensource" data-selected-links="/open-source /open-source">
          Open source
</a>        <a href="/business" class="js-selected-navigation-item nav-item nav-item-business" data-ga-click="Header, click, Nav menu - item:business" data-selected-links="/business /business/features /business/customers /business">
          Business
</a>        <a href="/explore" class="js-selected-navigation-item nav-item nav-item-explore" data-ga-click="Header, click, Nav menu - item:explore" data-selected-links="/explore /trending /trending/developers /integrations /integrations/feature/code /integrations/feature/collaborate /integrations/feature/ship /explore">
          Explore
</a>      </nav>

      <div class="site-header-actions">
            <a class="btn btn-primary site-header-actions-btn" href="/join?source=header-repo" data-ga-click="(Logged out) Header, clicked Sign up, text:sign-up">Sign up</a>
          <a class="btn site-header-actions-btn mr-2" href="/login?return_to=%2Feligrey%2FFileSaver.js" data-ga-click="(Logged out) Header, clicked Sign in, text:sign-in">Sign in</a>
      </div>

        <nav class="site-header-nav site-header-nav-secondary">
          <a class="nav-item" href="/pricing">Pricing</a>
          <a class="nav-item" href="/blog">Blog</a>
          <a class="nav-item" href="https://help.github.com">Support</a>
          <a class="nav-item header-search-link" href="https://github.com/search">Search GitHub</a>
              <div class="header-search scoped-search site-scoped-search js-site-search" role="search">
  <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/eligrey/FileSaver.js/search" class="js-site-search-form" data-scoped-search-url="/eligrey/FileSaver.js/search" data-unscoped-search-url="/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <label class="form-control header-search-wrapper js-chromeless-input-container">
      <div class="header-search-scope">This repository</div>
      <input type="text"
        class="form-control header-search-input js-site-search-focus js-site-search-field is-clearable"
        data-hotkey="s"
        name="q"
        placeholder="Search"
        aria-label="Search this repository"
        data-unscoped-placeholder="Search GitHub"
        data-scoped-placeholder="Search"
        tabindex="1"
        autocapitalize="off">
    </label>
</form></div>

        </nav>
    </div>
  </div>
</header>



    <div id="start-of-content" class="accessibility-aid"></div>

      <div id="js-flash-container">
</div>


    <div role="main" class="main-content">
        <div itemscope itemtype="http://schema.org/SoftwareSourceCode">
    <div id="js-repo-pjax-container" data-pjax-container>
      
<div class="pagehead repohead instapaper_ignore readability-menu experiment-repo-nav">
  <div class="container repohead-details-container">

    

<ul class="pagehead-actions">

  <li>
      <a href="/login?return_to=%2Feligrey%2FFileSaver.js"
    class="btn btn-sm btn-with-count tooltipped tooltipped-n"
    aria-label="You must be signed in to watch a repository" rel="nofollow">
    <svg aria-hidden="true" class="octicon octicon-eye" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M8.06 2C3 2 0 8 0 8s3 6 8.06 6c4.94 0 7.94-6 7.94-6S13 2 8.06 2z m-0.06 10c-2.2 0-4-1.78-4-4 0-2.2 1.8-4 4-4 2.22 0 4 1.8 4 4 0 2.22-1.78 4-4 4z m2-4c0 1.11-0.89 2-2 2s-2-0.89-2-2 0.89-2 2-2 2 0.89 2 2z"></path></svg>
    Watch
  </a>
  <a class="social-count" href="/eligrey/FileSaver.js/watchers">
    182
  </a>

  </li>

  <li>
      <a href="/login?return_to=%2Feligrey%2FFileSaver.js"
    class="btn btn-sm btn-with-count tooltipped tooltipped-n"
    aria-label="You must be signed in to star a repository" rel="nofollow">
    <svg aria-hidden="true" class="octicon octicon-star" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M14 6l-4.9-0.64L7 1 4.9 5.36 0 6l3.6 3.26L2.67 14l4.33-2.33 4.33 2.33L10.4 9.26 14 6z"></path></svg>
    Star
  </a>

    <a class="social-count js-social-count" href="/eligrey/FileSaver.js/stargazers">
      3,813
    </a>

  </li>

  <li>
      <a href="/login?return_to=%2Feligrey%2FFileSaver.js"
        class="btn btn-sm btn-with-count tooltipped tooltipped-n"
        aria-label="You must be signed in to fork a repository" rel="nofollow">
        <svg aria-hidden="true" class="octicon octicon-repo-forked" height="16" version="1.1" viewBox="0 0 10 16" width="10"><path d="M8 1c-1.11 0-2 0.89-2 2 0 0.73 0.41 1.38 1 1.72v1.28L5 8 3 6v-1.28c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2S0 1.89 0 3c0 0.73 0.41 1.38 1 1.72v1.78l3 3v1.78c-0.59 0.34-1 0.98-1 1.72 0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.73-0.41-1.38-1-1.72V9.5l3-3V4.72c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2zM2 4.2c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m3 10c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m3-10c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z"></path></svg>
        Fork
      </a>

    <a href="/eligrey/FileSaver.js/network" class="social-count">
      870
    </a>
  </li>
</ul>

    <h1 class="entry-title public ">
  <svg aria-hidden="true" class="octicon octicon-repo" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M4 9h-1v-1h1v1z m0-3h-1v1h1v-1z m0-2h-1v1h1v-1z m0-2h-1v1h1v-1z m8-1v12c0 0.55-0.45 1-1 1H6v2l-1.5-1.5-1.5 1.5V14H1c-0.55 0-1-0.45-1-1V1C0 0.45 0.45 0 1 0h10c0.55 0 1 0.45 1 1z m-1 10H1v2h2v-1h3v1h5V11z m0-10H2v9h9V1z"></path></svg>
  <span class="author" itemprop="author"><a href="/eligrey" class="url fn" rel="author">eligrey</a></span><!--
--><span class="path-divider">/</span><!--
--><strong itemprop="name"><a href="/eligrey/FileSaver.js" data-pjax="#js-repo-pjax-container">FileSaver.js</a></strong>

</h1>

  </div>
  <div class="container">
    
<nav class="reponav js-repo-nav js-sidenav-container-pjax"
     itemscope
     itemtype="http://schema.org/BreadcrumbList"
     role="navigation"
     data-pjax="#js-repo-pjax-container">

  <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
    <a href="/eligrey/FileSaver.js" aria-selected="true" class="js-selected-navigation-item selected reponav-item" data-hotkey="g c" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /eligrey/FileSaver.js" itemprop="url">
      <svg aria-hidden="true" class="octicon octicon-code" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M9.5 3l-1.5 1.5 3.5 3.5L8 11.5l1.5 1.5 4.5-5L9.5 3zM4.5 3L0 8l4.5 5 1.5-1.5L2.5 8l3.5-3.5L4.5 3z"></path></svg>
      <span itemprop="name">Code</span>
      <meta itemprop="position" content="1">
</a>  </span>

    <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
      <a href="/eligrey/FileSaver.js/issues" class="js-selected-navigation-item reponav-item" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /eligrey/FileSaver.js/issues" itemprop="url">
        <svg aria-hidden="true" class="octicon octicon-issue-opened" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M7 2.3c3.14 0 5.7 2.56 5.7 5.7S10.14 13.7 7 13.7 1.3 11.14 1.3 8s2.56-5.7 5.7-5.7m0-1.3C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7S10.86 1 7 1z m1 3H6v5h2V4z m0 6H6v2h2V10z"></path></svg>
        <span itemprop="name">Issues</span>
        <span class="counter">24</span>
        <meta itemprop="position" content="2">
</a>    </span>

  <span itemscope itemtype="http://schema.org/ListItem" itemprop="itemListElement">
    <a href="/eligrey/FileSaver.js/pulls" class="js-selected-navigation-item reponav-item" data-hotkey="g p" data-selected-links="repo_pulls /eligrey/FileSaver.js/pulls" itemprop="url">
      <svg aria-hidden="true" class="octicon octicon-git-pull-request" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M11 11.28c0-1.73 0-6.28 0-6.28-0.03-0.78-0.34-1.47-0.94-2.06s-1.28-0.91-2.06-0.94c0 0-1.02 0-1 0V0L4 3l3 3V4h1c0.27 0.02 0.48 0.11 0.69 0.31s0.3 0.42 0.31 0.69v6.28c-0.59 0.34-1 0.98-1 1.72 0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.73-0.41-1.38-1-1.72z m-1 2.92c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2zM4 3c0-1.11-0.89-2-2-2S0 1.89 0 3c0 0.73 0.41 1.38 1 1.72 0 1.55 0 5.56 0 6.56-0.59 0.34-1 0.98-1 1.72 0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.73-0.41-1.38-1-1.72V4.72c0.59-0.34 1-0.98 1-1.72z m-0.8 10c0 0.66-0.55 1.2-1.2 1.2s-1.2-0.55-1.2-1.2 0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2z m-1.2-8.8c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z"></path></svg>
      <span itemprop="name">Pull requests</span>
      <span class="counter">4</span>
      <meta itemprop="position" content="3">
</a>  </span>

    <a href="/eligrey/FileSaver.js/wiki" class="js-selected-navigation-item reponav-item" data-hotkey="g w" data-selected-links="repo_wiki /eligrey/FileSaver.js/wiki">
      <svg aria-hidden="true" class="octicon octicon-book" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M2 5h4v1H2v-1z m0 3h4v-1H2v1z m0 2h4v-1H2v1z m11-5H9v1h4v-1z m0 2H9v1h4v-1z m0 2H9v1h4v-1z m2-6v9c0 0.55-0.45 1-1 1H8.5l-1 1-1-1H1c-0.55 0-1-0.45-1-1V3c0-0.55 0.45-1 1-1h5.5l1 1 1-1h5.5c0.55 0 1 0.45 1 1z m-8 0.5l-0.5-0.5H1v9h6V3.5z m7-0.5H8.5l-0.5 0.5v8.5h6V3z"></path></svg>
      Wiki
</a>

  <a href="/eligrey/FileSaver.js/pulse" class="js-selected-navigation-item reponav-item" data-selected-links="pulse /eligrey/FileSaver.js/pulse">
    <svg aria-hidden="true" class="octicon octicon-pulse" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M11.5 8L8.8 5.4 6.6 8.5 5.5 1.6 2.38 8H0V10h3.6L4.5 8.2l0.9 5.4L9 8.5l1.6 1.5H14V8H11.5z"></path></svg>
    Pulse
</a>
  <a href="/eligrey/FileSaver.js/graphs" class="js-selected-navigation-item reponav-item" data-selected-links="repo_graphs repo_contributors /eligrey/FileSaver.js/graphs">
    <svg aria-hidden="true" class="octicon octicon-graph" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M16 14v1H0V0h1v14h15z m-11-1H3V8h2v5z m4 0H7V3h2v10z m4 0H11V6h2v7z"></path></svg>
    Graphs
</a>

</nav>

  </div>
</div>

<div class="container new-discussion-timeline experiment-repo-nav">
  <div class="repository-content">

    
<div class="repository-meta js-details-container">
  <span class="repository-meta-content">
        <span itemprop="about"> An HTML5 saveAs() FileSaver implementation</span>
        <span itemprop="url"><a href="http://eligrey.com/blog/post/saving-generated-files-on-the-client-side" rel="nofollow">http://eligrey.com/blog/post/saving-generated-files-on-the-client-side</a></span>
  </span>

</div>


<div class="overall-summary overall-summary-bottomless">
  <div class="stats-switcher-viewport js-stats-switcher-viewport">
    <div class="stats-switcher-wrapper">
    <ul class="numbers-summary">
      <li class="commits">
        <a data-pjax href="/eligrey/FileSaver.js/commits/master">
            <svg aria-hidden="true" class="octicon octicon-history" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M8 13H6V6h5v2H8v5zM7 1c-2.19 0-4.13 1.02-5.41 2.59L0 2v4h4l-1.5-1.5c1.05-1.33 2.67-2.2 4.5-2.2 3.14 0 5.7 2.56 5.7 5.7S10.14 13.7 7 13.7 1.3 11.14 1.3 8c0-0.34 0.03-0.67 0.09-1H0.08c-0.05 0.33-0.08 0.66-0.08 1 0 3.86 3.14 7 7 7s7-3.14 7-7S10.86 1 7 1z"></path></svg>
            <span class="num text-emphasized">
              199
            </span>
            commits
        </a>
      </li>
      <li>
        <a data-pjax href="/eligrey/FileSaver.js/branches">
          <svg aria-hidden="true" class="octicon octicon-git-branch" height="16" version="1.1" viewBox="0 0 10 16" width="10"><path d="M10 5c0-1.11-0.89-2-2-2s-2 0.89-2 2c0 0.73 0.41 1.38 1 1.72v0.3c-0.02 0.52-0.23 0.98-0.63 1.38s-0.86 0.61-1.38 0.63c-0.83 0.02-1.48 0.16-2 0.45V4.72c0.59-0.34 1-0.98 1-1.72 0-1.11-0.89-2-2-2S0 1.89 0 3c0 0.73 0.41 1.38 1 1.72v6.56C0.41 11.63 0 12.27 0 13c0 1.11 0.89 2 2 2s2-0.89 2-2c0-0.53-0.2-1-0.53-1.36 0.09-0.06 0.48-0.41 0.59-0.47 0.25-0.11 0.56-0.17 0.94-0.17 1.05-0.05 1.95-0.45 2.75-1.25s1.2-1.98 1.25-3.02h-0.02c0.61-0.36 1.02-1 1.02-1.73zM2 1.8c0.66 0 1.2 0.55 1.2 1.2s-0.55 1.2-1.2 1.2-1.2-0.55-1.2-1.2 0.55-1.2 1.2-1.2z m0 12.41c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z m6-8c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2 1.2 0.55 1.2 1.2-0.55 1.2-1.2 1.2z"></path></svg>
          <span class="num text-emphasized">
            1
          </span>
          branch
        </a>
      </li>

      <li>
        <a data-pjax href="/eligrey/FileSaver.js/releases">
          <svg aria-hidden="true" class="octicon octicon-tag" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M6.73 2.73c-0.47-0.47-1.11-0.73-1.77-0.73H2.5C1.13 2 0 3.13 0 4.5v2.47c0 0.66 0.27 1.3 0.73 1.77l6.06 6.06c0.39 0.39 1.02 0.39 1.41 0l4.59-4.59c0.39-0.39 0.39-1.02 0-1.41L6.73 2.73zM1.38 8.09c-0.31-0.3-0.47-0.7-0.47-1.13V4.5c0-0.88 0.72-1.59 1.59-1.59h2.47c0.42 0 0.83 0.16 1.13 0.47l6.14 6.13-4.73 4.73L1.38 8.09z m0.63-4.09h2v2H2V4z"></path></svg>
          <span class="num text-emphasized">
            1
          </span>
          release
        </a>
      </li>

      <li>
          <a href="/eligrey/FileSaver.js/graphs/contributors">
  <svg aria-hidden="true" class="octicon octicon-organization" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M4.75 4.95c0.55 0.64 1.34 1.05 2.25 1.05s1.7-0.41 2.25-1.05c0.34 0.63 1 1.05 1.75 1.05 1.11 0 2-0.89 2-2s-0.89-2-2-2c-0.41 0-0.77 0.13-1.08 0.33C9.61 1 8.42 0 7 0S4.39 1 4.08 2.33c-0.31-0.2-0.67-0.33-1.08-0.33-1.11 0-2 0.89-2 2s0.89 2 2 2c0.75 0 1.41-0.42 1.75-1.05z m5.2-1.52c0.2-0.38 0.59-0.64 1.05-0.64 0.66 0 1.2 0.55 1.2 1.2s-0.55 1.2-1.2 1.2-1.17-0.53-1.19-1.17c0.06-0.19 0.11-0.39 0.14-0.59zM7 0.98c1.11 0 2.02 0.91 2.02 2.02s-0.91 2.02-2.02 2.02-2.02-0.91-2.02-2.02S5.89 0.98 7 0.98zM3 5.2c-0.66 0-1.2-0.55-1.2-1.2s0.55-1.2 1.2-1.2c0.45 0 0.84 0.27 1.05 0.64 0.03 0.2 0.08 0.41 0.14 0.59-0.02 0.64-0.53 1.17-1.19 1.17z m10 0.8H1c-0.55 0-1 0.45-1 1v3c0 0.55 0.45 1 1 1v2c0 0.55 0.45 1 1 1h1c0.55 0 1-0.45 1-1v-1h1v3c0 0.55 0.45 1 1 1h2c0.55 0 1-0.45 1-1V12h1v1c0 0.55 0.45 1 1 1h1c0.55 0 1-0.45 1-1V11c0.55 0 1-0.45 1-1V7c0-0.55-0.45-1-1-1zM3 13h-1V10H1V7h2v6z m7-2h-1V9h-1v6H6V9h-1v2h-1V7h6v4z m3-1h-1v3h-1V7h2v3z"></path></svg>
    <span class="num text-emphasized">
      25
    </span>
    contributors
</a>

      </li>
    </ul>

      <div class="repository-lang-stats">
        <ol class="repository-lang-stats-numbers">
          <li>
              <a href="/eligrey/FileSaver.js/search?l=javascript"  data-ga-click="Repository, language stats search click, location:repo overview">
                <span class="color-block language-color" style="background-color:#f1e05a;"></span>
                <span class="lang">JavaScript</span>
                <span class="percent">79.1%</span>
              </a>
          </li>
          <li>
              <a href="/eligrey/FileSaver.js/search?l=html"  data-ga-click="Repository, language stats search click, location:repo overview">
                <span class="color-block language-color" style="background-color:#e44b23;"></span>
                <span class="lang">HTML</span>
                <span class="percent">15.7%</span>
              </a>
          </li>
          <li>
              <a href="/eligrey/FileSaver.js/search?l=css"  data-ga-click="Repository, language stats search click, location:repo overview">
                <span class="color-block language-color" style="background-color:#563d7c;"></span>
                <span class="lang">CSS</span>
                <span class="percent">5.2%</span>
              </a>
          </li>
        </ol>
      </div>
    </div>
  </div>
</div>

  <div class="repository-lang-stats-graph js-toggle-lang-stats" title="Click for language details" data-ga-click="Repository, language bar stats toggle, location:repo overview">
    <span class="language-color" aria-label="JavaScript 79.1%" style="width:79.1%; background-color:#f1e05a;" itemprop="keywords">JavaScript</span>
    <span class="language-color" aria-label="HTML 15.7%" style="width:15.7%; background-color:#e44b23;" itemprop="keywords">HTML</span>
    <span class="language-color" aria-label="CSS 5.2%" style="width:5.2%; background-color:#563d7c;" itemprop="keywords">CSS</span>
  </div>


<div class="file-navigation in-mid-page">

    <div class="select-menu get-repo-select-menu js-menu-container right select-menu-modal-right">
  <button class="btn btn-sm btn-primary select-menu-button js-menu-target"
    title="Clone or download this repository"
    type="button" aria-label="Clone or download this repository" tabindex="0" aria-haspopup="true">
    <span>Clone or download</span>
  </button>

  <div class="select-menu-modal-holder dropdown-menu-content js-menu-content" aria-hidden="true">
    <div class="get-repo-modal dropdown-menu dropdown-menu-sw pb-0 js-toggler-container ">
      <div class="clone-options https-clone-options">
        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/users/set_protocol?protocol_selector=ssh&amp;protocol_type=clone" class="right" data-form-nonce="9f111d64e28d2e53430d47f25015bae55cd27c97" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="I3gM+Ppd2j5DcVJa95nJnVinrp8Nz+zY5Xq2TzcxUz9rzLtJKiwzb4tIDCIMXrLMzT+bV4YRAgEm391EcRfOzg==" /></div>
          <button type="submit" class="btn-link btn-change-protocol js-toggler-target">
            Use SSH
          </button>
</form>
        <h4 class="mb-2">
          Clone with HTTPS
          <a class="muted-link" href="https://help.github.com/articles/which-remote-url-should-i-use" target="_blank">
            <svg aria-hidden="true" class="octicon octicon-question" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M6 10h2v2H6V10z m4-3.5c0 2.14-2 2.5-2 2.5H6c0-0.55 0.45-1 1-1h0.5c0.28 0 0.5-0.22 0.5-0.5v-1c0-0.28-0.22-0.5-0.5-0.5h-1c-0.28 0-0.5 0.22-0.5 0.5v0.5H4c0-1.5 1.5-3 3-3s3 1 3 2.5zM7 2.3c3.14 0 5.7 2.56 5.7 5.7S10.14 13.7 7 13.7 1.3 11.14 1.3 8s2.56-5.7 5.7-5.7m0-1.3C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7S10.86 1 7 1z"></path></svg>
          </a>
        </h4>
        <p class="mb-1 get-repo-decription-text">
          Use Git or checkout with SVN using the web URL.
        </p>

        <div class="input-group js-zeroclipboard-container">
  <input type="text" class="form-control input-monospace input-sm js-zeroclipboard-target js-url-field" value="https://github.com/eligrey/FileSaver.js.git" aria-label="Clone this repository at https://github.com/eligrey/FileSaver.js.git" readonly>
  <div class="input-group-button">
    <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><svg aria-hidden="true" class="octicon octicon-clippy" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M2 12h4v1H2v-1z m5-6H2v1h5v-1z m2 3V7L6 10l3 3V11h5V9H9z m-4.5-1H2v1h2.5v-1zM2 11h2.5v-1H2v1z m9 1h1v2c-0.02 0.28-0.11 0.52-0.3 0.7s-0.42 0.28-0.7 0.3H1c-0.55 0-1-0.45-1-1V3c0-0.55 0.45-1 1-1h3C4 0.89 4.89 0 6 0s2 0.89 2 2h3c0.55 0 1 0.45 1 1v5h-1V5H1v9h10V12zM2 4h8c0-0.55-0.45-1-1-1h-1c-0.55 0-1-0.45-1-1s-0.45-1-1-1-1 0.45-1 1-0.45 1-1 1h-1c-0.55 0-1 0.45-1 1z"></path></svg></button>
  </div>
</div>

      </div>

      <div class="clone-options ssh-clone-options">
        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/users/set_protocol?protocol_selector=https&amp;protocol_type=clone" class="right" data-form-nonce="9f111d64e28d2e53430d47f25015bae55cd27c97" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="nSWGwozJiUUOPeZQhBTzY+0flSeEbqpCRi2uapmmfwqHFBs/4ZAFljctoC1wkYFbLS/lAwCNReItpv8G7/xa3A==" /></div>
          <button type="submit" class="btn-link btn-change-protocol js-toggler-target">
            Use HTTPS
          </button>
</form>
        <h4 class="mb-2">
          Clone with SSH
          <a class="muted-link" href="https://help.github.com/articles/which-remote-url-should-i-use" target="_blank">
            <svg aria-hidden="true" class="octicon octicon-question" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M6 10h2v2H6V10z m4-3.5c0 2.14-2 2.5-2 2.5H6c0-0.55 0.45-1 1-1h0.5c0.28 0 0.5-0.22 0.5-0.5v-1c0-0.28-0.22-0.5-0.5-0.5h-1c-0.28 0-0.5 0.22-0.5 0.5v0.5H4c0-1.5 1.5-3 3-3s3 1 3 2.5zM7 2.3c3.14 0 5.7 2.56 5.7 5.7S10.14 13.7 7 13.7 1.3 11.14 1.3 8s2.56-5.7 5.7-5.7m0-1.3C3.14 1 0 4.14 0 8s3.14 7 7 7 7-3.14 7-7S10.86 1 7 1z"></path></svg>
          </a>
        </h4>
        <p class="mb-1 get-repo-decription-text">
          Use an SSH key and passphrase from account.
        </p>

        <div class="input-group js-zeroclipboard-container">
  <input type="text" class="form-control input-monospace input-sm js-zeroclipboard-target js-url-field" value="git@github.com:eligrey/FileSaver.js.git" aria-label="Clone this repository at git@github.com:eligrey/FileSaver.js.git" readonly>
  <div class="input-group-button">
    <button aria-label="Copy to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button"><svg aria-hidden="true" class="octicon octicon-clippy" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M2 12h4v1H2v-1z m5-6H2v1h5v-1z m2 3V7L6 10l3 3V11h5V9H9z m-4.5-1H2v1h2.5v-1zM2 11h2.5v-1H2v1z m9 1h1v2c-0.02 0.28-0.11 0.52-0.3 0.7s-0.42 0.28-0.7 0.3H1c-0.55 0-1-0.45-1-1V3c0-0.55 0.45-1 1-1h3C4 0.89 4.89 0 6 0s2 0.89 2 2h3c0.55 0 1 0.45 1 1v5h-1V5H1v9h10V12zM2 4h8c0-0.55-0.45-1-1-1h-1c-0.55 0-1-0.45-1-1s-0.45-1-1-1-1 0.45-1 1-0.45 1-1 1h-1c-0.55 0-1 0.45-1 1z"></path></svg></button>
  </div>
</div>

      </div>

      <div class="mt-2">
        
<a href="/eligrey/FileSaver.js/archive/master.zip"
   class="btn btn-outline get-repo-btn
"
   rel="nofollow"
   data-ga-click="Repository, download zip, location:repo overview">
  Download ZIP
</a>

      </div>
    </div>
  </div>
</div>


  <div class="btn-group right">

    <a href="/eligrey/FileSaver.js/find/master"
      class="btn btn-sm empty-icon right"
      data-pjax
      data-hotkey="t"
      data-ga-click="Repository, find file, location:repo overview">
      Find file
    </a>
  </div>

  
<div class="select-menu branch-select-menu js-menu-container js-select-menu left">
  <button class="btn btn-sm select-menu-button js-menu-target css-truncate" data-hotkey="w"
    title="master"
    type="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <i>Branch:</i>
    <span class="js-select-button css-truncate-target">master</span>
  </button>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <svg aria-label="Close" class="octicon octicon-x js-menu-close" height="16" role="img" version="1.1" viewBox="0 0 12 16" width="12"><path d="M7.48 8l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75-1.48-1.48 3.75-3.75L0.77 4.25l1.48-1.48 3.75 3.75 3.75-3.75 1.48 1.48-3.75 3.75z"></path></svg>
        <span class="select-menu-title">Switch branches/tags</span>
      </div>

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="form-control js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" data-filter-placeholder="Filter branches/tags" class="js-select-menu-tab" role="tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" data-filter-placeholder="Find a tag…" class="js-select-menu-tab" role="tab">Tags</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches" role="menu">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open selected"
               href="/eligrey/FileSaver.js/tree/master"
               data-name="master"
               data-skip-pjax="true"
               rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target js-select-menu-filter-text" title="master">
                master
              </span>
            </a>
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open "
              href="/eligrey/FileSaver.js/tree/1.2.0"
              data-name="1.2.0"
              data-skip-pjax="true"
              rel="nofollow">
              <svg aria-hidden="true" class="octicon octicon-check select-menu-item-icon" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M12 5L4 13 0 9l1.5-1.5 2.5 2.5 6.5-6.5 1.5 1.5z"></path></svg>
              <span class="select-menu-item-text css-truncate-target" title="1.2.0">
                1.2.0
              </span>
            </a>
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div>

    </div>
  </div>
</div>


      <button type="button" class="btn btn-sm disabled tooltipped tooltipped-n new-pull-request-btn" aria-label="You must be signed in to create a pull request">
        New pull request
      </button>

  <div class="breadcrumb">
    
  </div>
</div>





  <div class="commit-tease js-details-container">
    <span class="right">
      Latest commit
      <a class="commit-tease-sha" href="/eligrey/FileSaver.js/commit/242c1dccc1b2f859afbe3d15ad39fb71f151d5de" data-pjax>
        242c1dc
      </a>
      <span itemprop="dateModified"><relative-time datetime="2016-05-25T21:43:11Z">May 25, 2016</relative-time></span>
    </span>


    <span class="commit-author-section">
      <img alt="@jimmywarting" class="avatar" height="20" src="https://avatars0.githubusercontent.com/u/1148376?v=3&amp;s=40" width="20" />
      <a href="/jimmywarting" class="user-mention" rel="contributor">jimmywarting</a>
    </span>

        <a href="/eligrey/FileSaver.js/commit/242c1dccc1b2f859afbe3d15ad39fb71f151d5de" class="message" data-pjax="true" title="closes #134">closes</a> <a href="https://github.com/eligrey/FileSaver.js/issues/134" class="issue-link js-issue-link" data-url="https://github.com/eligrey/FileSaver.js/issues/134" data-id="62812196" data-error-text="Failed to load issue title" data-permission-text="Issue title is private">#134</a>
    </span>

  </div>


<div class="file-wrap">

  <a href="/eligrey/FileSaver.js/tree/242c1dccc1b2f859afbe3d15ad39fb71f151d5de" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

  <table class="files js-navigation-container js-active-navigation-container" data-pjax>


    <tbody>
      <tr class="warning include-fragment-error">
        <td class="icon"><svg aria-hidden="true" class="octicon octicon-alert" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M15.72 12.5l-6.85-11.98C8.69 0.21 8.36 0.02 8 0.02s-0.69 0.19-0.87 0.5l-6.85 11.98c-0.18 0.31-0.18 0.69 0 1C0.47 13.81 0.8 14 1.15 14h13.7c0.36 0 0.69-0.19 0.86-0.5S15.89 12.81 15.72 12.5zM9 12H7V10h2V12zM9 9H7V5h2V9z"></path></svg></td>
        <td class="content" colspan="3">Failed to load latest commit information.</td>
      </tr>

        <tr class="js-navigation-item">
          <td class="icon">
            <svg aria-hidden="true" class="octicon octicon-file-directory" height="16" version="1.1" viewBox="0 0 14 16" width="14"><path d="M13 4H7v-1c0-0.66-0.31-1-1-1H1c-0.55 0-1 0.45-1 1v10c0 0.55 0.45 1 1 1h12c0.55 0 1-0.45 1-1V5c0-0.55-0.45-1-1-1z m-7 0H1v-1h5v1z"></path></svg>
            <img alt="" class="spinner" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </td>
          <td class="content">
            <span class="css-truncate css-truncate-target"><a href="/eligrey/FileSaver.js/tree/master/demo" class="js-navigation-open" id="fe01ce2a7fbac8fafaed7c982a04e229-085c6dfb5f02300f404bcf28738955cb30533361" title="demo">demo</a></span>
          </td>
          <td class="message">
            <span class="css-truncate css-truncate-target">
                  <a href="/eligrey/FileSaver.js/commit/242c1dccc1b2f859afbe3d15ad39fb71f151d5de" class="message" data-pjax="true" title="closes #134">closes</a> <a href="https://github.com/eligrey/FileSaver.js/issues/134" class="issue-link js-issue-link" data-url="https://github.com/eligrey/FileSaver.js/issues/134" data-id="62812196" data-error-text="Failed to load issue title" data-permission-text="Issue title is private">#134</a>
            </span>
          </td>
          <td class="age">
            <span class="css-truncate css-truncate-target"><time-ago datetime="2016-05-25T21:43:11Z">May 25, 2016</time-ago></span>
          </td>
        </tr>
        <tr class="js-navigation-item">
          <td class="icon">
            <svg aria-hidden="true" class="octicon octicon-file-text" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M6 5H2v-1h4v1zM2 8h7v-1H2v1z m0 2h7v-1H2v1z m0 2h7v-1H2v1z m10-7.5v9.5c0 0.55-0.45 1-1 1H1c-0.55 0-1-0.45-1-1V2c0-0.55 0.45-1 1-1h7.5l3.5 3.5z m-1 0.5L8 2H1v12h10V5z"></path></svg>
            <img alt="" class="spinner" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </td>
          <td class="content">
            <span class="css-truncate css-truncate-target"><a href="/eligrey/FileSaver.js/blob/master/FileSaver.js" class="js-navigation-open" id="a1994ccf4140c4d9a0fdecf2698de179-d54e85cfac3ee30a7f8d4acb043f3ee38605c412" title="FileSaver.js">FileSaver.js</a></span>
          </td>
          <td class="message">
            <span class="css-truncate css-truncate-target">
                  <a href="/eligrey/FileSaver.js/commit/a6d11998e279e94f2926b2a897231355dfab48ab" class="message" data-pjax="true" title="Now use minor version instead of date">Now use minor version instead of date</a>
            </span>
          </td>
          <td class="age">
            <span class="css-truncate css-truncate-target"><time-ago datetime="2016-05-25T20:22:13Z">May 25, 2016</time-ago></span>
          </td>
        </tr>
        <tr class="js-navigation-item">
          <td class="icon">
            <svg aria-hidden="true" class="octicon octicon-file-text" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M6 5H2v-1h4v1zM2 8h7v-1H2v1z m0 2h7v-1H2v1z m0 2h7v-1H2v1z m10-7.5v9.5c0 0.55-0.45 1-1 1H1c-0.55 0-1-0.45-1-1V2c0-0.55 0.45-1 1-1h7.5l3.5 3.5z m-1 0.5L8 2H1v12h10V5z"></path></svg>
            <img alt="" class="spinner" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </td>
          <td class="content">
            <span class="css-truncate css-truncate-target"><a href="/eligrey/FileSaver.js/blob/master/FileSaver.min.js" class="js-navigation-open" id="290258ac7bf24d47d0b0011ba70e063a-420b796fe4364dd0a726467a1c42394210b2ef98" title="FileSaver.min.js">FileSaver.min.js</a></span>
          </td>
          <td class="message">
            <span class="css-truncate css-truncate-target">
                  <a href="/eligrey/FileSaver.js/commit/89a12bd9ac23f8e02b9427601e5c320956847532" class="message" data-pjax="true" title="Added build command with package.json">Added build command with package.json</a>
            </span>
          </td>
          <td class="age">
            <span class="css-truncate css-truncate-target"><time-ago datetime="2016-05-25T21:33:42Z">May 25, 2016</time-ago></span>
          </td>
        </tr>
        <tr class="js-navigation-item">
          <td class="icon">
            <svg aria-hidden="true" class="octicon octicon-file-text" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M6 5H2v-1h4v1zM2 8h7v-1H2v1z m0 2h7v-1H2v1z m0 2h7v-1H2v1z m10-7.5v9.5c0 0.55-0.45 1-1 1H1c-0.55 0-1-0.45-1-1V2c0-0.55 0.45-1 1-1h7.5l3.5 3.5z m-1 0.5L8 2H1v12h10V5z"></path></svg>
            <img alt="" class="spinner" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </td>
          <td class="content">
            <span class="css-truncate css-truncate-target"><a href="/eligrey/FileSaver.js/blob/master/LICENSE.md" class="js-navigation-open" id="37854d19817c792316d481f5beb93cc7-f4e447e0b0ae9f418d1b693a518a0c6417dfae04" itemprop="license" title="LICENSE.md">LICENSE.md</a></span>
          </td>
          <td class="message">
            <span class="css-truncate css-truncate-target">
                  <a href="/eligrey/FileSaver.js/commit/921c78ff43fdbb69e3a35f8e67ba8f0da5f20fd6" class="message" data-pjax="true" title="Change UTF-16 BOM to UTF-8

Fixes #219">Change UTF-16 BOM to UTF-8</a>
            </span>
          </td>
          <td class="age">
            <span class="css-truncate css-truncate-target"><time-ago datetime="2016-05-21T01:37:27Z">May 20, 2016</time-ago></span>
          </td>
        </tr>
        <tr class="js-navigation-item">
          <td class="icon">
            <svg aria-hidden="true" class="octicon octicon-file-text" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M6 5H2v-1h4v1zM2 8h7v-1H2v1z m0 2h7v-1H2v1z m0 2h7v-1H2v1z m10-7.5v9.5c0 0.55-0.45 1-1 1H1c-0.55 0-1-0.45-1-1V2c0-0.55 0.45-1 1-1h7.5l3.5 3.5z m-1 0.5L8 2H1v12h10V5z"></path></svg>
            <img alt="" class="spinner" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </td>
          <td class="content">
            <span class="css-truncate css-truncate-target"><a href="/eligrey/FileSaver.js/blob/master/README.md" class="js-navigation-open" id="04c6e90faac2675aa89e2176d2eec7d8-6e7cb1b63e8f860749c11dc90b7dd52ab3de1ded" title="README.md">README.md</a></span>
          </td>
          <td class="message">
            <span class="css-truncate css-truncate-target">
                  <a href="/eligrey/FileSaver.js/commit/242c1dccc1b2f859afbe3d15ad39fb71f151d5de" class="message" data-pjax="true" title="closes #134">closes</a> <a href="https://github.com/eligrey/FileSaver.js/issues/134" class="issue-link js-issue-link" data-url="https://github.com/eligrey/FileSaver.js/issues/134" data-id="62812196" data-error-text="Failed to load issue title" data-permission-text="Issue title is private">#134</a>
            </span>
          </td>
          <td class="age">
            <span class="css-truncate css-truncate-target"><time-ago datetime="2016-05-25T21:43:11Z">May 25, 2016</time-ago></span>
          </td>
        </tr>
        <tr class="js-navigation-item">
          <td class="icon">
            <svg aria-hidden="true" class="octicon octicon-file-text" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M6 5H2v-1h4v1zM2 8h7v-1H2v1z m0 2h7v-1H2v1z m0 2h7v-1H2v1z m10-7.5v9.5c0 0.55-0.45 1-1 1H1c-0.55 0-1-0.45-1-1V2c0-0.55 0.45-1 1-1h7.5l3.5 3.5z m-1 0.5L8 2H1v12h10V5z"></path></svg>
            <img alt="" class="spinner" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </td>
          <td class="content">
            <span class="css-truncate css-truncate-target"><a href="/eligrey/FileSaver.js/blob/master/bower.json" class="js-navigation-open" id="0a08a7565aba4405282251491979bb6b-9d1154edd5a94bd3ff249034b62b03f293e266c1" title="bower.json">bower.json</a></span>
          </td>
          <td class="message">
            <span class="css-truncate css-truncate-target">
                  <a href="/eligrey/FileSaver.js/commit/cb8e076073d44a994e29dd653a02c95af2036ad5" class="message" data-pjax="true" title="Added npm and bower son">Added npm and bower son</a>
            </span>
          </td>
          <td class="age">
            <span class="css-truncate css-truncate-target"><time-ago datetime="2016-05-25T21:04:22Z">May 25, 2016</time-ago></span>
          </td>
        </tr>
        <tr class="js-navigation-item">
          <td class="icon">
            <svg aria-hidden="true" class="octicon octicon-file-text" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M6 5H2v-1h4v1zM2 8h7v-1H2v1z m0 2h7v-1H2v1z m0 2h7v-1H2v1z m10-7.5v9.5c0 0.55-0.45 1-1 1H1c-0.55 0-1-0.45-1-1V2c0-0.55 0.45-1 1-1h7.5l3.5 3.5z m-1 0.5L8 2H1v12h10V5z"></path></svg>
            <img alt="" class="spinner" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
          </td>
          <td class="content">
            <span class="css-truncate css-truncate-target"><a href="/eligrey/FileSaver.js/blob/master/package.json" class="js-navigation-open" id="b9cfc7f2cdf78a7f4b91a753d10865a2-4e4fd78f36d827f169523490b5113cfb5466b14e" title="package.json">package.json</a></span>
          </td>
          <td class="message">
            <span class="css-truncate css-truncate-target">
                  <a href="/eligrey/FileSaver.js/commit/89a12bd9ac23f8e02b9427601e5c320956847532" class="message" data-pjax="true" title="Added build command with package.json">Added build command with package.json</a>
            </span>
          </td>
          <td class="age">
            <span class="css-truncate css-truncate-target"><time-ago datetime="2016-05-25T21:33:42Z">May 25, 2016</time-ago></span>
          </td>
        </tr>
    </tbody>
  </table>

</div>



  <div id="readme" class="readme boxed-group clearfix announce instapaper_body md">
    <h3>
      <svg aria-hidden="true" class="octicon octicon-book" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M2 5h4v1H2v-1z m0 3h4v-1H2v1z m0 2h4v-1H2v1z m11-5H9v1h4v-1z m0 2H9v1h4v-1z m0 2H9v1h4v-1z m2-6v9c0 0.55-0.45 1-1 1H8.5l-1 1-1-1H1c-0.55 0-1-0.45-1-1V3c0-0.55 0.45-1 1-1h5.5l1 1 1-1h5.5c0.55 0 1 0.45 1 1z m-8 0.5l-0.5-0.5H1v9h6V3.5z m7-0.5H8.5l-0.5 0.5v8.5h6V3z"></path></svg>
      README.md
    </h3>

      <article class="markdown-body entry-content" itemprop="text"><h1><a id="user-content-filesaverjs" class="anchor" href="#filesaverjs" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>FileSaver.js</h1>

<p>FileSaver.js implements the <code>saveAs()</code> FileSaver interface in browsers that do
not natively support it. There is a <a href="http://eligrey.com/demos/FileSaver.js/">FileSaver.js demo</a> that demonstrates saving
various media types.</p>

<p>FileSaver.js is the solution to saving files on the client-side, and is perfect for
webapps that need to generate files, or for saving sensitive information that shouldn't be
sent to an external server.</p>

<p>Looking for <code>canvas.toBlob()</code> for saving canvases? Check out
<a href="https://github.com/eligrey/canvas-toBlob.js">canvas-toBlob.js</a> for a cross-browser implementation.</p>

<h2><a id="user-content-supported-browsers" class="anchor" href="#supported-browsers" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Supported browsers</h2>

<table><thead>
<tr>
<th>Browser</th>
<th>Constructs as</th>
<th>Filenames</th>
<th>Max Blob Size</th>
<th>Dependencies</th>
</tr>
</thead><tbody>
<tr>
<td>Firefox 20+</td>
<td>Blob</td>
<td>Yes</td>
<td>800 MiB</td>
<td>None</td>
</tr>
<tr>
<td>Firefox &lt; 20</td>
<td>data: URI</td>
<td>No</td>
<td>n/a</td>
<td><a href="https://github.com/eligrey/Blob.js">Blob.js</a></td>
</tr>
<tr>
<td>Chrome</td>
<td>Blob</td>
<td>Yes</td>
<td><a href="https://code.google.com/p/chromium/issues/detail?id=375297">500 MiB</a></td>
<td>None</td>
</tr>
<tr>
<td>Chrome for Android</td>
<td>Blob</td>
<td>Yes</td>
<td><a href="https://code.google.com/p/chromium/issues/detail?id=375297">500 MiB</a></td>
<td>None</td>
</tr>
<tr>
<td>Edge</td>
<td>Blob</td>
<td>Yes</td>
<td>?</td>
<td>None</td>
</tr>
<tr>
<td>IE 10+</td>
<td>Blob</td>
<td>Yes</td>
<td>600 MiB</td>
<td>None</td>
</tr>
<tr>
<td>Opera 15+</td>
<td>Blob</td>
<td>Yes</td>
<td>500 MiB</td>
<td>None</td>
</tr>
<tr>
<td>Opera &lt; 15</td>
<td>data: URI</td>
<td>No</td>
<td>n/a</td>
<td><a href="https://github.com/eligrey/Blob.js">Blob.js</a></td>
</tr>
<tr>
<td>Safari 6.1+*</td>
<td>Blob</td>
<td>No</td>
<td>?</td>
<td>None</td>
</tr>
<tr>
<td>Safari &lt; 6</td>
<td>data: URI</td>
<td>No</td>
<td>n/a</td>
<td><a href="https://github.com/eligrey/Blob.js">Blob.js</a></td>
</tr>
</tbody></table>

<p>Feature detection is possible:</p>

<div class="highlight highlight-source-js"><pre><span class="pl-k">try</span> {
    <span class="pl-k">var</span> isFileSaverSupported <span class="pl-k">=</span> <span class="pl-k">!!</span><span class="pl-k">new</span> <span class="pl-en">Blob</span>;
} <span class="pl-k">catch</span> (e) {}</pre></div>

<h3><a id="user-content-ie--10" class="anchor" href="#ie--10" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>IE &lt; 10</h3>

<p>It is possible to save text files in IE &lt; 10 without Flash-based polyfills.
See <a href="https://github.com/koffsyrup/FileSaver.js#examples">ChenWenBrian and koffsyrup's <code>saveTextAs()</code></a> for more details.</p>

<h3><a id="user-content-safari-61" class="anchor" href="#safari-61" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Safari 6.1+</h3>

<p>Blobs may be opened instead of saved sometimes—you may have to direct your Safari users to manually
press <kbd>⌘</kbd>+<kbd>S</kbd> to save the file after it is opened. Using the <code>application/octet-stream</code> MIME type to force downloads <a href="https://github.com/eligrey/FileSaver.js/issues/12#issuecomment-47247096">can cause issues in Safari</a>.</p>

<h3><a id="user-content-ios" class="anchor" href="#ios" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>iOS</h3>

<p>saveAs must be run within a user interaction event such as onTouchDown or onClick; setTimeout will prevent saveAs from triggering. Due to restrictions in iOS saveAs opens in a new window instead of downloading, if you want this fixed please <a href="https://bugs.webkit.org/show_bug.cgi?id=102914">tell Apple</a> how this bug is affecting you.</p>

<h2><a id="user-content-syntax" class="anchor" href="#syntax" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Syntax</h2>

<div class="highlight highlight-source-js"><pre>FileSaver <span class="pl-en">saveAs</span>(Blob data, DOMString filename, optional <span class="pl-c1">Boolean</span> disableAutoBOM)</pre></div>

<p>Pass <code>true</code> for <code>disableAutoBOM</code> if you don't want FileSaver.js to automatically provide Unicode text encoding hints (see: <a href="https://en.wikipedia.org/wiki/Byte_order_mark">byte order mark</a>).</p>

<h2><a id="user-content-examples" class="anchor" href="#examples" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Examples</h2>

<h3><a id="user-content-saving-text" class="anchor" href="#saving-text" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Saving text</h3>

<div class="highlight highlight-source-js"><pre><span class="pl-k">var</span> blob <span class="pl-k">=</span> <span class="pl-k">new</span> <span class="pl-en">Blob</span>([<span class="pl-s"><span class="pl-pds">"</span>Hello, world!<span class="pl-pds">"</span></span>], {type<span class="pl-k">:</span> <span class="pl-s"><span class="pl-pds">"</span>text/plain;charset=utf-8<span class="pl-pds">"</span></span>});
<span class="pl-en">saveAs</span>(blob, <span class="pl-s"><span class="pl-pds">"</span>hello world.txt<span class="pl-pds">"</span></span>);</pre></div>

<p>The standard W3C File API <a href="https://developer.mozilla.org/en-US/docs/DOM/Blob"><code>Blob</code></a> interface is not available in all browsers.
<a href="https://github.com/eligrey/Blob.js">Blob.js</a> is a cross-browser <code>Blob</code> implementation that solves this.</p>

<h3><a id="user-content-saving-a-canvas" class="anchor" href="#saving-a-canvas" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Saving a canvas</h3>

<div class="highlight highlight-source-js"><pre><span class="pl-k">var</span> canvas <span class="pl-k">=</span> <span class="pl-c1">document</span>.<span class="pl-c1">getElementById</span>(<span class="pl-s"><span class="pl-pds">"</span>my-canvas<span class="pl-pds">"</span></span>), ctx <span class="pl-k">=</span> <span class="pl-smi">canvas</span>.<span class="pl-en">getContext</span>(<span class="pl-s"><span class="pl-pds">"</span>2d<span class="pl-pds">"</span></span>);
<span class="pl-c">// draw to canvas...</span>
<span class="pl-smi">canvas</span>.<span class="pl-en">toBlob</span>(<span class="pl-k">function</span>(<span class="pl-smi">blob</span>) {
    <span class="pl-en">saveAs</span>(blob, <span class="pl-s"><span class="pl-pds">"</span>pretty image.png<span class="pl-pds">"</span></span>);
});</pre></div>

<p>Note: The standard HTML5 <code>canvas.toBlob()</code> method is not available in all browsers.
<a href="https://github.com/eligrey/canvas-toBlob.js">canvas-toBlob.js</a> is a cross-browser <code>canvas.toBlob()</code> that polyfills this.</p>

<p><a href="https://camo.githubusercontent.com/e45db383ed87f57d340c88f92da60eb35a29cb04/68747470733a2f2f696e2e676574636c69636b792e636f6d2f3231323731326e732e676966" target="_blank"><img src="https://camo.githubusercontent.com/e45db383ed87f57d340c88f92da60eb35a29cb04/68747470733a2f2f696e2e676574636c69636b792e636f6d2f3231323731326e732e676966" alt="Tracking image" data-canonical-src="https://in.getclicky.com/212712ns.gif" style="max-width:100%;"></a></p>

<h2><a id="user-content-contributing" class="anchor" href="#contributing" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Contributing</h2>

<p>The <code>FileSaver.js</code> distribution file is compiled with Uglify.js like so:</p>

<div class="highlight highlight-source-shell"><pre>uglifyjs FileSaver.js --mangle --comments /@source/ <span class="pl-k">&gt;</span> FileSaver.min.js
<span class="pl-c"># or simply:</span>
npm run build</pre></div>

<p>Please make sure you build a production version before submitting a pull request.</p>

<h2><a id="user-content-installation" class="anchor" href="#installation" aria-hidden="true"><svg aria-hidden="true" class="octicon octicon-link" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M4 9h1v1h-1c-1.5 0-3-1.69-3-3.5s1.55-3.5 3-3.5h4c1.45 0 3 1.69 3 3.5 0 1.41-0.91 2.72-2 3.25v-1.16c0.58-0.45 1-1.27 1-2.09 0-1.28-1.02-2.5-2-2.5H4c-0.98 0-2 1.22-2 2.5s1 2.5 2 2.5z m9-3h-1v1h1c1 0 2 1.22 2 2.5s-1.02 2.5-2 2.5H9c-0.98 0-2-1.22-2-2.5 0-0.83 0.42-1.64 1-2.09v-1.16c-1.09 0.53-2 1.84-2 3.25 0 1.81 1.55 3.5 3 3.5h4c1.45 0 3-1.69 3-3.5s-1.5-3.5-3-3.5z"></path></svg></a>Installation</h2>

<div class="highlight highlight-source-shell"><pre>npm install file-saver --save
bower install file-saver</pre></div>
</article>
  </div>


  </div>
  <div class="modal-backdrop"></div>
</div>


    </div>
  </div>

    </div>

        <div class="container site-footer-container">
  <div class="site-footer" role="contentinfo">
    <ul class="site-footer-links right">
        <li><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
      <li><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li><a href="https://github.com/blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a href="https://github.com/about" data-ga-click="Footer, go to about, text:about">About</a></li>

    </ul>

    <a href="https://github.com" aria-label="Homepage" class="site-footer-mark" title="GitHub">
      <svg aria-hidden="true" class="octicon octicon-mark-github" height="24" version="1.1" viewBox="0 0 16 16" width="24"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59 0.4 0.07 0.55-0.17 0.55-0.38 0-0.19-0.01-0.82-0.01-1.49-2.01 0.37-2.53-0.49-2.69-0.94-0.09-0.23-0.48-0.94-0.82-1.13-0.28-0.15-0.68-0.52-0.01-0.53 0.63-0.01 1.08 0.58 1.23 0.82 0.72 1.21 1.87 0.87 2.33 0.66 0.07-0.52 0.28-0.87 0.51-1.07-1.78-0.2-3.64-0.89-3.64-3.95 0-0.87 0.31-1.59 0.82-2.15-0.08-0.2-0.36-1.02 0.08-2.12 0 0 0.67-0.21 2.2 0.82 0.64-0.18 1.32-0.27 2-0.27 0.68 0 1.36 0.09 2 0.27 1.53-1.04 2.2-0.82 2.2-0.82 0.44 1.1 0.16 1.92 0.08 2.12 0.51 0.56 0.82 1.27 0.82 2.15 0 3.07-1.87 3.75-3.65 3.95 0.29 0.25 0.54 0.73 0.54 1.48 0 1.07-0.01 1.93-0.01 2.2 0 0.21 0.15 0.46 0.55 0.38C13.71 14.53 16 11.53 16 8 16 3.58 12.42 0 8 0z"></path></svg>
</a>
    <ul class="site-footer-links">
      <li>&copy; 2016 <span title="0.07826s from github-fe122-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="https://github.com/site/terms" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li><a href="https://github.com/security" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li><a href="https://github.com/contact" data-ga-click="Footer, go to contact, text:contact">Contact</a></li>
        <li><a href="https://help.github.com" data-ga-click="Footer, go to help, text:help">Help</a></li>
    </ul>
  </div>
</div>



    

    <div id="ajax-error-message" class="ajax-error-message flash flash-error">
      <svg aria-hidden="true" class="octicon octicon-alert" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M15.72 12.5l-6.85-11.98C8.69 0.21 8.36 0.02 8 0.02s-0.69 0.19-0.87 0.5l-6.85 11.98c-0.18 0.31-0.18 0.69 0 1C0.47 13.81 0.8 14 1.15 14h13.7c0.36 0 0.69-0.19 0.86-0.5S15.89 12.81 15.72 12.5zM9 12H7V10h2V12zM9 9H7V5h2V9z"></path></svg>
      <button type="button" class="flash-close js-flash-close js-ajax-error-dismiss" aria-label="Dismiss error">
        <svg aria-hidden="true" class="octicon octicon-x" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M7.48 8l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75-1.48-1.48 3.75-3.75L0.77 4.25l1.48-1.48 3.75 3.75 3.75-3.75 1.48 1.48-3.75 3.75z"></path></svg>
      </button>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/compat-7db58f8b7b91111107fac755dd8b178fe7db0f209ced51fc339c446ad3f8da2b.js"></script>
      <script crossorigin="anonymous" src="https://assets-cdn.github.com/assets/frameworks-e76ce42ce77c934586f7cacbe24d556dbe6fefdbe8b53a393644b18199f7c291.js"></script>
      <script async="async" crossorigin="anonymous" src="https://assets-cdn.github.com/assets/github-3403611476aba5449f7af712dbf7b488bbb552e0a3e93c55d36c058fe7968b46.js"></script>
      
      
      
      
      
      
    <div class="js-stale-session-flash stale-session-flash flash flash-warn flash-banner hidden">
      <svg aria-hidden="true" class="octicon octicon-alert" height="16" version="1.1" viewBox="0 0 16 16" width="16"><path d="M15.72 12.5l-6.85-11.98C8.69 0.21 8.36 0.02 8 0.02s-0.69 0.19-0.87 0.5l-6.85 11.98c-0.18 0.31-0.18 0.69 0 1C0.47 13.81 0.8 14 1.15 14h13.7c0.36 0 0.69-0.19 0.86-0.5S15.89 12.81 15.72 12.5zM9 12H7V10h2V12zM9 9H7V5h2V9z"></path></svg>
      <span class="signed-in-tab-flash">You signed in with another tab or window. <a href="">Reload</a> to refresh your session.</span>
      <span class="signed-out-tab-flash">You signed out in another tab or window. <a href="">Reload</a> to refresh your session.</span>
    </div>
    <div class="facebox" id="facebox" style="display:none;">
  <div class="facebox-popup">
    <div class="facebox-content" role="dialog" aria-labelledby="facebox-header" aria-describedby="facebox-description">
    </div>
    <button type="button" class="facebox-close js-facebox-close" aria-label="Close modal">
      <svg aria-hidden="true" class="octicon octicon-x" height="16" version="1.1" viewBox="0 0 12 16" width="12"><path d="M7.48 8l3.75 3.75-1.48 1.48-3.75-3.75-3.75 3.75-1.48-1.48 3.75-3.75L0.77 4.25l1.48-1.48 3.75 3.75 3.75-3.75 1.48 1.48-3.75 3.75z"></path></svg>
    </button>
  </div>
</div>

  </body>
</html>


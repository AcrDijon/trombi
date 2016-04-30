<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>{{title or 'No title'}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="" />
    <meta name="author" content="" />

    <!--CSS-START-->
    <link href="/resources/css/bootstrap.min.css" rel="stylesheet" />
    <link href="/resources/css/bootstrap-theme.min.css" rel="stylesheet" />
    <link href="/resources/css/style.css" rel="stylesheet" />
    <link href="/resources/css/lightbox.min.css" rel="stylesheet" />
    <link id="bsdp-css" href="/resources/css/datepicker3.css" rel="stylesheet">
    <link id="jqta-css" href="/resources/css/jquery-linedtextarea.css"
          rel="stylesheet">
    <link href="/resources/css/jquery.toastmessage.css" rel="stylesheet" />
    <!--CSS-END-->

    <!--[if lt IE 9]>
    <script src="/resources/js/html5.js"></script>
    <![endif]-->
</head>
<body>
    <nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="/">ACR Dijon</a>
        </div>
        <div id="navbar" class="collapse navbar-collapse">
          <ul class="nav navbar-nav">
            <li><a href="/member">Liste des Adhérents</a></li>
            <li><a href="/member/{{user.id}}">Ma fiche</a></li>
            % if user.is_super_user:
            <li><a href="/admin">Gestion</a></li>
            % end
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav>

    <div class="container">
        <div class="row">
            <div class="span12">
                <!--JS-START-->
                <script src="/resources/js/jquery.min.js"></script>
                <script src="/resources/js/bootstrap.min.js"></script>
                <script src="/resources/js/bootstrap-datepicker.js"></script>
                <script src="/resources/js/bootstrap-datepicker.fr.min.js" charset="UTF-8"></script>
                <!--JS-END-->
                <!-- CONTENT -->
                <div class="row">
                    <div class="span12" id="contentContainer">
                        {{!base}}
                    </div>
                </div>
                <!-- END-CONTENT -->
            </div><!--/span-->
        </div><!--/row-->

        <hr>

        <footer>
            <p>&copy; Tarek Ziadé - 2016</p>
        </footer>
    </div><!--/.fluid-container-->
</body>
</html>

<!DOCTYPE html>
<html>
<head>
    <title>HALLO</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <header>
        <h1>AAAAAAAAAAAAAAAAAAAAAAA</h1>
    </header>

    <div class="container">
        <nav>
            <a href="/">Home</a>
            <a href="?page=1.html">Page 1</a>
            <a href="?page=2.html">Page 2</a>
            <a href="?page=3.html">Page 3 </a>
            <a href="?page=4.html">Page 4 </a>
        </nav>

        <main>
            <div class="box">
                
                <?php
                    if (isset($_GET['page'])) {
                        $page = $_GET['page'];
                    } else {
                        $page = 'home';
                    }

                    if ($page == '1.html') {
                        require('1.html');
                    } 
                    elseif ($page == '2.html') {
                        require('2.html');
                    }
                    else if ($page == '3.html') {
                        require('3.html');
                    } 
                    else if ($page == '4.html') {
                        require('4.html');
                    } 
                    else {
                        require('home.html');
                    }
                ?>

            </div>
        </main>
    </div>

</body>
</html>
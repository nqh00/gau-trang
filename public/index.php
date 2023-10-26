<?php

function listFiles($directory) {
    $files = [];
    $items = scandir($directory);
    
    foreach ($items as $item) {
        if ($item != "." && $item != "..") {
            $path = $directory . '/' . $item;

            if (is_file($path)) {
                $files[] = ['type' => 'file', 'name' => $item, 'path' => $directory];
            } elseif (is_dir($path)) {
                $subFiles = listFiles($path);
                $files = array_merge($files, $subFiles);
            }
        }
    }

    return $files;
}

$directory = '/var/www/webdav/gautrang';
$files = listFiles($directory);

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Danh Sách Tệp Tin và Thư Mục</title>
</head>

<body>
    <h1>Danh Sách Tệp Tin và Thư Mục</h1>
    <ul>
        <?php foreach ($files as $file): ?>
            <li>
                <?php if ($file['type'] === 'file'): ?>
                    Tệp: <?php echo $file['name']; ?>
                    - <a href="/home<?php echo str_replace($directory, '', $file['path']) . '/' . $file['name']; ?>">Tải Xuống</a>
                <?php endif; ?>
            </li>
        <?php endforeach; ?>
    </ul>
</body>

</html>

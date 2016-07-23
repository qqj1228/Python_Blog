// upload_image.js
// 使用WebUploader组件实现上传图片功能
// 官网地址：http://fex.baidu.com/webuploader/

// 图片上传demo
jQuery(function() {
    var $ = jQuery,
        $list = $('#fileList'),
        // 优化retina, 在retina下这个值是2
        ratio = window.devicePixelRatio || 1,

        // 缩略图大小
        thumbnailWidth = 100 * ratio,
        thumbnailHeight = 100 * ratio,

        // Web Uploader实例
        uploader;

    // 初始化Web Uploader
    uploader = WebUploader.create({

        // 自动上传。
        auto: true,

        // swf文件路径
        swf: 'http://cdn.staticfile.org/webuploader/0.1.5/Uploader.swf',

        // 文件接收服务端。
        server: '/upload',

        // 选择文件的按钮。可选。
        // 内部根据当前运行是创建，可能是input元素，也可能是flash.
        pick: '#filePicker',

        // 只允许选择文件，可选。
        accept: {
            title: 'Images',
            extensions: 'gif,jpg,jpeg,bmp,png',
            mimeTypes: 'image/*'
        }
    });

    // 当有文件添加进来的时候
    uploader.on( 'fileQueued', function( file ) {
        var $li = $(
                '<div id="' + file.id + '" class="uk-thumbnail uk-thumbnail-mini uk-margin-small uk-margin-small-right">' +
                    '<img>' +
                    '<div class="uk-thumbnail-caption">' + file.name + '</div>' +
                '</div>'
            ),
        $img = $li.find('img');

        $list.append( $li );

        // 创建缩略图
        uploader.makeThumb( file, function( error, src ) {
            if ( error ) {
                $img.replaceWith('<span>不能预览</span>');
                return;
            }

            $img.attr( 'src', src );
        }, thumbnailWidth, thumbnailHeight );

        // 显示进度条
        var $ul = $( '#uploader' ),
            $progress = $ul.find('.uk-progress');
        $progress.removeClass('uk-hidden');
    });

    // 文件上传过程中创建进度条实时显示。
    uploader.on( 'uploadProgress', function( file, percentage ) {
        var $li = $( '#uploader' ),
            $percent = $li.find('.uk-progress-bar');

        $percent.css( 'width', percentage * 100 + '%' );
        $percent.text( percentage * 100 + '%' );
    });

    // 文件上传成功，给item添加成功class, 用样式标记上传成功。
    uploader.on( 'uploadSuccess', function( file, response ) {
        var $li = $( '#'+file.id ),
            $name = $li.find('.uk-thumbnail-caption');
        $name.text(response.filename);
    });

    // 文件上传失败，显示上传出错。
    uploader.on( 'uploadError', function( file ) {
        var $li = $( '#'+file.id ),
            $error = $li.find('div.error');

        // 避免重复创建
        if ( !$error.length ) {
            $error = $('<div class="error uk-thumbnail-caption" style="color:red;"></div>').appendTo( $li );
        }

        $error.text('上传失败!');
    });

    // 完成上传完了，成功或者失败，先隐藏进度条。
    uploader.on( 'uploadComplete', function( file ) {
        $( '#uploader' ).find('.uk-progress').addClass('uk-hidden');
    });
});

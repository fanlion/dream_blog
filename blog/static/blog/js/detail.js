$(document).ready(function () {
    // 为表单的必填文本框添加事件
    $("form :input").blur(function () {
        var $parent = $(this).parent();
        // 删除之前的错误提醒信息

        $parent.find(".msg").remove();
        var errorMsg = "";

        // 验证昵称
        if ($(this).is("#id_name")) {
            if ($.trim(this.value) === "") {
                errorMsg = "留下你的大名";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            } else if ($.trim(this.value).length > 20) {
                errorMsg = "昵称不要超过20字符";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            }
        }

        // 验证邮箱
        if ($(this).is("#id_email")) {
            if ($.trim(this.value) === "") {
                errorMsg = "留下你的邮箱";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            } else if ($.trim(this.value).length > 50) {
                errorMsg = "邮箱不要超过50字符";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            } else if (!/.+@.+\.[a-zA-Z]{2,4}$/.test($.trim(this.value))) {
                errorMsg = "请输入正确的E-Mail地址";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            }
        }

        // 验证个人主页
        if ($(this).is("#id_url")) {
            if ($.trim(this.value) !== "" && $.trim(this.value).length > 100) {
                errorMsg = "个人主页地址不要超过100字符";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            }
        }

        // 校验验证码
        if ($(this).is("#id_verify_code")) {
            if ($.trim(this.value) === "") {
                errorMsg = "验证码不能为空";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            } else if ($.trim(this.value).length > 20) {
                errorMsg = "验证码不要超过20字符";
                $parent.append("<span class='msg form-error'>" + errorMsg + "</span>");
            }
        }

    }).keyup(function () {
        // triggerHandler 防止事件执行完后，浏览器自动为标签获得焦点
        $(this).triggerHandler("blur");
        
    }).focus(function () {
        $(this).triggerHandler("blur");
    });

    // 校验评论内容
    $("#id_comment").blur(function () {
        var $parent = $(this).parent();
        var errorMsg = "";
        // 移除之前的提示框
        $parent.find(".msg").remove();
        if ($.trim(this.value) === "") {
            errorMsg = "评论不要为空";
            $parent.append("<span class='msg form-error'>" + errorMsg + "</span>")
        } else if ($.trim(this.value).length > 250) {
             errorMsg = "评论不要超过250字";
            $parent.append("<span class='msg form-error'>" + errorMsg + "</span>")
        }
    });


});

// 点击图片修改验证码
function ChangeCode(ths) {
    // 点击图片的时候修改图片src，达到刷新验证码的效果
    ths.src = $('#check_code').attr('src').split('?')[0] + '?' + Math.random();
}

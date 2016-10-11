function initNavActive()
{
    urlTable = {
        "/":"#nav-index",
        "/success":"#nav-success",
        "/fail":"#nav-fail",
        "/search":"#nav-search",
        "/uin":"#nav-uin",
    };
    
    pathname = document.location.pathname;
    targetNav = urlTable[pathname];

    $(targetNav).addClass("active")

}

function showTable(data)
{
    console.log("show Table");
    console.log(data);
    $(".table-search-content").remove();
    if (data == "[]"){
        showAlert('#search', "search-alert", "结果为空");
        return;
    }

    var tds = eval(data);
    for (td in tds)
    {
        console.log(td);
        var line = "<tr class='table-search-content'>";
        line += "<td>"+ tds[td]['sendtime'] + "</td>"
        line += "<td>"+ tds[td]['queue'] + "</td>"
        line += "<td>"+ tds[td]['uin'] + "</td>"
        line += "<td>"+ tds[td]['code'] + "</td>"
        line += "<td>"+ tds[td]['retmessage'] + "</td>"
        line += "<td>"+ tds[td]['status'] + "<br/><a href='/detail/" + tds[td]['requestid'] + "'>详情</a></td>"
        line += "</tr>"
        $("#table-search-menu").after(line)
    }
}

function showUin(data)
{
    console.log("show Uin");
    console.log(data);
    $(".table-uin-content").remove();
    if (data == "[]"){
        showAlert('#uin', "uin-alert", "结果为空");
        return;
    }

    var tds = eval(data);
    for (td in tds)
    {
        console.log(td);
        var line = "<tr class='table-uin-content'>";
        line += "<td>"+ tds[td]['uin'] + "</td>"
        line += "<td>"+ tds[td]['channel'] + "</td>"
        line += "<td>"+ tds[td]['token'] + "</td>"
        line += "</tr>"
        $("#table-uin-menu").after(line)
    }
}
function searchUin(argv)
{
    requestPath = '/search/uin/' + argv;
    console.log("requestPath:" + requestPath);
    $.get(requestPath, function(data, status){
            showTable(data);
        })
}

function searchMsgid(argv)
{
    requestPath = '/search/msgid/' + argv;
    console.log("requestPath:" + requestPath);
    $.get(requestPath, function(data, status){
        if (data == "[]") {
            searchUin(argv)
        } else {
            showTable(data)
        }
    })
}

function getUin(argv){
    requestPath = '/uin/search/' + argv;
    $.get(requestPath, function(data, status){
        showUin(data);
    })
}

function showAlert(after, id, msg)
{
    content =   '<div class="alert alert-warning alert-dismissible" role="alert" id="' +  id + '">' +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>' + 
                '<strong>Warning!</strong> ' + msg + '</div>'
    $(after).after(content);
}

function search(){
    $("#search-alert").alert('close');
    console.log("begin");
    argv = $("#search-argv").val()
    console.log("get argv:" + argv)
    argvLen = argv.length
    
    if (argvLen == 0 ){
        showAlert('#search', 'search-alert', "参数不能为空");
        return;
    }

    if (argvLen == 13) {
        searchMsgid(argv);
    } else {
        searchUin(argv);
    }
}

function uin(){
    $("#uin-alert").alert('close');
    console.log("begin");
    argv = $("#uin-argv").val();
    argvLen = argv.length;

    if (argvLen == 0){
        showAlert('#uin', 'uin-alert', "参数不能为空");
        return;
    }

    getUin(argv)
}

$(document).ready(function(){
    initNavActive();
    $("#search-argv").keyup(function(e){
        if(e.keyCode == 13) {
            search();
        }
    });
    $("#uin-argv").keyup(function(e){
        if(e.keyCode == 13) {
            uin();
        }
    });
});


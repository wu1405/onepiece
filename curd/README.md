# Django CURD(create,update,read,delte)示例
首选设计url



        /curd/list            列出表里的所有记录，并带翻页功能
        /curd/add             添加记录，添加完后跳转到/curd/list
        /curd/delete          在/curd/list里点击删除按钮，调用这个链接删除完后返回/curd/list
        /curd/update          在/curd/list页面里点击记录，跳转到记录明细页面,然后调用这个url进行更新
        /curd/info            显示记录详细信息






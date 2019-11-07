#!/usr/bin/env python3
# coding:utf-8

from django.utils.safestring import mark_safe


class PageInfo:
    def __init__(self, curpage, allpage, peritem=7):
        self.Curpage = curpage
        self.Allpage = allpage
        self.Peritem = peritem

    @property
    def start(self):
        return (self.Curpage - 1) * self.Peritem

    @property
    def end(self):
        return self.Curpage * self.Peritem

    @property
    def all_page(self):
        temp = divmod(self.Allpage, self.Peritem)
        if temp[1] == 0:
            all_page_count = temp[0]       
        else:
            all_page_count = temp[0] + 1
        return all_page_count


def Pager(page, all_page_count):
    # page当前页面
    # all_page_count总页数
    page_html = []
    first_page = "<a name='page_info_add' href='javascript:void(0)'>首页</a>"
    page_html.append(first_page)
    if page <= 1:
        last_page = "<a name='page_info_add' href='javascript:void(0)'>上一页</a>"
    else:
        last_page = "<a name='page_info_add' href='javascript:void(0)'>上一页</a>"
  
    page_html.append(last_page)
    if all_page_count < 5:  # 让页面显示11页。前后显示5页
        begin = 0
        end = all_page_count
    else:
        if page < 6:
            begin = 0 
            end = 11
        else:
            if page + 6 > all_page_count:
                begin = page - 6
                end = all_page_count
            else:
                begin = page - 6
                end = page + 5
                        
    for i in range(begin, end):
        if page == i+1:
            cur_html = "<a name='page_info_add' class='selected' href='javascript:void(0)'>{}</a>".format(i+1, i+1)
        else:
            cur_html = "<a name='page_info_add' href='javascript:void(0)'>{}</a>".format(i+1, i+1)
        page_html.append(cur_html)
    if all_page_count <= page:
        next_page = "<a name='page_info_add' href='javascript:void(0)'>下一页</a>"
    else:
        next_page = "<a name='page_info_add' href='javascript:void(0)'>下一页</a>"

    page_html.append(next_page)
    end_page = "<a name='page_info_add' href='javascript:void(0)'>尾页</a>"
    page_html.append(end_page)
    page_string = mark_safe(''.join(page_html))
    
    return page_string


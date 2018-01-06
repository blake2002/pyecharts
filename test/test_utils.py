# coding=utf-8
from __future__ import unicode_literals

import json
import os
import codecs
from datetime import date
import numpy as np

from nose.tools import eq_
from pyecharts.utils import (
    write_utf8_html_file,
    get_resource_dir,
    json_dumps,
    merge_js_dependencies
)


def test_get_resource_dir():
    path = get_resource_dir('templates')
    expected = os.path.join(os.getcwd(), '..', 'pyecharts', 'templates')
    eq_(path, os.path.abspath(expected))


def test_write_utf8_html_file():
    content = "柱状图数据堆叠示例"
    file_name = 'test.html'
    write_utf8_html_file(file_name, content)
    with codecs.open(file_name, 'r', 'utf-8') as f:
        actual_content = f.read()
        eq_(content, actual_content)


def test_json_encoder():
    """
    Test json encoder.
    :return:
    """
    data = date(2017, 1, 1)
    eq_(json.dumps({'date': '2017-01-01', 'a': '1'}, indent=0),
        json_dumps({'date': data, 'a': '1'}))

    data2 = {'np_list': np.array(['a', 'b', 'c'])}
    data2_e = {'np_list': ['a', 'b', 'c']}
    eq_(json.dumps(data2_e, indent=0), json_dumps(data2))


def test_merge_js_dependencies():
    # PyEchartsConfig.merge_js_dependencies(str1, str2,...)
    eq_(['echarts', 'fujian'],
        merge_js_dependencies('echarts', 'fujian'))

    # PyEchartsConfig.merge_js_dependencies(chart)
    class MockChart(object):
        def __init__(self, js_dependencies):
            self.js_dependencies = js_dependencies

    ch1 = MockChart(['echarts', 'fujian', 'zhengjiang', 'anhui'])
    eq_(
        ['echarts', 'fujian', 'zhengjiang', 'anhui'],
        merge_js_dependencies(ch1)
    )

    # PyEchartsConfig.merge_js_dependencies(chart1, chart2 )
    ch1 = MockChart(['echarts'])
    ch2 = MockChart(['echarts', 'beijing'])
    eq_(
        ['echarts', 'beijing'],
        merge_js_dependencies(ch1, ch2)
    )

    # PyEchartsConfig.merge_js_dependencies(*chart_list)

    mock_page = [ch1, ch2]
    ch1 = MockChart(['echarts'])
    ch2 = MockChart(['echarts', 'beijing'])
    eq_(
        ['echarts', 'beijing'],
        merge_js_dependencies(*mock_page)
    )

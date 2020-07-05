from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from pymongo import MongoClient
from collections import OrderedDict

Builder.load_string('''
<DataTabel>:
    id:main_win
    RecycleView:
        viewclass: 'CustLabel'
        id:tabel_floor
        RecycleGridLayout:
            id:tabel_floor_layout
            cols:5
            default_size:(None,None)
            default_size_hint:(1,None)
            size_hint_y:None
            height:self.minimum_height
            spacing:5
            multiline:True

<CustLabel@Label>
    text_size: root.width, None
    size: self.texture_size
    bolor:(1,1,1,1)
    canvas.before:
        Color:
            rgba:root.color
            Rectangle:
                size:self.size
                pos:self.pos


''')


class DataTabel(BoxLayout):
    def __init__(self, tabel='', **kwargs):
        super().__init__(**kwargs)
        # k=0
        # posts = self.get_Posts()
        posts = tabel
        col_titles = [k for k in posts.keys()]
        rows_len = len(posts[col_titles[0]])
        self.columns = len(col_titles)
        tabel_data = []
        for t in col_titles:
            tabel_data.append({'text': str(t)})
        for r in range(rows_len):
            for t in col_titles:
                tabel_data.append({'text': str(posts[t][r]), 'size_hint_y': None, 'height': 60, 'bcolor': (1, 1, 1, 1),
                                   'multiline': True})
        self.ids.tabel_floor_layout.cols = self.columns
        self.ids.tabel_floor.data = tabel_data

# class DataTabelApp(App):
#    def build(self):
#       return DataTabelWindow()
#
# if __name__ == '__main__':
#   s=DataTabelApp()
#  s.run()

ReloadBehavior
=========

`ReloadBehavior` is a  mixin behavior widget, that adds a reloading animations to a
ScrollView. when the user drags down to get the effect user get notified by
the `on_reload` event.


### Demo Screenshot

<p align="center">
  <img src="https://raw.githubusercontent.com/avour/garden.reloadbehavior/master/Screenshot.png">
</p>


Here is a simple example:

```python
from kivy.garden.reloadbehavior import ReloadBehavior
from kivy.base import runTouchApp

class Reloader(ReloadBehavior, ScrollView):
    
    def on_reload(self):
        # do anythin
        print('Reloading........')

gridlayout = Builder.load_string('''
GridLayout:
    size_hint_y: None
    height: self.minimum_height
    cols: 1
    ''')
    
reloader = Reloader()
reloader.add_widget(grid)
for i in range(20):
    grid.add_widget(Button(size_hint_y=None,
    text=str(i+1), height='46dp'))

(root)
```



[![ReloadBehavior Video demonstrattion](http://img.youtube.com/vi/PUD_RTmpxag/0.jpg)](http://www.youtube.com/watch?v=PUD_RTmpxag "ReloadBehavior Video demonstration")

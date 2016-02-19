from pyvalidator.call_stack.obj_call_node import *


class ObjCallStack(object):
    def __init__(self, obj):
        self.top = ObjCallNode(obj, None)
        self._calls_list = [obj]

    def add(self, obj):
        self.top = ObjCallNode(obj, self.top)
        self._calls_list.append(obj)

    def clone(self):
        call_stack = None
        for idx, obj in enumerate(self._calls_list):
            if idx == 0:
                call_stack = ObjCallStack(obj)
            else:
                call_stack.add(obj)

        return call_stack

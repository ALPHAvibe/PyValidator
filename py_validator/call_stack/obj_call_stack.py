from py_validator.call_stack.obj_call_node import *


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
            call_stack = ObjCallStack(obj) if idx == 0 else call_stack.add(obj)

        return call_stack

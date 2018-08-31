#!/usr/bin/env python
# -*- coding: utf-8 -*-
class MyClass(object):

    class_name = "MyClass"  # 类属性, 三种方法都能调用

    def __init__(self):
        self.instance_name = "instance_name"  # 实例属性, 只能被实例方法调用
        self.class_name = "instance_class_name"

    def get_class_name_instancemethod(self):  # 实例方法, 只能通过实例调用
        # 实例方法可以访问类属性、实例属性
        return MyClass.class_name

    @classmethod
    def get_class_name_classmethod(cls):  # 类方法, 可通过类名.方法名直接调用
        # 类方法可以访问类属性，不能访问实例属性
        return "我是静态方法"

    @staticmethod
    def get_class_name_staticmethod():  # 静态方法, 可通过类名.方法名直接调用
        # 静态方法可以访问类属性，不能访问实例属性
        return "我是静态方法"

    def instance_visit_class_attribute(self):
        # 实例属性与类属性重名时，self.class_name优先访问实例属性
        pass

if __name__ == "__main__":

    MyClass.class_name = "MyClassNew"
    intance_class = MyClass()
    print "class method:", MyClass.get_class_name_classmethod()
    print "static method:", MyClass.get_class_name_staticmethod()

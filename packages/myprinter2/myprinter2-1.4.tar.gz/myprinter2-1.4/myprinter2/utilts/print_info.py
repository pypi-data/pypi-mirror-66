#!/usr/bin/env python3

class Printer():
    # content is a list : ['first line', 'second line', ...]
    def echo(self, content):
        for i in content:
            print(i.rstrip())


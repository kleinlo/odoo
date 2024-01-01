#!/usr/bin/python3
# @Time    : 2022-08-10
# @Author  : Kevin Kong (kfx2007@163.com)

def chunkify_list(items, chunk_size):
    for i in range(0, len(items), chunk_size):
        yield items[i:i+chunk_size]
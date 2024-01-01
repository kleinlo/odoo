# Mommy Base

本模块基于企业版定制，并不一定适配所有三方主题

version: 16.3.2

## 功能列表

## 工具方法

* setup_modifiers: 封装了适用于fields_view_get方法中定制字段属性的方法.

## 获取当前活动记录

```python
self.active_model
self.active_records
```

## 封装统一提示框

```python
return self.show_message("Title","Content")
```

统一确认框

```python
return self.show_confirm_message("Are you sure?","tips...")
```

确认动作会触发上线文对象的\_action_pops_up_confirm方法

## 快速获取单据序列号

```python
self.next_by_code()
```

## 设置字段颜色

如果要显示某个字段的标签颜色，使用color属性：

```python
<field name="demo1" color="red"/>
```

字段标签将以红色显示出来。

## 快速编辑控制

16.0 暂时无法生效
## 快速美化PyQt--QcureUi

---

### QcureUi
- 快速美化PyQt应用
- 项目地址(欢迎star):[https://github.com/Amiee-well/cureUi](https://github.com/Amiee-well/cureUi)

### 使用方法
- pip install QcureUi

- 调用QcureUi.cure.Windows()

- 共有五个参数填写：

  1.第一个参数为QWidget面板类（必填）

  2.第二个参数为托盘名字（必填）

  3.第三个参数为选择美化颜色面板（选填，默认为default）

  现已有参数为：blue，blueDeep，blueGreen，pink四种

  该参数为True时将随机从已有颜色库返回其一

  4.第四个参数为窗口名字（选填，默认为QCureWindow）

  5.第五个参数为窗口图标（选填，默认为空）

### 注意事项
- 注意:托盘图标默认名称为icon.jpg,改变该图标可在运行目录下放置该图片
- 使用示例:
    from cureUi import cure
    app = QApplication(sys.argv)
    win = cure.Windows(Examples(), 'tray name', True, 'program name', 'myicon.ico')
    sys.exit(app.exec_())

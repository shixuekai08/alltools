import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.0
import QtQuick.Controls.Styles 1.4

Item {
    id: mainWindow
    visible: true
    width: 1200
    height: 960


    signal finalPathChanged(string src) //final 变化信号

    property string font_yahei: "MicroSoft Yahei"
    property real labelWidth: 150 //label标签的宽度
    property real labelHeight: 50
    property int level: 0 //当前显示的日志等级

    property real menuItemHeight: 30
    property bool mainIng: releaseUpdateModule.ing || versionIniModule.ing || packageModule.ing || downloadModule.ing

    //菜单栏
    Rectangle {
        id: menubarRectangle
        color: "#e8e8e8"
        width: mainWindow.width
        height: 40
        anchors.left: mainWindow.left
        anchors.top: mainWindow.top
        border.width: 1
        border.color: "#9f9f9f"

        Row {
            id: menubarRow
            x: 1
            y: 1
            width: menubarRectangle.width - 30
            height: menubarRectangle.height - menubarRectangle.border.width*2

            Rectangle {
                id: configRectangle
                height: menubarRow.height
                width: configText.width + 30
                color: configPopup.visible?"#3875d6": menubarRectangle.color

                Text {
                    id: configText
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.pixelSize: 14
                    font.family: font_yahei
                    renderType: Text.NativeRendering
                    text: qsTr("设置")
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color: configPopup.visible?"#ffffff": "#000000"
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {
                        configPopup.x = configText.x + menubarRectangle.x
                        configPopup.open()
                    }
                }
            }

            Rectangle {
                id: helpRectangle
                height: menubarRow.height
                width: helpText.width + 30
                color: helpPopup.visible?"#3875d6": menubarRectangle.color

                Text {
                    id: helpText
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    font.pixelSize: 14
                    font.family: font_yahei
                    renderType: Text.NativeRendering
                    text: qsTr("帮助")
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color: helpPopup.visible?"#ffffff": "#000000"
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: {

                        helpPopup.x = helpText.x + menubarRectangle.x
                        helpPopup.open()
                    }
                }
            }
        }
    }

    //设置菜单
    Popup {
        id: configPopup
        width: 180
        height: 136
        margins: 0
        padding: 0
        y: menubarRectangle.y + menubarRectangle.height

        Rectangle {
            id: configItem
            width: configPopup.width
            height: configPopup.height
            color: "#e8e8e8"

            Column {
                Rectangle {
                    id: confg1Rectangle
                    width: configItem.width
                    height: menuItemHeight
                    color: "#e8e8e8"

                    Text {
                        id: config1Text
                        anchors.left: parent.left
                        anchors.leftMargin: 24
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        font.family: font_yahei
                        renderType: Text.NativeRendering
                        text: "重新加载config.json"
                        color: "#000000"
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onExited: {
                            confg1Rectangle.color = "#e8e8e8"
                            config1Text.color = "#000000"
                        }

                        onEntered: {
                            confg1Rectangle.color = "#3875d6"
                            config1Text.color = "#ffffff"
                        }

                        onClicked: {
                            configPopup.close()

                            if (mainIng){
                                warnDialog.open()
                                return
                            }

                            configFileDialog.open()
                        }
                    }
                }

                Rectangle {
                    width: configItem.width
                    height: 1
                    color: "#cdcdcd"
                }

                Rectangle {
                    id: confg2Rectangle
                    width: configItem.width
                    height: menuItemHeight
                    color: "#e8e8e8"

                    Text {
                        id: config2Text
                        anchors.left: parent.left
                        anchors.leftMargin: 24
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        font.family: font_yahei
                        renderType: Text.NativeRendering
                        text: "配置文件说明"
                        color: "#000000"
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onExited: {
                            confg2Rectangle.color = "#e8e8e8"
                            config2Text.color = "#000000"
                        }

                        onEntered: {
                            confg2Rectangle.color = "#3875d6"
                            config2Text.color = "#ffffff"
                        }

                        onClicked: {
                            configPopup.close()

                            configExplainDialog.open()
                        }
                    }
                }

                Rectangle {
                    width: configItem.width
                    height: 1
                    color: "#cdcdcd"
                }

                Rectangle {
                    id: confg3Rectangle
                    width: configItem.width
                    height: menuItemHeight
                    color: "#e8e8e8"

                    Text {
                        id: config3Text
                        anchors.left: parent.left
                        anchors.leftMargin: 24
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        font.family: font_yahei
                        renderType: Text.NativeRendering
                        text: "重新加载version.json"
                        color: "#000000"
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onExited: {
                            confg3Rectangle.color = "#e8e8e8"
                            config3Text.color = "#000000"
                        }

                        onEntered: {
                            confg3Rectangle.color = "#3875d6"
                            config3Text.color = "#ffffff"
                        }

                        onClicked: {
                            configPopup.close()

                            if (mainIng){
                                warnDialog.open()
                                return
                            }

                            versionFileDialog.open()
                        }
                    }
                }

                Rectangle {
                    width: configItem.width
                    height: 1
                    color: "#cdcdcd"
                }

            }
        }
    }

    //帮助菜单
    Popup {
        id: helpPopup
        width: 180
        height: 136
        margins: 0
        padding: 0
        y: menubarRectangle.y + menubarRectangle.height

        Rectangle {
            id: helpItem
            width: helpPopup.width
            height: helpPopup.height
            color: "#e8e8e8"

            Column {
                Rectangle {
                    id: help1Rectangle
                    width: helpItem.width
                    height: menuItemHeight
                    color: "#e8e8e8"

                    Text {
                        id: help1Text
                        anchors.left: parent.left
                        anchors.leftMargin: 24
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        font.family: font_yahei
                        renderType: Text.NativeRendering
                        text: "关于 ..."
                        color: "#000000"
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onExited: {
                            help1Rectangle.color = "#e8e8e8"
                            help1Text.color = "#000000"
                        }

                        onEntered: {
                            help1Rectangle.color = "#3875d6"
                            help1Text.color = "#ffffff"
                        }

                        onClicked: {
                            helpPopup.close()
                            aboutDialog.open()
                        }
                    }
                }

                Rectangle {
                    width: configItem.width
                    height: 1
                    color: "#cdcdcd"
                }

                Rectangle {
                    id: help2Rectangle
                    width: helpItem.width
                    height: menuItemHeight
                    color: "#e8e8e8"

                    Text {
                        id: help2Text
                        anchors.left: parent.left
                        anchors.leftMargin: 24
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        font.family: font_yahei
                        renderType: Text.NativeRendering
                        text: "版本信息"
                        color: "#000000"
                    }

                    MouseArea {
                        anchors.fill: parent
                        hoverEnabled: true
                        onExited: {
                            help2Rectangle.color = "#e8e8e8"
                            help2Text.color = "#000000"
                        }

                        onEntered: {
                            help2Rectangle.color = "#3875d6"
                            help2Text.color = "#ffffff"
                        }

                        onClicked: {
                            helpPopup.close()
                            nameAbstractDialog.open()
                        }
                    }
                }

                Rectangle {
                    width: configItem.width
                    height: 1
                    color: "#cdcdcd"
                }

            }
        }
    }

    //config.json选择对话框
    FileDialog {
        id: configFileDialog
        title: "请选择配置文件"
        nameFilters: ["json文件 (*.json)"]

        onAccepted: {
            var jsonPath = configFileDialog.fileUrl.toString()
            var name = jsonPath.substring(8, jsonPath.length)
            _log.print("info", "reload josn from "+name)
            _config_parser.load(name)

        }

        onRejected: {
            console.log("Canceled")
        }
    }

    //version.json选择对话框
    FileDialog {
        id: versionFileDialog
        title: "请选择配置文件"
        nameFilters: ["json文件 (*.json)"]

        onAccepted: {
            var jsonPath = versionFileDialog.fileUrl.toString()
            var name = jsonPath.substring(8, jsonPath.length)
            _log.print("info", "reload josn from "+name)
            _version_manager.load(name)

        }

        onRejected: {
            console.log("Canceled")
        }
    }


    //左边栏
    LeftSideBar {
        id: leftSideBar
        anchors.top: menubarRectangle.bottom
        anchors.left: mainWindow.left
        anchors.bottom: mainWindow.bottom
    }



    //发布更新模块
    ReleaseUpdateModule {
        id: releaseUpdateModule
        anchors.left: leftSideBar.right
        anchors.leftMargin: 5
        anchors.right: mainWindow.right
        anchors.rightMargin: 5
        anchors.top: menubarRectangle.bottom
        anchors.topMargin: 10
        visible: leftSideBar.selectedBar == 0

    }


    //生成version.ini模块
    VersionIniModule {
        id: versionIniModule
        anchors.left: leftSideBar.right
        anchors.leftMargin: 5
        anchors.right: mainWindow.right
        anchors.rightMargin: 5
        anchors.top: menubarRectangle.bottom
        anchors.topMargin: 10
        visible: leftSideBar.selectedBar == 1
    }


    //安装包
    PackageModule{
        id: packageModule
        anchors.left: leftSideBar.right
        anchors.leftMargin: 5
        anchors.right: mainWindow.right
        anchors.rightMargin: 5
        anchors.top: menubarRectangle.bottom
        anchors.topMargin: 10
        visible: leftSideBar.selectedBar == 2


    }

    //下载
    DownloadModule {
        id: downloadModule
        anchors.left: leftSideBar.right
        anchors.leftMargin: 5
        anchors.right: mainWindow.right
        anchors.rightMargin: 5
        anchors.top: menubarRectangle.bottom
        anchors.topMargin: 10
        visible: leftSideBar.selectedBar == 3
    }

    UpdateRateModule {
        id: updateRateModule
        anchors.left: leftSideBar.right
        anchors.leftMargin: 5
        anchors.right: mainWindow.right
        anchors.rightMargin: 5
        anchors.top: menubarRectangle.bottom
        anchors.topMargin: 10
        visible: leftSideBar.selectedBar == 4
    }

    //日志
    Item {
        id: logger
        anchors.left: leftSideBar.right
        anchors.right: mainWindow.right
        anchors.top: {
            if (leftSideBar.selectedBar == 0)
                return releaseUpdateModule.bottom
            else if (leftSideBar.selectedBar == 1)
                return versionIniModule.bottom
            else if (leftSideBar.selectedBar == 2)
                return packageModule.bottom
            else if (leftSideBar.selectedBar == 3)
                return downloadModule.bottom
            else if (leftSideBar.selectedBar == 4)
                return updateRateModule.bottom
        }
        anchors.topMargin: 10
        anchors.bottom: mainWindow.bottom
        clip: true

        property int selectedIndex: 0


        ScrollView {
            id: infoScrollView
            width: logger.width
            height: logger.height - bottomButton.height
            anchors.top: logger.top
            clip: true

            ScrollBar.horizontal.policy: ScrollBar.AsNeeded
            ScrollBar.vertical.policy: ScrollBar.AsNeeded

            TextArea {
                id: infoTextArea
                readOnly: true
                renderType: Text.NativeRendering
                font.family: font_yahei
                font.pixelSize: 12
                selectByMouse: true

                background: Rectangle{
                    color: "#eeeeee"
                }
            }

            visible: level == 0
        }

        ScrollView {
            id: warnScrollView
            anchors.fill: infoScrollView
            clip: true

            ScrollBar.horizontal.policy: ScrollBar.AsNeeded
            ScrollBar.vertical: ScrollBar {
                id: warnvbar
                hoverEnabled: true
                active: hovered || pressed
                orientation: Qt.Vertical
                size: warnScrollView.height / warnTextArea.height
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                onSizeChanged: warnvbar.position = 1- warnvbar.size
            }

            TextArea {
                id: warnTextArea
                readOnly: true
                renderType: Text.NativeRendering
                font.family: font_yahei
                font.pixelSize: 12
                selectByMouse: true


                background: Rectangle{
                    color: "#eeeeee"
                }
            }

            visible: level == 1
        }

        ScrollView {
            id: errorScrollView
            anchors.fill: infoScrollView
            clip: true

            ScrollBar.horizontal.policy: ScrollBar.AsNeeded
            ScrollBar.vertical: ScrollBar {
                id: errorvbar
                hoverEnabled: true
                active: hovered || pressed
                orientation: Qt.Vertical
                size: errorScrollView.height / errorTextArea.height
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                onSizeChanged: errorvbar.position = 1- errorvbar.size
            }

            TextArea {
                id: errorTextArea
                readOnly: true
                renderType: Text.NativeRendering
                font.family: font_yahei
                font.pixelSize: 12
                selectByMouse: true


                background: Rectangle{
                    color: "#eeeeee"
                }
            }

            visible: level == 2
        }


        Rectangle {
            id: bottomButton
            width: logger.width
            height: 30
            anchors.bottom: logger.bottom
            color: "#ff7700"

            Row {
                id: topRow
                spacing: 1

                //info
                Rectangle {
                    id: infoRectangle
                    width: infoText.width + 10
                    height: bottomButton.height
                    color: {
                        if (logger.selectedIndex==0)
                            return"#ffffff"
                        else if (infoMouseArea.containsMouse)
                            return "#ff5300"
                        else
                            return "#ff7700"
                    }
                    clip: true

                    Text {
                        id: infoText
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        color: logger.selectedIndex==0?"#000000":"#ffffff"
                        font.bold: true
                        renderType: Text.NativeRendering
                        font.family: font_yahei
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        text: qsTr("INFO")
                    }

                    MouseArea {
                        id: infoMouseArea
                        anchors.fill: parent
                        hoverEnabled: true

                        onClicked: {
                            level = 0
                            logger.selectedIndex = 0
                        }
                    }
                }

                //warning
                Rectangle {
                    id: warnRectangle
                    width: warnText.width + 10
                    height: bottomButton.height
                    color: {
                        if (logger.selectedIndex==1)
                            return"#ffffff"
                        else if (warnMouseArea.containsMouse)
                            return "#ff5300"
                        else
                            return "#ff7700"
                    }
                    clip: true

                    Text {
                        id: warnText
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        color: logger.selectedIndex==1?"#000000":"#ffffff"
                        font.bold: true
                        renderType: Text.NativeRendering
                        font.family: font_yahei
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        text: qsTr("WARNING")
                    }

                    MouseArea {
                        id: warnMouseArea
                        anchors.fill: parent
                        hoverEnabled: true

                        onClicked: {
                            level = 1
                            logger.selectedIndex = 1
                        }
                    }
                }

                //error
                Rectangle {
                    id: errorRectangle
                    width: errorText.width + 10
                    height: bottomButton.height
                    color: {
                        if (logger.selectedIndex==2)
                            return"#ffffff"
                        else if (errorMouseArea.containsMouse)
                            return "#ff5300"
                        else
                            return "#ff7700"
                    }
                    clip: true

                    Text {
                        id: errorText
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        font.bold: true
                        color: logger.selectedIndex==2?"#000000":"#ffffff"
                        renderType: Text.NativeRendering
                        font.family: font_yahei
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        text: qsTr("ERROR")
                    }

                    MouseArea {
                        id: errorMouseArea
                        anchors.fill: parent
                        hoverEnabled: true

                        onClicked: {
                            level = 2
                            logger.selectedIndex = 2
                        }
                    }
                }

                //清空
                Rectangle {
                    id: clearRectangle
                    width: clearText.width + 10
                    height: bottomButton.height
                    color: {
                        if (logger.selectedIndex==3)
                            return"#ffffff"
                        else if (clearMouseArea.containsMouse)
                            return "#ff5300"
                        else
                            return "#ff7700"
                    }
                    clip: true

                    Text {
                        id: clearText
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        font.pixelSize: 14
                        font.bold: true
                        color: logger.selectedIndex==3?"#000000":"#ffffff"
                        renderType: Text.NativeRendering
                        font.family: font_yahei
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        text: qsTr("清空")
                    }

                    MouseArea {
                        id: clearMouseArea
                        anchors.fill: parent
                        hoverEnabled: true

                        onClicked: {
                            infoTextArea.text = ""
                            warnTextArea.text = ""
                            errorTextArea.text = ""
                            logger.selectedIndex = 3
                        }
                    }
                }

            }

        }
    }

    //反馈提醒
    FeedbackDialog {
        id: warnDialog
        x: (mainWindow.width - warnDialog.width)/2
        y: (mainWindow.height - warnDialog.height)/2
    }

    //关于
    AboutDialog {
        id: aboutDialog
        x: (mainWindow.width - aboutDialog.width)/2
        y: (mainWindow.height - aboutDialog.height)/2
    }

    //config.json各字段说明对话框
    ConfigExplainDialog {
        id: configExplainDialog
        x: (mainWindow.width - configExplainDialog.width)/2
        y: (mainWindow.height - configExplainDialog.height)/2
    }

    //
    NameAbstractDialog {
        id: nameAbstractDialog
        x: (mainWindow.width - nameAbstractDialog.width)/2
        y: (mainWindow.height - nameAbstractDialog.height)/2
    }

    //_log
    Connections {
        target: _log

        onInfoChanged: {
            var now = new Date()
            infoTextArea.append("[ "+now.toLocaleTimeString()+" INFO] " +msg)
        }

        onWarningChanged: {
            var now = new Date()
            infoTextArea.append("[ "+now.toLocaleTimeString()+" WARNNING] " +msg)
            warnTextArea.append("[ "+now.toLocaleTimeString()+" WARNNING] " +msg)
        }

        onErrorChanged: {
            var now = new Date()
            infoTextArea.append("[ "+now.toLocaleTimeString()+" ERROR] " +msg)
            warnTextArea.append("[ "+now.toLocaleTimeString()+" ERROR] " +msg)
            errorTextArea.append("[ "+now.toLocaleTimeString()+" ERROR] " +msg)
        }

    }

    //_template_parser
    Connections {
        target: _template_parser

        onUrlChanged: {
            urlPrefix = url
        }

        onAppCodeChanged: {
            appCode = code
        }

        onZdbFileChanged: {
            zdbFile = file
        }

        onSrcPathChanged: {
            srcPath = path
        }

        onDestPathChanged: {
            destPath = path
        }

        onFinalPathChanged: {
            finalPath = path
        }

    }

    //_config_manager
    Connections {
        target: _config_manager

        onLastVersionChanged: {
            lastVersionTextInput.text = version
            lastVersion = version
        }

        onFinalPathChanged: {
            finalPath = path
        }
    }


    //_main_window
    Connections {
        target: _main_window

        onWidthChanged: {
            mainWindow.width = arg
        }

        onHeightChanged: {
            mainWindow.height = arg
        }
    }


}

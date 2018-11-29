import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.0

Item {
    id: urm
    width: 800
    height: 790
    clip: true

    property real urmLabelWidth: 150 //label标签的宽度
    property real urmLabelHeight: 50
    property real urmCellWidth: 100
    property bool ing: true
    property string filePath: ""


    //更新率数据表格文件路径
    Rectangle {
        id: filePathRectangle
        width: urmLabelWidth
        height: urmLabelHeight
        anchors.top: parent.top
        anchors.left: parent.left
        color: "#eeeeee"

        Text {
            id: filePathText
            anchors.fill: parent
            font.pixelSize: 14
            renderType: Text.NativeRendering
            font.family: font_yahei
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("更新率报表路径：")
        }
    }

    TextField {
        id: filePathTextInput
        height: urmLabelHeight
        anchors.verticalCenter: filePathRectangle.verticalCenter
        anchors.left: filePathRectangle.right
        anchors.leftMargin: 2
        anchors.right: fileButton.left
        anchors.rightMargin: 2
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        placeholderText: qsTr("请输xlsx文件路径")
        text: filePath
        readOnly: true
    }

    //更新率数据表格文件路径选择按钮
    Rectangle {
        id: fileButton
        width: 40
        height: 50
        anchors.right: parent.right
        anchors.verticalCenter: filePathRectangle.verticalCenter
        color: "#eeeeee"

        Text {
            id: fileText
            anchors.fill: parent
            font.pixelSize: 14
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("...")
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onClicked: {
                fileFileDialog.open()
            }
        }
    }

    FileDialog {
          id: fileFileDialog
          title: "请选择版本所在的文件夹"
          nameFilters: ["xlsx文件 (*.xlsx)"]

          onAccepted: {
              var urlPath = fileFileDialog.fileUrl.toString()
              filePath = urlPath.substring(8, urlPath.length)
              _log.print("info", "file path switchs to "+filePath)
              _update_rater.reload(filePath)
          }

          onRejected: {
              console.log("Canceled")
          }
      }


    //日期条件选择
    Rectangle {
        id: dateRectangle
        width: urmLabelWidth
        height: urmLabelHeight
        anchors.top: filePathRectangle.bottom
        anchors.topMargin: 10
        anchors.left: parent.left
        color: "#eeeeee"

        Text {
            anchors.fill: parent
            font.pixelSize: 14
            renderType: Text.NativeRendering
            font.family: font_yahei
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("日期选择：")
        }
    }


    CustomComboBox {
        id: dateFromComboBox
        height: urmLabelHeight
        width: urmLabelWidth
        anchors.verticalCenter: dateRectangle.verticalCenter
        anchors.left: dateRectangle.right
        anchors.leftMargin: 2
        currentIndex: 0
        model: ["All"]

        onClicked: _update_rater.adjustStartDate(dateFromComboBox.currentIndex)
    }

    Text {
        id: dateText
        width: 20
        height: urmLabelHeight
        anchors.verticalCenter: dateRectangle.verticalCenter
        anchors.left: dateFromComboBox.right
        anchors.leftMargin: 2
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        text: qsTr("~")
    }

    CustomComboBox {
        id: dateToComboBox
        height: urmLabelHeight
        width: urmLabelWidth
        anchors.verticalCenter: dateRectangle.verticalCenter
        anchors.left: dateText.right
        anchors.leftMargin: 2
        currentIndex: 0
        model: ["All"]

        onClicked: _update_rater.adjustEndDate(dateToComboBox.count - 1 - dateToComboBox.currentIndex)
    }


    //版本号选择
    Rectangle {
        id: startVersionRectangle
        width: urmLabelWidth
        height: urmLabelHeight
        anchors.verticalCenter: dateRectangle.verticalCenter
        anchors.left: dateToComboBox.right
        anchors.leftMargin: 20
        color: "#eeeeee"

        Text {
            anchors.fill: parent
            font.pixelSize: 14
            renderType: Text.NativeRendering
            font.family: font_yahei
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("版本选择:")
        }
    }

    CustomComboBox {
        id: startVersionComboBox
        height: urmLabelHeight
        width: urmLabelWidth
        anchors.verticalCenter: dateRectangle.verticalCenter
        anchors.left: startVersionRectangle.right
        anchors.leftMargin: 2
        currentIndex: 0
        model: ["All"]
    }

    Text {
        id: fromtoText
        width: 20
        height: urmLabelHeight
        anchors.verticalCenter: dateRectangle.verticalCenter
        anchors.left: startVersionComboBox.right
        anchors.leftMargin: 2
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        text: qsTr("=>")
    }

    CustomComboBox {
        id: endVersionComboBox
        height: urmLabelHeight
        width: urmLabelWidth
        anchors.verticalCenter: dateRectangle.verticalCenter
        anchors.left: fromtoText.right
        anchors.leftMargin: 2
        font.family: font_yahei
        font.pixelSize: 12
        currentIndex: 0
        model: ["All"]
    }


    //表格一的统计结果
    Text {
        id: sheetText_1
        width: urm.width
        height: 25
        anchors.top: dateRectangle.bottom
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 18
        color: "#000000"
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: qsTr("----------------------------------表格一的统计结果----------------------------------")
        clip: true
    }

    //启动总UV、PV
    ListView {
        id: totalLauncher
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: sheetText_1.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal

        model: listModel

        delegate: component
    }

    //显示启动统计
    ListView {
        id: explicitLauncher
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: totalLauncher.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal
        model: listModel

        delegate: component
    }

    //隐式启动统计
    ListView {
        id: implicitLauncher
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: explicitLauncher.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal
        model: listModel

        delegate: component
    }


    Component {
        id: component

        Item {
            id: componentItem
            width: componentRectangle.width + 2 + componentTextInput.width
            height: urmLabelHeight
            clip: true

            Rectangle {
                id: componentRectangle
                width: urmLabelWidth
                height: componentItem.height
                anchors.left: parent.left
                anchors.top: parent.top
                color: "#eeeeee"
                clip: true

                Text {
                    anchors.fill: parent
                    font.pixelSize: 14
                    font.family: font_yahei
                    renderType: Text.NativeRendering
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    text: modelData["_name"]
                    elide: Text.ElideRight
                }

                MouseArea {
                    id: componentMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                }

                ToolTip.visible: componentMouseArea.containsMouse
                ToolTip.text: modelData["_name"]

            }

            TextField {
                id: componentTextInput
                width: 100
                height: componentItem.height
                anchors.verticalCenter: componentRectangle.verticalCenter
                anchors.left: componentRectangle.right
                anchors.leftMargin: 2
                cursorVisible: false
                font.pixelSize: 14
                renderType: Text.NativeRendering
                font.family: font_yahei
                selectByMouse: true
                readOnly: true
                text: modelData["_value"]
            }
        }
    }

    ListModel {
        id: listModel

        ListElement {
            _name: "启动总UV"
            _value: "100"
        }

        ListElement {
            _name: "启动总PV"
            _value: "100"
        }
    }


    //表格二的统计结果
    Text {
        id: sheetText_2
        width: urm.width
        height: 25
        anchors.top: implicitLauncher.bottom
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 18
        color: "#000000"
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: qsTr("----------------------------------表格二的统计结果----------------------------------")
        clip: true
    }


    //下载总UV、PV
    ListView {
        id: totalDownload
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: sheetText_2.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal
        model: listModel

        delegate: component
    }

    //显示更新成功统计
    ListView {
        id: explicitDownload
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: totalDownload.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal
        model: listModel

        delegate: component
    }

    //隐式更新下载统计
    ListView {
        id: implicitDownload
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: explicitDownload.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal
        model: listModel

        delegate: component
    }


    //表格三的统计结果
    Text {
        id: sheetText_3
        width: urm.width
        height: 25
        anchors.top: implicitDownload.bottom
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 18
        color: "#000000"
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: qsTr("----------------------------------表格三的统计结果----------------------------------")
        clip: true
    }


    //隐式更新成功总UV、PV
    ListView {
        id: implicitCopy
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: sheetText_3.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal
        model: listModel

        delegate: component
    }

    //更新率统计结果
    Text {
        id: sheetText_4
        width: urm.width
        height: 25
        anchors.top: implicitCopy.bottom
        anchors.topMargin: 10
        anchors.horizontalCenter: parent.horizontalCenter
        font.pixelSize: 18
        color: "#000000"
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: qsTr("----------------------------------更新率的统计结果----------------------------------")
        clip: true
    }

    //更新率统计
    ListView {
        id: rate
        height: urmLabelHeight
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: sheetText_4.bottom
        anchors.topMargin: 10
        spacing: 10
        orientation: ListView.Horizontal
        model: listModel

        delegate: component
    }


    //一键统计
    Rectangle {
        id: runRectangle
        width: urmLabelWidth
        height: urmLabelHeight
        anchors.left: rate.left
        anchors.top: rate.bottom
        anchors.topMargin: 10
        color: "#aaafba"
        radius: 4
        enabled: false

        Text {
            id: runText
            anchors.fill: parent
            font.pixelSize: 18
            font.bold: true
            color: "#ffffff"
            renderType: Text.NativeRendering
            font.family: font_yahei
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("开始统计")
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onEntered: {
                if (!ing)
                    runRectangle.color = "#ff5d23"
            }
            onExited: {
                if (!ing)
                    runRectangle.color = "#ff7700"
            }

            onClicked: {
                _update_rater.censusByCondition(startVersionComboBox.currentIndex, endVersionComboBox.currentIndex)
            }
        }
    }

    //进度条
    Rectangle {
        id: pbgRectangle
        height: urmLabelHeight - 30
        anchors.left: runRectangle.right
        anchors.leftMargin: 10
        anchors.right: parent.right
        anchors.verticalCenter: runRectangle.verticalCenter
        color: "#eeeeee"
        radius: height/2

        property real value: 0.0

        Rectangle {
            id: pbRectangle
            width: 0
            height: pbgRectangle.height
            anchors.left: pbgRectangle.left
            color: "#8ad16e"
            radius: height/2

            PropertyAnimation {
                id: animation;
                loops: 1
                running: false
                target: pbRectangle
                property: "width"
                duration: 2000
            }
        }


    }

    function speed(percent){
        if (percent >= 0 && percent <= 1){
            pbgRectangle.value = percent
            if (animation.running){
                animation.stop()
            }
            animation.from = pbRectangle.width
            animation.to = pbgRectangle.width * pbgRectangle.value
            animation.start()
        }
        else{
            pbgRectangle.value = 0
            pbRectangle.width = 0
        }
    }

    //_update_rater
    Connections {
        target: _update_rater

        onTotalLauncherChanged: {
            totalLauncher.model = tlmodel
        }

        onExplicitLauncherChanged: {
            explicitLauncher.model = elmodel
        }

        onImplicitLauncherChanged: {
            implicitLauncher.model = ilmodel
        }

        onTotalDownloadChanged: {
            totalDownload.model = tdmodel
        }

        onExplicitDownloadChanged: {
            explicitDownload.model = edmodel
        }

        onImplicitDownloadChanged: {
            implicitDownload.model = idmodel
        }

        onImplicitCopyChanged: {
            implicitCopy.model = icmodel
        }

        onRateChanged: {
            rate.model = rmodel
        }

        onStartDateListChanged: {
            dateFromComboBox.model = sdlmodel
            dateFromComboBox.currentIndex = focusindex
        }

        onEndDateListChanged: {
            dateToComboBox.model = edlmodel
            dateToComboBox.currentIndex = dateToComboBox.count - focusindex - 1
        }

        onStartVersionListChanged: {
            startVersionComboBox.model = svlmodel
        }

        onEndVersionListChanged: {
            endVersionComboBox.model = evlmodel
        }

        onProgressChanged: {
            speed(percent)
        }

        onFeedback: {
            ing = enable
            if (ing){
                runRectangle.color = "#aaafba"
                runRectangle.enabled = false
                fileButton.enabled = false
            }
            else{
                runRectangle.color = "#ff7700"
                runRectangle.enabled = true
                fileButton.enabled = true
            }
        }

    }
}

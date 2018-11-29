import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.0

Item {
    id: pm
    width: 800
    height: 290

    property real pmLabelWidth: 150 //label标签的宽度
    property real pmLabelHeight: 50
    property alias pmFinalPath: copyTextInput.text
    property alias pmDestPath: pasteTextField.text
    property bool ing: false


    //复制源
    Rectangle {
        id: copyRectangle
        width: pmLabelWidth
        height: pmLabelHeight
        anchors.top: parent.top
        anchors.left: parent.left
        color: "#eeeeee"

        Text {
            id: copyVersionText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("复制：")
        }
    }

    TextField {
        id: copyTextInput
        height: pmLabelHeight
        anchors.verticalCenter: copyRectangle.verticalCenter
        anchors.left: copyRectangle.right
        anchors.leftMargin: 2
        anchors.right: parent.right
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        selectByMouse: true
        validator: IntValidator{bottom: 0; top: 999999999;}
    }


    //粘贴
    Rectangle {
        id: pasteRectangle
        width: pmLabelWidth
        height: pmLabelHeight
        anchors.left: copyRectangle.left
        anchors.top: copyRectangle.bottom
        anchors.topMargin: 10
        color: "#eeeeee"

        Text {
            id: pasteText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("粘贴：")
        }
    }

    //粘贴文件夹
    TextField {
        id: pasteTextField
        height: pmLabelHeight
        anchors.verticalCenter: pasteRectangle.verticalCenter
        anchors.left: pasteRectangle.right
        anchors.leftMargin: 2
        anchors.right: parent.right
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: ""
        readOnly: true
        selectByMouse: true
    }


    CustomComboBox {
        id: signCustomComboBox
        height: pmLabelHeight
        width: pmLabelWidth
        anchors.left: pasteRectangle.left
        anchors.top: pasteRectangle.bottom
        anchors.topMargin: 10
        currentIndex: 0
        model: ["校验签名", "不校验签名"]
    }

    //打包
    Rectangle {
        id: runRectangle
        width: pmLabelWidth
        height: pmLabelHeight
        anchors.left: signCustomComboBox.right
        anchors.leftMargin: 10
        anchors.verticalCenter: signCustomComboBox.verticalCenter
        color: "#ff7700"
        radius: 4

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
            text: qsTr("一键打包")
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
                _install_packager.packing(pmFinalPath, pmDestPath, signCustomComboBox.currentIndex==0)
            }
        }
    }

    //进度条
    Rectangle {
        id: pbgRectangle
        height: pmLabelHeight - 30
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

    //_config_manager
    Connections {
        target: _config_manager

        onFinalPathChanged: {
            pmFinalPath = path
        }
    }

    //_template_parser
    Connections {
        target: _template_parser

        onFinalPathChanged: {
            pmFinalPath = path
        }

        onPackagePathChanged: {
            pmDestPath = path
        }
    }

    //_install_packager
    Connections {
        target: _install_packager

        onProgressChanged: {
            speed(percent)
        }

        onFeedback: {
            ing = enable
            if (ing){
                runRectangle.color = "#aaafba"
                runRectangle.enabled = false
            }
            else{
                runRectangle.color = "#ff7700"
                runRectangle.enabled = true
            }
        }
    }

}

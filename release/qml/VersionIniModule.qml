import QtQuick 2.7
import QtQuick.Controls 2.3

Item {
    id: vim
    width: 800
    height: 400

    property real vimLabelWidth: 150 //label标签的宽度
    property real vimLabelHeight: 50
    property bool ing: false

    //预发版本号
    Rectangle {
        id: versionRectangle
        width: vimLabelWidth
        height: vimLabelHeight
        anchors.left: parent.left
        anchors.top: parent.top
        color: "#eeeeee"

        Text {
            id: versionText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("预发版本号：")
        }
    }

    TextField {
        id: versionTextInput
        width: 200
        height: vimLabelHeight
        anchors.verticalCenter: versionRectangle.verticalCenter
        anchors.left: versionRectangle.right
        anchors.leftMargin: 2
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        placeholderText: qsTr("请输入9位版本号")
        validator: IntValidator{bottom: 0; top: 999999999;}
        selectByMouse: true
        text: {
            var now = new Date
            return now.toLocaleDateString(Qt.locale("de_DE"), "yyyyMMdd")+"0"
        }
    }


    //预发版本名称
    Rectangle {
        id: vnameRectangle
        width: vimLabelWidth
        height: vimLabelHeight
        anchors.left: versionTextInput.right
        anchors.leftMargin: 10
        anchors.verticalCenter: versionTextInput.verticalCenter
        color: "#eeeeee"

        Text {
            id: vnameText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("预发版本名称：")
        }
    }

    TextField {
        id: vnameTextInput
        width: 200
        height: vimLabelHeight
        anchors.verticalCenter: vnameRectangle.verticalCenter
        anchors.left: vnameRectangle.right
        anchors.leftMargin: 2
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        placeholderText: qsTr("请输入版本名称")
        text: "V6.1.7"
        selectByMouse: true
    }


    //隐式更新最小版本号
    Rectangle {
        id: minVersionRectangle
        width: vimLabelWidth
        height: vimLabelHeight
        anchors.left: parent.left
        anchors.top: versionRectangle.bottom
        anchors.topMargin: 10
        color: "#eeeeee"

        Text {
            id: minVersionText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("隐式更新最小版本号：")
        }
    }

    TextField {
        id: minVersionTextInput
        width: 200
        height: vimLabelHeight
        anchors.verticalCenter: minVersionRectangle.verticalCenter
        anchors.left: minVersionRectangle.right
        anchors.leftMargin: 2
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        placeholderText: qsTr("请输入9位版本号")
        validator: IntValidator{bottom: 0; top: 999999999;}
        selectByMouse: true
        text: {
            var now = new Date
            return now.toLocaleDateString(Qt.locale("de_DE"), "yyyyMMdd")+"0"
        }
    }


    //version.ini地址
    Rectangle {
        id: iniRectangle
        width: vimLabelWidth
        height: vimLabelHeight
        anchors.left: minVersionTextInput.right
        anchors.leftMargin: 10
        anchors.verticalCenter: minVersionTextInput.verticalCenter
        color: "#eeeeee"

        Text {
            id: iniText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("version.ini地址：")
        }
    }

    TextField {
        id: iniTextInput
        width: 200
        height: vimLabelHeight
        anchors.verticalCenter: iniRectangle.verticalCenter
        anchors.left: iniRectangle.right
        anchors.leftMargin: 2
        cursorVisible: false
        font.pixelSize: 12
        renderType: Text.NativeRendering
        font.family: font_yahei
        placeholderText: qsTr("请输入版本名称")
        text: "V6.1.7"
        selectByMouse: true
        readOnly: true

    }




    //新版修改信息
    Item {
        id: updateInfoItem
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: minVersionRectangle.bottom
        height: vim.height - 170


        Text {
            id: updateInfoTip
            width: updateInfoItem.width
            height: 40
            text: "本次更新的文案："
            color: "#000000"
            renderType: Text.NativeRendering
            font.family: font_yahei
            font.pixelSize: 12
            horizontalAlignment: Text.AlignLeft
            verticalAlignment: Text.AlignVCenter
        }

        ScrollView {
            id: infoScrollView
            width: updateInfoItem.width
            anchors.top: updateInfoTip.bottom
            anchors.bottom: updateInfoItem.bottom
            clip: true

            ScrollBar.horizontal.policy: ScrollBar.AsNeeded
            ScrollBar.vertical.policy: ScrollBar.AsNeeded

            TextArea {
                id: updateInfoTextArea
                renderType: Text.NativeRendering
                font.family: font_yahei
                font.pixelSize: 12
                selectByMouse: true


                background: Rectangle{
                    color: "#eeeeee"
                }
            }

        }
    }


    //生成version.ini
    Rectangle {
        id: genVersionRectangle
        width: vimLabelWidth
        height: vimLabelHeight
        anchors.left: updateInfoItem.left
        anchors.top: updateInfoItem.bottom
        anchors.topMargin: 10
        color: "#aaafba"
        enabled: false
        radius: 4

        Text {
            anchors.fill: parent
            font.pixelSize: 18
            font.bold: true
            color: "#ffffff"
            renderType: Text.NativeRendering
            font.family: font_yahei
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("生成version.ini")
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onEntered: {
                if (!ing)
                    genVersionRectangle.color = "#ff5d23"
            }
            onExited: {
                if (!ing)
                    genVersionRectangle.color = "#ff7700"
            }

            onClicked: {
                _ini_producer.produce(versionTextInput.text, vnameTextInput.text, minVersionTextInput.text, updateInfoTextArea.text, iniTextInput.text)
            }
        }
    }

    //进度条
    Rectangle {
        id: pbgRectangle
        height: vimLabelHeight - 30
        anchors.left: genVersionRectangle.right
        anchors.leftMargin: 10
        anchors.right: parent.right
        anchors.verticalCenter: genVersionRectangle.verticalCenter
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

    //_ini_producer
    Connections {
        target: _ini_producer

        onProgressChanged: {
            speed(percent)
        }

        onFeedback: {
            ing = enable
            if (ing){
                genVersionRectangle.color = "#aaafba"
                genVersionRectangle.enabled = false
            }
            else{
                genVersionRectangle.color = "#ff7700"
                genVersionRectangle.enabled = true
            }
        }
    }

    //_config_manager
    Connections {
        target: _config_manager

        onFinalPathChanged: {
            iniTextInput.text = path+"/version.ini"
        }

        onMinHideVersionChanged: {
            minVersionTextInput.text = version
        }

        onParseResultChanged: {
            if (enable){
                genVersionRectangle.color = "#ff7700"
                genVersionRectangle.enabled = true
            }
            else
            {
                genVersionRectangle.color = "#aaafba"
                genVersionRectangle.enabled = false
            }
        }
    }

    //_template_parser
    Connections {
        target: _template_parser

        onFinalPathChanged: {
            iniTextInput.text = path+"/version.ini"
        }
    }

}


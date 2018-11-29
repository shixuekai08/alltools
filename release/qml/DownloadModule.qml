import QtQuick 2.7
import QtQuick.Controls 2.3

Item {
    id: dm
    width: 800
    height: 290

    property real dmLabelWidth: 150 //label标签的宽度
    property real dmLabelHeight: 50
    property string dmUrlPrefix: ""
    property string dmAppCode: ""
    property string dmZdbFile: ""
    property alias dmLastVersion: lastVersionTextInput.text
    property bool ing: false

    //上一个发行的版本号
    Rectangle {
        id: lastVersionRectangle
        width: dmLabelWidth
        height: dmLabelHeight
        anchors.top: parent.top
        anchors.left: parent.left
        color: "#eeeeee"

        Text {
            id: lastVersionText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("上一个发行的版本号：")
        }
    }

    TextField {
        id: lastVersionTextInput
        width: 200
        height: dmLabelHeight
        anchors.verticalCenter: lastVersionRectangle.verticalCenter
        anchors.left: lastVersionRectangle.right
        anchors.leftMargin: 2
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        selectByMouse: true
        validator: IntValidator{bottom: 0; top: 999999999;}
    }


    //zdb 标签
    Rectangle {
        id: zdbLabelRectangle
        width: dmLabelWidth
        height: dmLabelHeight
        anchors.left: lastVersionRectangle.left
        anchors.top: lastVersionRectangle.bottom
        anchors.topMargin: 10
        color: "#eeeeee"

        Text {
            id: zdbLabelText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("zdb下载地址：")
        }
    }

    //zdb url
    TextField {
        id: zdbTextInput
        height: dmLabelHeight
        anchors.verticalCenter: zdbLabelRectangle.verticalCenter
        anchors.left: zdbLabelRectangle.right
        anchors.leftMargin: 2
        anchors.right: parent.right
        cursorVisible: false
        font.pixelSize: 10
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: dmUrlPrefix+dmAppCode+"/"+dmLastVersion+"/"+dmZdbFile
        readOnly: true
        selectByMouse: true
    }


    //zdb保存地址 标签
    Rectangle {
        id: storeRectangle
        width: dmLabelWidth
        height: dmLabelHeight
        anchors.left: lastVersionRectangle.left
        anchors.top: zdbLabelRectangle.bottom
        anchors.topMargin: 10
        color: "#eeeeee"

        Text {
            id: storeText
            anchors.fill: parent
            font.pixelSize: 14
            font.family: font_yahei
            renderType: Text.NativeRendering
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("zdb保存地址：")
        }
    }

    //zdb保存地址
    TextField {
        id: storeTextInput
        height: dmLabelHeight
        anchors.verticalCenter: storeRectangle.verticalCenter
        anchors.left: storeRectangle.right
        anchors.leftMargin: 2
        anchors.right: parent.right
        cursorVisible: false
        font.pixelSize: 12
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: ""
        readOnly: true
        selectByMouse: true
    }



    //下载zdb
    Rectangle {
        id: zdbRectangle
        width: dmLabelWidth
        height: dmLabelHeight
        anchors.left: storeRectangle.left
        anchors.top: storeRectangle.bottom
        anchors.topMargin: 10
        color: "#ff7700"
        radius: 4
        property bool beClicked: false

        Text {
            id: zdbText
            anchors.fill: parent
            font.pixelSize: 18
            color: "#ffffff"
            renderType: Text.NativeRendering
            font.family: font_yahei
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("下载zdb")
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onEntered: {
                if (!ing)
                    zdbRectangle.color = "#ff5d23"
            }
            onExited: {
                if (!ing)
                    zdbRectangle.color = "#ff7700"
            }

            onClicked: {
                _downloader.downloadAndUnzip(zdbTextInput.text, storeTextInput.text+"/"+dmZdbFile, storeTextInput.text)
            }
        }
    }

    //进度条
    Rectangle {
        id: dmpbgRectangle
        height: dmLabelHeight - 30
        anchors.left: zdbRectangle.right
        anchors.leftMargin: 10
        anchors.right: parent.right
        anchors.verticalCenter: zdbRectangle.verticalCenter
        color: "#eeeeee"
        radius: height/2

        property real value: 0.0

        Rectangle {
            id: pbRectangle
            width: 0
            height: dmpbgRectangle.height
            anchors.left: dmpbgRectangle.left
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
            dmpbgRectangle.value = percent
            if (animation.running){
                animation.stop()
            }
            animation.from = pbRectangle.width
            animation.to = dmpbgRectangle.width * dmpbgRectangle.value
            animation.start()
        }
        else{
            dmpbgRectangle.value = 0
            pbRectangle.width = 0
        }
    }

    //_config_manager
    Connections {
        target: _config_manager

        onLastVersionChanged: {
            dmLastVersion = version
        }

        onFinalPathChanged: {
            storeTextInput.text = path
        }
    }

    //_template_parser
    Connections {
        target: _template_parser

        onFinalPathChanged: {
            storeTextInput.text = path
        }

        onUrlChanged: {
            dmUrlPrefix = url
        }

        onAppCodeChanged: {
            dmAppCode = code
        }

        onZdbFileChanged: {
            dmZdbFile = file
        }
    }

    //_downloader
    Connections {
        target: _downloader

        onProgressChanged: {
            speed(percent)
        }

        onFeedback: {
            ing = enable
            if (ing){
                zdbRectangle.color = "#aaafba"
                zdbRectangle.enabled = false
            }
            else{
                zdbRectangle.color = "#ff7700"
                zdbRectangle.enabled = true
            }
        }

    }

}


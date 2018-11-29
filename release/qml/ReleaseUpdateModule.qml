import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Dialogs 1.0

Item {
    id: rum
    width: 800
    height: 290

    property real rumLabelWidth: 150 //label标签的宽度
    property real rumLabelHeight: 50
    property alias rumLastVersion: lastVersionTextInput.text
    property alias rumFinalPath: finalPathTextInput.text
    property string rumUrlPrefix: "https://sta-op.douyucdn.cn/dyadmin-ext/client-download/pc/"
    property string rumAppCode: "Douyu_Live_PC_Client"
    property string rumZdbFile: "ProgramConfig.zdb.zip"
    property string rumSrcPath: ""
    property string rumDestPath: ""
    property bool ing: false


    //上一个发行的版本号
    Rectangle {
        id: lastVersionRectangle
        width: rumLabelWidth
        height: rumLabelHeight
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
        height: rumLabelHeight
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

    CustomComboBox {
        id: signCustomComboBox
        height: rumLabelHeight
        width: rumLabelWidth
        anchors.right: parent.right
        anchors.verticalCenter: lastVersionRectangle.verticalCenter
        currentIndex: 0
        model: ["校验签名", "不校验签名"]
    }



    //zdb 标签
    Rectangle {
        id: zdbLabelRectangle
        width: rumLabelWidth
        height: rumLabelHeight
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
        height: rumLabelHeight
        anchors.verticalCenter: zdbLabelRectangle.verticalCenter
        anchors.left: zdbLabelRectangle.right
        anchors.leftMargin: 2
        anchors.right: parent.right
        cursorVisible: false
        font.pixelSize: 10
        renderType: Text.NativeRendering
        font.family: font_yahei
        text: rumUrlPrefix+rumAppCode+"/"+rumLastVersion+"/"+rumZdbFile
        readOnly: true
        selectByMouse: true
    }


    //final文件夹路径
    Rectangle {
        id: finalPathRectangle
        width: rumLabelWidth
        height: rumLabelHeight
        anchors.left: lastVersionRectangle.left
        anchors.top: zdbLabelRectangle.bottom
        anchors.topMargin: 10
        color: "#eeeeee"

        Text {
            id: finalPathText
            anchors.fill: parent
            font.pixelSize: 14
            renderType: Text.NativeRendering
            font.family: font_yahei
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            text: qsTr("final文件夹路径：")
        }
    }

    TextField {
        id: finalPathTextInput
        height: rumLabelHeight
        anchors.verticalCenter: finalPathRectangle.verticalCenter
        anchors.left: finalPathRectangle.right
        anchors.leftMargin: 2
        anchors.right: finalButton.left
        anchors.rightMargin: 2
        cursorVisible: false
        font.pixelSize: 14
        renderType: Text.NativeRendering
        font.family: font_yahei
        placeholderText: qsTr("请输版本文件路径")
        text: ""
        readOnly: true
    }

    //final文件夹路径选择按钮
    Rectangle {
        id: finalButton
        width: 40
        height: 50
        anchors.right: parent.right
        anchors.verticalCenter: finalPathRectangle.verticalCenter
        color: "#eeeeee"

        Text {
            id: finalText
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
                finalFileDialog.open()
            }
        }
    }

    FileDialog {
          id: finalFileDialog
          title: "请选择版本所在的文件夹"
          selectFolder: true

          onAccepted: {
              var urlPath = finalFileDialog.folder.toString()
              finalPath = urlPath.substring(8, urlPath.length)
              mainWindow.finalPathChanged(finalPath)
              _log.print("info", "final path switchs to "+finalPath)
          }

          onRejected: {
              console.log("Canceled")
          }
      }


    //预发版本号
    Rectangle {
        id: versionRectangle
        width: rumLabelWidth
        height: rumLabelHeight
        anchors.left: parent.left
        anchors.top: finalPathRectangle.bottom
        anchors.topMargin: 10
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
        height: rumLabelHeight
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
        width: rumLabelWidth
        height: rumLabelHeight
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
        height: rumLabelHeight
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
        width: rumLabelWidth
        height: rumLabelHeight
        anchors.verticalCenter: versionRectangle.verticalCenter
        anchors.left: vnameTextInput.right
        anchors.leftMargin: 10
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
        height: rumLabelHeight
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



    CustomComboBox {
        id: zipCustomComboBox
        height: rumLabelHeight
        width: rumLabelWidth
        anchors.left: versionRectangle.left
        anchors.top: versionRectangle.bottom
        anchors.topMargin: 10
        currentIndex: 0
        model: ["压缩", "不压缩"]
    }



    //一键打包
    Rectangle {
        id: runRectangle
        width: rumLabelWidth
        height: rumLabelHeight
        anchors.verticalCenter: zipCustomComboBox.verticalCenter
        anchors.left: zipCustomComboBox.right
        anchors.leftMargin: 10
        color: "#aaafba"
        enabled: false
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
                _release_updater.packing(zdbTextInput.text,
                                         rumZdbFile,
                                         versionTextInput.text,
                                         vnameTextInput.text,
                                         minVersionTextInput.text,
                                         zipCustomComboBox.currentIndex==0,
                                         signCustomComboBox.currentIndex==0)
            }
        }
    }

    //进度条
    Rectangle {
        id: pbgRectangle
        height: rumLabelHeight - 30
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

        onLastVersionChanged: {
            rumLastVersion = version
        }

        onFinalPathChanged: {
            rumFinalPath = path
        }

        onParseResultChanged: {
            if (enable){
                runRectangle.color = "#ff7700"
                runRectangle.enabled = true
                finalButton.enabled = true
            }
            else
            {
                runRectangle.color = "#aaafba"
                runRectangle.enabled = false
                finalButton.enabled = false
            }
        }
    }

    //_template_parser
    Connections {
        target: _template_parser

        onFinalPathChanged: {
            rumFinalPath = path
        }

        onUrlChanged: {
            rumUrlPrefix = url
        }

        onAppCodeChanged: {
            rumAppCode = code
        }

        onZdbFileChanged: {
            rumZdbFile = file
        }
    }


    //_release_updater
    Connections {
        target: _release_updater

        onProgressChanged: {
            speed(percent)
        }

        onFeedback: {
            ing = enable
            if (ing){
                runRectangle.color = "#aaafba"
                runRectangle.enabled = false
                finalButton.enabled = false
            }
            else{
                runRectangle.color = "#ff7700"
                runRectangle.enabled = true
                finalButton.enabled = true
            }
        }
    }

    //_ini_producer
    Connections {
        target: _ini_producer

        onVersionChanged: {
            versionTextInput.text = version
        }

        onVersionNameChanged: {
            vnameTextInput.text = versionName
        }

        onMinHideVersionChanged: {
            minVersionTextInput.text = version
        }
    }

}

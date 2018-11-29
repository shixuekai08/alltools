import QtQuick 2.7
import QtQuick.Controls 2.3

Dialog {
    id: naDialog
    title: "历史版本信息"
    width: 600
    height: 400
    padding: 0
    margins: 0

    ScrollView {
        id: naScrollView
        width: naDialog.width
        height: naDialog.height - 48
        clip: true


        ScrollBar.horizontal.policy: ScrollBar.AsNeeded
        ScrollBar.vertical.policy: ScrollBar.AsNeeded

        TextArea {
            id: naTextArea
            renderType: Text.NativeRendering
            font.family: font_yahei
            font.pixelSize: 14
            selectByMouse: true

            background: Rectangle{
                color: "#eeeeee"
            }
        }

    }

    Connections {
        target: _version_manager

        onDataChanged: {
            naTextArea.text = data
        }
    }
}

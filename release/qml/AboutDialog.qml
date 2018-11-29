import QtQuick 2.7
import QtQuick.Controls 2.3

Dialog {
    id: aboutDialog
    title: "关于 斗鱼客户端发版"
    width: 600
    height: 300
    padding: 0
    margins: 0

    Item {
        id: aboutItem
        width: aboutDialog.width
        height: aboutDialog.height - 48

        Text {
            anchors.horizontalCenter: aboutItem.horizontalCenter
            anchors.bottom: aboutItem.bottom
            anchors.bottomMargin: 10
            font.pixelSize: 18
            font.bold: true
            renderType: Text.NativeRendering
            font.family: font_yahei
            text: qsTr("Copyright © 2018 www.douyu.com")
        }

    }
}


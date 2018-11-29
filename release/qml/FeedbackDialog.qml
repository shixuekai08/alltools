import QtQuick 2.7
import QtQuick.Controls 2.3


Dialog {
    id: warnDialog
    title: "提示"
    width: 400
    height: 200

    Text {
        x: 50
        y: 50
        font.pixelSize: 18
        font.bold: true
        color: "red"
        renderType: Text.NativeRendering
        font.family: font_yahei
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        text: qsTr("正在打包中，请稍后再试！！！")
    }
}

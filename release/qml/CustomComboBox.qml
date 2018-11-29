import QtQuick 2.7
import QtQuick.Controls 2.3

ComboBox {
    id: comboBox
    height: 150
    width: 50
    font.family: font_yahei
    font.pixelSize: 14
    currentIndex: 0
    model: ["All"]

    signal clicked(var mouse)

    background: Rectangle {
        border.width: 1
        border.color: "#b0b5ba"
    }

    delegate: Rectangle {
        id: cbRectangle
        width: comboBox.width
        height: comboBox.height
        color: "#ffffff"

        Text {
            id: cbText
            width: cbRectangle.width - 10
            height: cbRectangle.height
            leftPadding: 5
            anchors.centerIn: parent
            font.family: font_yahei
            font.pixelSize: 14
            renderType: Text.NativeRendering
            verticalAlignment: Text.AlignVCenter
            text: modelData
            color: "#000000"
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onExited: {
                cbRectangle.color = "#ffffff"
                cbText.color = "#000000"
            }
            onEntered: {
                cbRectangle.color = "#0078d7"
                cbText.color = "#ffffff"
            }

            onClicked: {
                comboBox.popup.close()
                comboBox.currentIndex = index
                comboBox.clicked(mouse)
            }
        }
    }
}

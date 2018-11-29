import QtQuick 2.7
import QtQuick.Controls 2.3

Rectangle {
    id: leftSideBarRectangle
    width: 70
    height: 200
    color: "#404244"

    property string hoverColor: "#595b5d"
    property string pressColor: "#262829"
    property int selectedBar: 0

    Column {
        width: leftSideBarRectangle.width
        height: leftSideBarRectangle.height

        //发布更新
        Rectangle {
            id: lsb1Rectangle
            width: parent.width
            height: 50
            color: {
                if (selectedBar == 0)
                    return leftSideBarRectangle.pressColor
                else if (lsb1MouseArea.containsMouse)
                    return leftSideBarRectangle.hoverColor
                else
                    return leftSideBarRectangle.color
            }


            Text {
                id: lsb1Text
                anchors.fill: parent
                font.pixelSize: 14
                font.family: font_yahei
                renderType: Text.NativeRendering
                text: qsTr("更新包")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: "#ffffff"
            }

            ToolTip {
                id: lsb1ToolTip
                parent: lsb1Rectangle
                text: "制作发布更新用的包"
                font.pixelSize: 12
                font.family: font_yahei
            }

            MouseArea {
                id: lsb1MouseArea
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    lsb1ToolTip.visible = true
                }

                onExited: {
                    lsb1ToolTip.visible = false
                }

                onPressed: {
                    selectedBar = 0
                }
            }

        }

        //version生成
        Rectangle {
            id: lsb2Rectangle
            width: parent.width
            height: 50
            color: {
                if (selectedBar == 1)
                    return leftSideBarRectangle.pressColor
                else if (lsb2MouseArea.containsMouse)
                    return leftSideBarRectangle.hoverColor
                else
                    return leftSideBarRectangle.color
            }


            Text {
                id: lsb2Text
                anchors.fill: parent
                font.pixelSize: 14
                font.family: font_yahei
                renderType: Text.NativeRendering
                text: qsTr("version")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: "#ffffff"
            }

            ToolTip {
                id: lsb2ToolTip
                parent: lsb2Rectangle
                text: "制作version.ini文件"
                font.pixelSize: 12
                font.family: font_yahei
            }


            MouseArea {
                id: lsb2MouseArea
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    lsb2ToolTip.visible = true
                }

                onExited: {
                    lsb2ToolTip.visible = false
                }

                onPressed: {
                    selectedBar = 1
                }
            }
        }

        //打安装包
        Rectangle {
            id: lsb3Rectangle
            width: parent.width
            height: 50
            color: {
                if (selectedBar == 2)
                    return leftSideBarRectangle.pressColor
                else if (lsb3MouseArea.containsMouse)
                    return leftSideBarRectangle.hoverColor
                else
                    return leftSideBarRectangle.color
            }


            Text {
                id: lsb3Text
                anchors.fill: parent
                font.pixelSize: 14
                font.family: font_yahei
                renderType: Text.NativeRendering
                text: qsTr("安装包")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: "#ffffff"
            }

            ToolTip {
                id: lsb3ToolTip
                parent: lsb3Rectangle
                text: "制作安装用的包"
                font.pixelSize: 12
                font.family: font_yahei
            }


            MouseArea {
                id: lsb3MouseArea
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    lsb3ToolTip.visible = true
                }

                onExited: {
                    lsb3ToolTip.visible = false
                }

                onPressed: {
                    selectedBar = 2
                }
            }
        }


        //下载
        Rectangle {
            id: lsb4Rectangle
            width: parent.width
            height: 50
            color: {
                if (selectedBar == 3)
                    return leftSideBarRectangle.pressColor
                else if (lsb4MouseArea.containsMouse)
                    return leftSideBarRectangle.hoverColor
                else
                    return leftSideBarRectangle.color
            }


            Text {
                id: lsb4Text
                anchors.fill: parent
                font.pixelSize: 14
                font.family: font_yahei
                renderType: Text.NativeRendering
                text: qsTr("下载")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: "#ffffff"
            }

            ToolTip {
                id: lsb4ToolTip
                parent: lsb4Rectangle
                text: "下载已经发布版本的zdb"
                font.pixelSize: 12
                font.family: font_yahei
            }


            MouseArea {
                id: lsb4MouseArea
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    lsb4ToolTip.visible = true
                }

                onExited: {
                    lsb4ToolTip.visible = false
                }

                onPressed: {
                    selectedBar = 3
                }
            }
        }


        //更新率统计
        Rectangle {
            id: lsb5Rectangle
            width: parent.width
            height: 50
            color: {
                if (selectedBar == 4)
                    return leftSideBarRectangle.pressColor
                else if (lsb5MouseArea.containsMouse)
                    return leftSideBarRectangle.hoverColor
                else
                    return leftSideBarRectangle.color
            }


            Text {
                id: lsb5Text
                anchors.fill: parent
                font.pixelSize: 14
                font.family: font_yahei
                renderType: Text.NativeRendering
                text: qsTr("更新率")
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: "#ffffff"
            }

            ToolTip {
                id: lsb5ToolTip
                parent: lsb5Rectangle
                text: "统计更新率"
                font.pixelSize: 12
                font.family: font_yahei
            }


            MouseArea {
                id: lsb5MouseArea
                anchors.fill: parent
                hoverEnabled: true

                onEntered: {
                    lsb5ToolTip.visible = true
                }

                onExited: {
                    lsb5ToolTip.visible = false
                }

                onPressed: {
                    selectedBar = 4
                }
            }
        }


    }
}

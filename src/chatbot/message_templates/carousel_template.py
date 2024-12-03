from linebot.models import FlexSendMessage


def create_houses_carousel(data_list):
    bubbles = []
    for data in data_list:
        # Create bubble structure for every house item
        bubble = {
            "type": "bubble",
            "size": "mega",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    # {
                    #     "type": "image",
                    #     "url": f"https://yourimagestorage.com/{data['Photo']}",
                    #     "size": "full",
                    #     "aspectMode": "cover",
                    #     "aspectRatio": "320:213",
                    # },
                    {
                        "type": "text",
                        "text": f"{data['City']}, {data['District']}",
                        "wrap": True,
                        "weight": "bold",
                        "size": "md",
                    },
                    {
                        "type": "text",
                        "text": f"街道: {data['Street']}",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": f"樓層: {data['Floor']}",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": f"類型: {data['Type']}",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": f"大小: {data['Size']} 坪",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": f"能否開火: {'可以' if data['Fire'] else '不行'}",
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "text",
                        "text": f"能否議價: {'可以' if data['Negotiate_Price'] else '不行'}",  # noqa
                        "size": "sm",
                        "color": "#666666",
                        "wrap": True,
                    },
                    {
                        "type": "button",
                        "action": {
                            "type": "uri",
                            "label": "查看更多",
                            "uri": data["URL"],
                        },
                        "style": "primary",
                        "color": "#905c44",
                        "margin": "md",
                    },
                ],
            },
        }
        bubbles.append(bubble)

    # Use carousel sructure to organize bubbles
    carousel = {"type": "carousel", "contents": bubbles}

    return FlexSendMessage(alt_text="房屋推薦", contents=carousel)

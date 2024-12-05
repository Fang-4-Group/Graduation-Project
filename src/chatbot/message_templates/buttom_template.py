from linebot.models import ButtonsTemplate, PostbackAction, TemplateSendMessage


def create_check_button():
    template = ButtonsTemplate(
        title="Summary Checklist",
        text="See the checklist to keep track of your chatting progress.",
        actions=[
            PostbackAction(
                label="Check my checklist",
                data="action=call_llm_api",
            )
        ],
    )

    return TemplateSendMessage(
        alt_text="Check your progress", template=template
    )  # noqa

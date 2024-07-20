from linebot.models import ButtonsTemplate, PostbackAction, TemplateSendMessage


def create_check_button():
    template = ButtonsTemplate(
        title="Checklist",
        text="Press the button to get the checklist.",
        actions=[
            PostbackAction(
                label="Call LLM API",
                display_text="Checking progress...",
                data="action=call_llm_api",
            )
        ],
    )

    return TemplateSendMessage(
        alt_text="Check your progress", template=template
    )  # noqa

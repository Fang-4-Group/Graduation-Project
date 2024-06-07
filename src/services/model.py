import torch
from transformers import AutoImageProcessor, ResNetForImageClassification

from datasets import load_dataset


async def test():
    dataset = load_dataset("huggingface/cats-image", trust_remote_code=True)
    image = dataset["test"]["image"][0]

    processor = AutoImageProcessor.from_pretrained("microsoft/resnet-50")
    model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")

    inputs = processor(image, return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    # model predicts one of the 1000 ImageNet classes
    predicted_label = logits.argmax(-1).item()
    print(model.config.id2label[predicted_label])
    return model.config.id2label[predicted_label]

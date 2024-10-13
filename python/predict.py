from PIL import Image
import torch
from model import FoodClassifier
from torchvision import transforms
import torch.nn.functional as F
from classes import class_to_idx

def predict(image_path, model_path, class_to_idx):
    print('Model yükleniyor...')
    model = FoodClassifier(len(class_to_idx))
    model.load_state_dict(torch.load(model_path))
    model.eval()
    print('Model yüklendi.')

    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

    print(f'Görüntü yükleniyor: {image_path}')
    image = Image.open(image_path).convert('RGB')
    image = transform(image).unsqueeze(0)

    print('Tahmin yapılıyor...')
    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)
        max_prob, predicted = torch.max(probabilities, 1)

    threshold = 0.9
    if max_prob.item() < threshold:
        print("Tahmin belirsiz, lütfen başka bir resim deneyin.")
        return None
    else:
        idx_to_class = {v: k for k, v in class_to_idx.items()}
        predicted_class = idx_to_class[predicted.item()]
        print(f'Tahmin edilen sınıf: {predicted_class}')

    return predicted_class

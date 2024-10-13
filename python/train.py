import torch
import torch.optim as optim
import torch.nn as nn
from data_loader import load_data
from model import FoodClassifier

data_dir = 'TurkishFood'
dataloader, class_to_idx = load_data(data_dir)
print(f'Loaded {len(dataloader.dataset)} images.')

num_classes = len(class_to_idx)
model = FoodClassifier(num_classes)

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    epoch_loss = 0  # Epok kaybını tutmak için
    for images, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()  # Her döngüde kaybı toplayın

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss/len(dataloader):.4f}')

# Modeli kaydedin
torch.save(model.state_dict(), 'food_classifier2.pth')
print("Model kaydedildi: food_classifier2.pth")
